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

Synchronize a personal foobar2000 music library to a FiiO Snowsky Echo Nano DAP using a nested-directory layout.

The Echo Nano firmware lacks native `.m3u` playlist support and has an 8,192-file hardware indexing ceiling. This script organizes tracks into a nested directory layout so curated favorites can be accessed via folder navigation while keeping full-library chronological playback intact without duplicating files.

**Architecture & How It Works:**

* **Favorites Direct Access (`Storage > TF Card > Music > <Favorites>`):** Favorite tracks are placed into `/Music/<Favorite Playlist>/` for 1-click folder browsing.
* **Full Library Order (`Category > All Songs`):** Recursively indexes `/Music/`, sorting the entire collection by zero-padded filename rank (`0001.`, `0002.`, …) in foobar2000 playlist order.
* **Zero Duplicate Files:** Tracks exist as single physical files on disk to stay safely below the 8,192-file firmware indexing limit.
* **Embedded Cover Art Stripping:** Automatically removes embedded images across FLAC, MP3, WAV, OGG, OPUS, and M4A to save flash storage (can be disabled with `--keep-cover-art`).
* **Fully Idempotent & Incremental:** Inspects actual on-disk state and records progress to an on-card `.manifest_nested.json` manifest. Safe to cancel with `Ctrl+C` and resume anytime.
* **Safety & Reliability:** Pre-flight disk space checks, automatic FAT32/exFAT dot-file cleanup (`.DS_Store`, `._*`), filesystem write-cache sync (`os.sync()`), and optional post-sync unmounting.

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
echo-nano-sync --keep-cover-art        # Preserve embedded album artwork in audio files
echo-nano-sync --dry-run               # Preview plan (copies, moves, art strips) without writing
echo-nano-sync --limit 20              # Sync only the first 20 tracks (useful for test runs)
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

