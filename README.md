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

Synchronize a personal foobar2000 music library to a FiiO Snowsky Echo Nano DAP using a flat card-root layout, with fully automatic sync when the player is plugged in.

The Echo Nano firmware lacks native `.m3u` playlist support and has an 8,192-file hardware indexing ceiling. Its File Browser sorts files by raw directory-entry order (not by filename), so this script renumbers tracks with zero-padded rank prefixes and then runs `fatsort` to physically reorder the card's directory entries — giving correct playback order without rewriting any audio data.

**Architecture & How It Works:**

* **Favorites Direct Access (`Storage > TF Card > Top Rated`):** Favorite tracks are placed into `/Top Rated/` at the card root for 1-click folder browsing.
* **Full Library Order (File Browser at card root):** Non-favorite tracks live at the card root, named `0001.`, `0002.`, … in foobar2000 playlist order. A `fatsort -n` pass reorders the FAT directory entries so the Nano's File Browser (which sorts by copy order) shows them in the correct sequence.
* **Zero Duplicate Files:** Tracks exist as single physical files on disk to stay safely below the 8,192-file firmware indexing limit.
* **Embedded Cover Art Stripping:** Automatically removes embedded images across FLAC, MP3, WAV, OGG, OPUS, and M4A to save flash storage (can be disabled with `--keep-cover-art`).
* **Atomic, Crash-Safe Writes:** Every file is staged in a hidden `.sync_tmp` directory, fsynced, then atomically renamed into place — a real filename never holds a torn/partial write, so unplugging mid-sync can't corrupt existing tracks.
* **Idempotent & Resumable:** State is recorded in an on-card `.manifest_nested.json` (per-track `rel_path`, `rank`, `title`, `mtime`, and on-card `size`). Re-running reconciles against actual on-disk state, validates sizes, and resumes where an interrupted run left off. `Ctrl+C` finishes the current file, saves progress, and exits cleanly; just run it again to continue.
* **Safety & Reliability:** Pre-flight disk space checks, automatic FAT32/exFAT junk cleanup (`.DS_Store`, `._*`, `.Spotlight-V100`, `.fseventsd`, …), `os.sync()` barriers between phases and after `fatsort`, a `fsck.fat` repair before sorting, and the card is left safely unmounted on completion.
* **Notifications:** Desktop notifications on sync start and completion.

**Automatic sync on plug-in:** A background watcher (`echo-nano-sync-watch`, documented below) runs the sync automatically whenever the player is plugged in.

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
echo-nano-sync                             # Manual incremental sync; leaves the card unmounted
echo-nano-sync --keep-cover-art            # Preserve embedded album artwork in audio files
echo-nano-sync --dry-run                   # Preview plan (copies, moves, art strips) without writing
echo-nano-sync --limit 20                  # Sync only the first 20 tracks (useful for test runs)
echo-nano-sync --force-strip               # Force re-check and strip embedded art from all files on card
echo-nano-sync --dest /path/to/mount       # Specify a custom SD card mount path

systemctl --user enable --now echo-nano-sync      # Auto-sync whenever the player is plugged in
journalctl --user -u echo-nano-sync -f            # Watch a background sync live
tail -f ~/.local/state/echo-nano-sync.log         # ...or its log file
```

**Requirements:**

* Python 3.9+ with `mutagen`
* foobar2000 (Wine) with playlists saved in `.fplite` format
* `fatsort` (sorts FAT directory entries for correct Nano playback order)
* `dosfstools` (provides `fsck.fat` for pre-sort filesystem repair)
* `udisks2` (provides `udisksctl` for mounting/unmounting the card)
* `libnotify` / `notify-send` (optional, for desktop notifications)
* systemd (user session) for the auto-sync watcher


---

### 🔄 echo-nano-sync-watch

Background watcher that automatically syncs the Echo Nano whenever the player is plugged in. Companion to `echo-nano-sync`.

**How it works:**

* Polls every 2 s for the Nano's SD card partition, identified by udev identity `ID_MODEL=NANO_SD` — this cleanly distinguishes the card from the player's internal `NANO` storage, and works even when the card isn't mounted.
* On detection: ensures the card is mounted (`udisksctl mount` if needed), verifies it's a synced library (has `.manifest_nested.json`), then runs `echo-nano-sync --dest <mount>`.
* After the sync finishes (it unmounts the card), the watcher waits for the player to be **unplugged** before it will sync again — so it runs once per plug-in rather than looping.
* Sends a desktop notification if the card can't be mounted or the sync fails.

**Logging:** the sync output is echoed live both to the systemd journal and appended to `~/.local/state/echo-nano-sync.log`:

```bash
journalctl --user -u echo-nano-sync -f          # live output from the service
tail -f ~/.local/state/echo-nano-sync.log       # ...or the plain log file
```

**Running it as a service:**

```bash
systemctl --user enable --now echo-nano-sync     # start at login and run now
systemctl --user status echo-nano-sync           # check it's watching
systemctl --user disable --now echo-nano-sync    # stop auto-sync
```

The unit file (`echo-nano-sync.service`) lives in `~/.config/systemd/user/` (kept in dotfiles), starts the watcher at login, and restarts it on failure.

**Prerequisites:**

* `~/bin` cloned so both `echo-nano-sync` and `echo-nano-sync-watch` are present (the setup skips otherwise).
* **Passwordless sudo** for just `fatsort` and `fsck.fat` — headless runs have no terminal to prompt at. Installed as `/etc/sudoers.d/echo-nano-sync` by the dotfiles desktop setup.
* The same packages as `echo-nano-sync` (`udisks2`, `fatsort`, `dosfstools`, `libnotify`).

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

