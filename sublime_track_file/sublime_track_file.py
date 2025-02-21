import sublime
import sublime_plugin
from pathlib import Path
import time

class TrackFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings('SublimeTrackFile.sublime-settings')
        default_file = settings.get('default_track_file', '')
        
        self.window.show_input_panel(
            "Enter file path to track:",
            default_file,
            self.on_done,
            None,
            None
        )

    def on_done(self, file_path):
        view = self.window.active_view()
        if view:
            view.run_command('start_tracking_file', {'file_path': file_path})

class StartTrackingFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path):
        settings = sublime.load_settings('SublimeTrackFile.sublime-settings')
        watch_interval = settings.get('watch_interval', 1000)  # Default to 1 second
        max_file_size = settings.get('max_file_size', 1048576)  # Default to 1MB
        
        self.view.settings().set('track_file_path', file_path)
        self.view.run_command('watch_file', {'file_path': file_path, 'watch_interval': watch_interval, 'max_file_size': max_file_size})

class StopTrackingFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('watch_file', {'stop': True})
        self.view.settings().erase('track_file_path')

class WatchFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path=None, watch_interval=1000, max_file_size=1048576, stop=False):
        if hasattr(self.view, 'file_watcher'):
            self.view.file_watcher.stop()
            
        if not stop and file_path:
            self.view.file_watcher = FileWatcher(self.view, file_path, watch_interval, max_file_size)
            self.view.file_watcher.start()

class FileWatcher:
    def __init__(self, view, watch_file, watch_interval=1000, max_file_size=1048576):
        self.view = view
        self.watch_file = watch_file
        self.watch_interval = watch_interval
        self.max_file_size = max_file_size
        self.is_watching = False
        self.last_modified = 0
        self.last_position = 0
        
    def start(self):
        self.is_watching = True
        try:
            self.last_modified = Path(self.watch_file).stat().st_mtime
            self.last_position = Path(self.watch_file).stat().st_size
        except Exception as e:
            print(f"Error starting file watch: {e}")
        sublime.set_timeout_async(self.watch_file_async, self.watch_interval)
        
    def stop(self):
        self.is_watching = False
        
    def truncate_file_if_needed(self):
        """Keep only the last max_file_size bytes of the file"""
        try:
            with open(self.watch_file, 'r', newline='') as f:
                content = f.read()
            if len(content) > self.max_file_size:
                with open(self.watch_file, 'w', newline='') as f:
                    f.write(content[-self.max_file_size:])
                self.last_position = self.max_file_size
        except Exception as e:
            print(f"Error truncating file: {e}")

    def normalize_line_endings(self, text):
        """Normalize line endings to match the view's line endings"""
        if not text:
            return text
            
        # Get the view's line ending setting
        view_line_endings = self.view.line_endings()
        # First convert all line endings to \n
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Then convert to the desired line ending if windows
        if view_line_endings == 'windows':
            text = text.replace('\n', '\r\n')
        return text
    
    def watch_file_async(self):
        if not self.is_watching:
            return
            
        try:
            current_mtime = Path(self.watch_file).stat().st_mtime
            current_size = Path(self.watch_file).stat().st_size
            
            # Check if file size exceeds limit
            if current_size > self.max_file_size:
                self.truncate_file_if_needed()
            
            if current_mtime > self.last_modified and current_size > self.last_position:
                with open(self.watch_file, 'r', newline='') as f:
                    f.seek(self.last_position)
                    new_text = f.read(current_size - self.last_position)
                    print(f"New text detected (raw): {repr(new_text)}")
                    
                    if new_text:
                        # Normalize line endings
                        new_text = self.normalize_line_endings(new_text)
                        print(f"Normalized text: {repr(new_text)}")
                        
                        # Insert text exactly as is, without adding any extra newlines
                        self.view.run_command('insert_annotation', {'text': new_text})
                        
                self.last_modified = current_mtime
                self.last_position = current_size
                print(f"Updated position to: {self.last_position}")
        except Exception as e:
            print(f"Error watching file: {e}")
            
        sublime.set_timeout_async(self.watch_file_async, 1000)

class InsertAnnotationCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        # Get the current cursor position
        insert_point = self.view.sel()[0].begin()
        
        # Insert the text
        self.view.insert(edit, insert_point, text)
        
        # Set cursor position to end of inserted text
        new_cursor_position = insert_point + len(text)
        
        # Clear current selection and set cursor position
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(new_cursor_position, new_cursor_position)) 