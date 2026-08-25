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

* `bluetoothctl` (bluez package)
* `fzf` (fuzzy finder)
* `awk` (text processing)

---

### 🎵 foobar2000

Command-line interface to a Wine installation of foobar2000.

**Features:**

* Automatically converts Linux paths to Windows-style paths
* Launches foobar2000 in the background
* Passes command-line arguments to foobar2000

**Usage:**

```bash
foobar2000 /path/to/music.flac
foobar2000 ~/Music/*.mp3
```

**Requirements:**

* Wine
* foobar2000 installed in Wine prefix

**Credits:** Written by Drew Weymouth

---

### 🎶 echo-nano-sync

Synchronize a personal foobar2000 music library to a FiiO Snowsky Echo Nano DAP SD card using a nested-directory layout.

The Echo Nano firmware lacks native `.m3u` playlist support and has an 8,192-file hardware indexing ceiling. This script organizes files into a nested directory structure so you get 1-click access to curated favorites while keeping full library playback in chronological order—without duplicating files or mangling audio metadata.

**Architecture & How it Works:**

* **Zero Metadata Mangling:** Leaves all audio tags (`TITLE`, `ARTIST`, `ALBUM`, `GENRE`) completely untouched.
* **Embedded Cover Art Stripping:** Automatically removes high-resolution embedded images (`APIC`, `covr`, FLAC pictures) to optimize storage on FAT32/exFAT.
* **Top Rated (`Storage > TF Card > Music > Top Rated`):** 4★+ songs live in `/Music/Top Rated/` for direct, single-click folder browsing.
* **All Songs (`Category > All Songs`):** Recursively indexes `/Music/` and `/Music/Top Rated/`, playing the entire collection sorted by zero-padded filename rank (`0001.`, `0002.`, …) in exact foobar2000 reverse-date order.
* **Zero Duplicate Files:** Keeps all tracks as single physical files, comfortably staying within the 8,192-track limit.
* **Incremental & Resumable:** Tracks state on-card in `.manifest_nested.json` after every write. Safe to interrupt with `Ctrl+C` and resume anytime.
* **Safety Checks:** Pre-flight free storage validation, auto-cleanup of OS junk files (`.DS_Store`, `._*`), write-cache flushing (`os.sync()`), and optional auto-eject.

**Defaults** (auto-detected or overridden via CLI):

| Setting | Default | Description |
| --- | --- | --- |
| foobar2000 profile | `~/foobar2000/profile` | Location of playlist index and `.fplite` files |
| Source library | `~/Music/0Main` | Root directory of your local music library |
| Master playlist | `Library Sorted` | Full library ordered chronologically |
| Top-rated playlist | `Top Rated` | Curated favorites playlist |
| SD card mount | `/run/media/$USER/*` | Auto-detects mounted removable storage |

**Usage:**

```bash
echo-nano-sync                         # Incremental sync of library to auto-detected SD card
echo-nano-sync --eject-after           # Sync and safely unmount the card with udisksctl on completion
echo-nano-sync --dry-run               # Preview plan (copies, moves, art strips) without writing
echo-nano-sync --limit 20              # Sync only the first 20 tracks (useful for fast verification)
echo-nano-sync --force-strip           # Force re-check and strip embedded art from all files on card
echo-nano-sync --dest /path/to/mount   # Specify a custom SD card mount path
```

**Requirements:**

* Python 3.9+ with `mutagen`
* foobar2000 (Wine) with playlists saved in `.fplite` format
* `udisksctl` (optional, for `--eject-after`)
* `libnotify` / `notify-send` (optional, for desktop notifications)

---

### 🍷 dwproton-run

Convenience wrapper for running Windows applications with a specific Proton version via Lutris.

**Usage:**

```bash
dwproton-run program.exe
```

**Requirements:**

* Lutris with Proton runner installed

---

### ⌨️ run-wooting

Wrapper script to run Wooting Background Service in a distrobox container.

**Features:**

* Solves GLIBC compatibility issues on older distros
* Runs the service in an Ubuntu 24.04 container

**Usage:**

```bash
run-wooting
```

**Requirements:**

* `distrobox`
* Wooting Background Service AppImage
* Ubuntu 24.04 container named `wooting-container`

---

### 🌐 mkwebapp

Creates a KDE/Wayland-compatible `.desktop` file for a web app using a Chromium-based browser.

**Features:**

* Automatically fetches the page title if no name is given
* Downloads a 128x128 favicon as the app icon
* Names the `.desktop` file after the Chromium Wayland app ID so KDE matches the taskbar icon correctly
* Detects duplicates and exits early to avoid overwriting existing entries

**Usage:**

```bash
mkwebapp <URL> [App Name]
mkwebapp https://music.youtube.com "YouTube Music"
mkwebapp https://music.youtube.com   # fetches title automatically
```

**Requirements:**

* `helium-browser`, `google-chrome-stable`, or `chromium`
* `curl`
* `file`

---

### ⚔️ sekirofpsunlock

A binary executable to patch Sekiro: Shadows Die Twice for Linux.

Original project [Repository](https://github.com/Lahvuun/sekirofpsunlock)

Launch Option Example:

```text
sekirofpsunlock 15 set-resolution 2560 2560 1440 set-fps 180 & %command%
```

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/umutondersu/bin-scripts.git ~/bin
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

```

