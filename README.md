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

### 🎶 echo-nano-sync

Sync foobar2000 playlists to a FiiO SnowSky ECHO NANO SD card.

The ECHO NANO ignores `.m3u` files entirely — its SoC can't read them. This script works around that by copying tracks into per-playlist folders with embedded tags (`ALBUM`, `ALBUMARTIST`, `TRACKNUMBER`) so the device's album/artist browser shows them as playlists.

**Features:**

- Reads foobar2000 `.fplite` playlists directly — no intermediate files needed
- Incrementally syncs to the card: only copies new tracks, removes dropped ones, renames/reorders changed positions
- Enforces the device's 8,192-track firmware limit across all playlists
- Zero-padded filenames (`0001`, `0002`, …) so the player sorts by playlist order, not alphabetically
- `--repad` command to fix padding on existing cards without re-copying
- `--reset --yes` to wipe the card workspace and do a clean rebuild
- `--convert-only` to export playlists as `.m3u` files without touching the card
- `--dry-run` to preview changes without writing anything

**Defaults** (edit constants at top of script if paths change):

| Setting | Default |
|---|---|
| foobar2000 profile | `~/foobar2000/profile` |
| Source library | `~/Music/0Main` |
| SD card mount | `/run/media/qorcialwolf/NANO SD` |

**Usage:**

```bash
echo-nano-sync --list                              # list all foobar playlists + track counts
echo-nano-sync                                     # convert + sync "Top Rated" (default)
echo-nano-sync --playlists "Top Rated,Favorites"  # multiple playlists
echo-nano-sync --playlists all                    # every playlist except whole-library dupes
echo-nano-sync --sync-only                        # sync to card only (no .m3u export)
echo-nano-sync --convert-only                     # export .m3u files only, don't touch card
echo-nano-sync --reset --yes                      # wipe card workspace and rebuild (~2h for 1721 tracks)
echo-nano-sync --repad                            # fix filename padding on existing card (seconds)
echo-nano-sync --dry-run                          # preview without writing
```

**Requirements:**

- Python venv at `~/src/echo-nano/.venv` with `mutagen` installed
- EchoList library at `~/src/echo-nano/echolist`
- foobar2000 (Wine) with playlists saved as `.fplite` format
- SD card mounted at `/run/media/qorcialwolf/NANO SD`

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
