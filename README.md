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

---

### 📞 kdeconnect-mic-mute

Automatically mutes the microphone when a phone call is active via KDE Connect, and unmutes when the call ends.

**How it works:**

KDE Connect's PauseMusic plugin already mutes the default output sink during calls. This script watches for sink mute state changes via `pactl subscribe` and mirrors them to the default input source (microphone). The KDE Connect telephony D-Bus signals are also monitored as a supplementary path for incoming call detection.

**Usage:**

Runs as a systemd user service — no manual interaction needed.

```bash
systemctl --user status kdeconnect-mic-mute   # Check status
journalctl --user -fu kdeconnect-mic-mute     # Watch live logs
```

**Requirements:**
- KDE Connect with PauseMusic plugin enabled and configured to mute system sound
- `pactl` (PipeWire or PulseAudio)
- `python-dbus`

---

### 📱 scrcpy-autostart

Automatically launches scrcpy when an Android phone is plugged in via USB.

**Features:**
- Launched by udev via `systemd-run --user`
- Waits up to 30 seconds for ADB authorisation before proceeding
- Launches scrcpy with screen-off and stay-awake flags

**Usage:**

Triggered automatically by udev when a device is connected. Can also be run manually:
```bash
scrcpy-autostart
```

**Requirements:**
- `adb` (Android Debug Bridge)
- `scrcpy`
- udev rule to trigger on device plug-in

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
