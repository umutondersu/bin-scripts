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

### 🍷 dwproton-run.sh

Convenience wrapper for running Windows applications with a specific Proton version via Lutris.

**Usage:**
```bash
dwproton-run.sh program.exe
```

**Requirements:**
- Lutris with Proton runner installed

---

### ⌨️ run-wooting.sh

Wrapper script to run Wooting Background Service in a distrobox container.

**Features:**
- Solves GLIBC compatibility issues on older distros
- Runs the service in an Ubuntu 24.04 container

**Usage:**
```bash
run-wooting.sh
```

**Requirements:**
- `distrobox`
- Wooting Background Service AppImage
- Ubuntu 24.04 container named `wooting-container`

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
