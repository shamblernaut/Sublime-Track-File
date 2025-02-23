# Sublime Track File

A Sublime Text plugin that allows you to track changes in a file and automatically insert new content into your current view. Perfect for real-time monitoring of log files or any text file that updates frequently.

## Features

- Track changes in any text file in real-time
- Automatically insert new content at cursor position
- Configurable watch interval
- Proper handling of different line endings (Windows/Unix)
- Customizable settings

## Installation

### Manual Installation

1. Download or clone this repository
2. Copy all files to your Sublime Text Packages directory:
   - Linux: `~/.config/sublime-text/Packages/User/`
   - Windows: `%APPDATA%\Sublime Text\Packages\User\`
   - macOS: `~/Library/Application Support/Sublime Text/Packages/User/`

### Package Control (Coming Soon)

Support for Package Control installation will be added in the future.

## Usage

1. Open Sublime Text
2. Open a new file where you want the tracked content to appear
3. Press `Ctrl+Shift+T` (Windows/Linux) or use the command palette to select "Track File: Start Tracking"
4. Enter the path to the file you want to track
5. Any new content added to the tracked file will appear at your cursor position
6. To stop tracking, use the command palette and select "Track File: Stop Tracking"

## Settings

The plugin can be configured through the settings file. Create a file named `SublimeTrackFile.sublime-settings` in your User packages directory with these options:

```json
{
    // The interval (in milliseconds) at which to check for file changes
    "watch_interval": 1000,

    // Default file path to track (optional)
    // If set, this file will be pre-filled when starting tracking
    "default_track_file": ""
}
```

## Key Bindings

Default key binding:
- `ctrl+shift+t`: Start tracking a file

You can customize the key binding by editing your key bindings file.

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 