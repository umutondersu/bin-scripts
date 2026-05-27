# Personal Utility Scripts

A collection of useful command-line utilities and helper scripts for Linux.

## Scripts

### 🎮 bt-menu

Interactive Bluetooth manager with a clean command-line interface using `fzf`.

**Features:**

- Scan and pair with new Bluetooth devices
- Manage paired devices (connect/disconnect/forget)
- List connected devices with status, battery level, and device type
- Configurable scan duration for pairing

**Usage:**

```bash
bt-menu              # Show help
bt-menu pair         # Scan for 5 seconds and pair with a new device
bt-menu pair 10      # Scan for 10 seconds (custom duration)
bt-menu manage       # Interactively manage paired devices
bt-menu ls           # List connected devices
bt-menu ls --all     # List all paired devices with status
```

**Requirements:**

- `bluetoothctl` (bluez package)
- `fzf` (fuzzy finder)
- `awk` (text processing)

---

### 🎵 foobar2000

Command-line interface to a Wine installation of foobar2000.

**Features:**

- Automatically converts Linux paths to Windows-style paths
- Launches foobar2000 in the background
- Passes command-line arguments to foobar2000

**Usage:**

```bash
foobar2000 /path/to/music.flac
foobar2000 ~/Music/*.mp3
```

**Requirements:**

- Wine
- foobar2000 installed in Wine prefix

**Credits:** Written by Drew Weymouth

---

### 🍷 dwproton-run

Convenience wrapper for running Windows applications with a specific Proton version via Lutris.

**Usage:**

```bash
dwproton-run program.exe
```

**Requirements:**

- Lutris with Proton runner installed

---

### ⌨️ run-wooting

Wrapper script to run Wooting Background Service in a distrobox container.

**Features:**

- Solves GLIBC compatibility issues on older distros
- Runs the service in an Ubuntu 24.04 container

**Usage:**

```bash
run-wooting
```

**Requirements:**

- `distrobox`
- Wooting Background Service AppImage
- Ubuntu 24.04 container named `wooting-container`

### 🌐 mkwebapp

Creates a KDE/Wayland-compatible `.desktop` file for a web app using a Chromium-based browser.

**Features:**

- Automatically fetches the page title if no name is given
- Downloads a 128x128 favicon as the app icon
- Names the `.desktop` file after the Chromium Wayland app ID so KDE matches the taskbar icon correctly
- Detects duplicates and exits early to avoid overwriting existing entries

**Usage:**

```bash
mkwebapp <URL> [App Name]
mkwebapp https://music.youtube.com "YouTube Music"
mkwebapp https://music.youtube.com   # fetches title automatically
```

**Requirements:**

- `helium-browser`, `google-chrome-stable`, or `chromium`
- `curl`
- `file`

---

### sekirofpsunlock

A binary executable to patch Sekiro: Shadows Die Twice for Linux.

Original project [Repository](https://github.com/Lahvuun/sekirofpsunlock)

Launch Option Example:

```
sekirofpsunlock 15 set-resolution 2560 2560 1440 set-fps 180 & %command%
```

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/YOUR_USERNAME/bin-scripts.git ~/bin
```

2. Ensure `~/bin` is in your PATH:

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

3. Make scripts executable (if needed):

```bash
chmod +x ~/bin/*
```

## Contributing

These are personal scripts, but feel free to fork and adapt them for your own use!

## License

MIT License - Feel free to use and modify as needed.
