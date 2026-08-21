#!/home/qorcialwolf/src/echo-nano/.venv/bin/python3
"""Echo NANO sync pipeline.

Stage 1 — CONVERT: regenerate UTF-8 .m3u playlists in ~/Music/0Main/Playlists
   from foobar2000's authoritative .fplite data (never touching audio files).

Stage 2 — SYNC: deploy selected playlists to the SD card via the EchoList
   library (folder-per-playlist copies + playlist tags), enforcing the
   8,192-track firmware limit.

Usage examples:
  echo-nano-sync.py --list
  echo-nano-sync.py --playlists "Top Rated,R Top Rated"            # convert + sync
  echo-nano-sync.py --playlists "Top Rated" --sync-only            # card only
  echo-nano-sync.py --playlists "Top Rated" --convert-only         # m3u only
  echo-nano-sync.py --playlists "Top Rated" --reset --yes          # wipe card workspace, full rebuild
  echo-nano-sync.py --playlists "Top Rated" --desired-set "..."    # (future) 

Sync is incremental: it adds new tracks, removes stale ones, and reorders
copies to match the foobar playlist order — only copying the delta.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HOME = Path.home()
MAX_TRACKS = 8192

DEFAULT_PROFILE = HOME / "foobar2000" / "profile"
DEFAULT_SOURCE_ROOT = HOME / "Music" / "0Main"
DEFAULT_PLAYLIST_DIR = DEFAULT_SOURCE_ROOT / "Playlists"
DEFAULT_DEST = Path("/run/media/qorcialwolf/NANO SD")
DEFAULT_ECHOLIST_SRC = HOME / "src" / "echo-nano" / "echolist"

# Internal playlists that are just the whole library under another name.
DUPES_OF_WHOLE_LIBRARY = {"Whole Library", "Library Playback"}


def _add_echolist_to_path(echolist_src: Path) -> None:
    if str(echolist_src) not in sys.path:
        sys.path.insert(0, str(echolist_src))
    try:
        import echolist.manager  # noqa: F401
    except ImportError as exc:
        sys.exit(f"cannot import echolist from {echolist_src}: {exc}")


def load_playlist_index(profile: Path) -> dict[str, str]:
    """Map foobar GUID -> playlist name from playlists-v2.0/index.txt."""
    index_file = profile / "playlists-v2.0" / "index.txt"
    if not index_file.exists():
        sys.exit(f"foobar playlist index not found: {index_file}")
    mapping: dict[str, str] = {}
    for line in index_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        guid, name = line.split(":", 1)
        mapping[guid.strip()] = name.strip()
    return mapping


def resolve_fplite_name(name: str, index: dict[str, str]) -> str:
    """Return the canonical playlist name matching `name` (case/fold-insensitive)."""
    from echolist.naming import playlist_id
    target = playlist_id(name)
    for candidate in index.values():
        if playlist_id(candidate) == target:
            return candidate
    return name


def get_fplite_path(profile: Path, guid: str) -> Path:
    return profile / "playlists-v2.0" / f"playlist-{guid}.fplite"


def parse_fplite(fplite: Path, source_root: Path) -> tuple[list[Path], list[str]]:
    """Read one .fplite -> (tracks in playlist order, unresolved entries)."""
    tracks: list[Path] = []
    missing: list[str] = []
    for raw in fplite.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line:
            continue
        entry = line[len("file-relative://"):] if line.startswith("file-relative://") else line
        entry = entry.replace("\\", "/")
        marker = "0Main/"
        if marker in entry:
            entry = entry.split(marker, 1)[1]
        p = source_root / entry
        if p.is_file():
            tracks.append(p.resolve())
        else:
            missing.append(line)
    return tracks, missing


def write_m3u(name: str, tracks: list[Path], dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / f"{name}.m3u"
    body = [f"#PLAYLIST: {name}"] + [str(p) for p in tracks]
    out.write_text("\n".join(body) + "\n", encoding="utf-8-sig")
    return out


def convert_playlists(profile: Path, source_root: Path, dest_dir: Path,
                      selected: list[str], dry_run: bool = False) -> list[dict]:
    index = load_playlist_index(profile)
    reports = []
    for sel in selected:
        canonical = resolve_fplite_name(sel, index)
        guid = next((g for g, n in index.items() if n == canonical), None)
        if guid is None:
            reports.append({"name": sel, "error": f"no foobar playlist named '{sel}'"})
            continue
        fplite = get_fplite_path(profile, guid)
        if not fplite.exists():
            reports.append({"name": canonical, "error": f"missing {fplite.name}"})
            continue
        tracks, missing = parse_fplite(fplite, source_root)
        out = None
        if not dry_run:
            out = write_m3u(canonical, tracks, dest_dir)
        reports.append({
            "name": canonical,
            "guid": guid,
            "fplite": fplite.name,
            "tracks": len(tracks),
            "missing": missing,
            "out": str(out) if out else str(dest_dir / f"{canonical}.m3u"),
        })
    return reports


def load_selected_m3u(name: str, playlist_dir: Path, source_root: Path) -> list[Path]:
    """Return resolved, ordered track paths from a generated .m3u file."""
    from echolist.m3u import parse_m3u
    result = parse_m3u(playlist_dir / f"{name}.m3u", source_root=source_root)
    if result["missing"]:
        print(f"    WARNING {len(result['missing'])} m3u entries did not resolve")
    return result["tracks"]


def open_manager(dest_root: Path, source_root: Path) -> "object":
    from echolist.manager import PlaylistManager
    workspace_config = dest_root / "Playlists" / ".echolist" / "config.json"
    if workspace_config.exists():
        return PlaylistManager.open(dest_root)
    return PlaylistManager.init(source_root, dest_root)


def reset_workspace(dest_root: Path) -> None:
    from echolist.safe_write import SafeWriter
    workspace = SafeWriter(dest_root).root / "Playlists"
    if workspace.exists():
        shutil.rmtree(workspace)
        print(f"removed {workspace}")


def _ordered_srcs(mgr, pl: dict) -> list[str]:
    src_root = Path(mgr.config.source_root).resolve()
    ordered = sorted(pl["tracks"], key=lambda t: t.get("index", 0))
    return [str(src_root / (t.get("src_path") or "")) for t in ordered]


def _reorder_to(mgr, pid: str, want: list[Path]) -> None:
    """Rename store-track copy files and re-tag so they match `want` order exactly."""
    from echolist.naming import track_filename
    from echolist.tags import apply_playlist_tags

    pl = mgr.store.playlists[pid]
    src_root = Path(mgr.config.source_root).resolve()
    by_src = {str(src_root / (t.get("src_path") or "")): t for t in pl["tracks"]}
    pad = len(str(len(want)))
    plan = []
    for pos, p in enumerate(want, 1):
        t = by_src.get(str(p))
        if t is None:
            raise RuntimeError(f"reorder: no stored track for {p}")
        ext = Path(t["copy_name"]).suffix
        title = t["copy_name"].split(" - ", 1)[-1].rsplit(".", 1)[0]
        plan.append((t, pos, t["copy_name"], track_filename(pos, title, ext, pad)))

    folder = pl["folder"]
    # pass 1: every file that must change goes to a unique temp name
    for t, idx, old, new in plan:
        if old != new:
            tmp = f"_echolist_tmp_{idx}_{old}"
            try:
                mgr.writer.rename(f"{folder}/{old}", f"{folder}/{tmp}")
            except Exception:
                pass
    # pass 2: temp -> final name, update store + tags
    for t, idx, old, new in plan:
        src = f"_echolist_tmp_{idx}_{old}" if old != new else old
        if old != new:
            try:
                mgr.writer.rename(f"{folder}/{src}", f"{folder}/{new}")
            except Exception:
                new = old  # keep old name if the rename failed
        t["index"] = idx
        t["copy_name"] = new
        try:
            path = mgr.writer.resolve(f"{folder}/{new}")
            apply_playlist_tags(path, mgr.config.node_name,
                                mgr.config.album_prefix + pl["name"],
                                idx, t.get("src_path", ""), pid)
        except Exception:
            pass
    pl["tracks"] = [entry[0] for entry in plan]  # bring store list order in line
    mgr.store.save()


def sync_playlist(mgr, pid: str, name: str, want: list[Path], budget: int) -> dict:
    """Ensure `mgr`'s playlist `pid` contains exactly `want` tracks, in order.

    Incremental: keeps unchanged copies, adds missing ones, removes stale ones,
    then reorders so files match the playlist order on the card."""
    want_set = {str(p) for p in want}
    store_pid = mgr.store.playlists.get(pid)

    if store_pid is None:
        if len(want) > budget:
            return {"status": "over-limit",
                    "detail": f"needs {len(want)} tracks but only {budget} of {MAX_TRACKS} remain"}
        mgr.create_playlist(name)
        added = 0
        for pos, src in enumerate(want, 1):
            mgr.add_track(pid, src, total=len(want))
            added += 1
            if pos % 100 == 0 or pos == len(want):
                print(f"    [{name}] {pos}/{len(want)}")
        return {"status": "synced", "count": added}

    src_root = Path(mgr.config.source_root).resolve()
    existing = {str(src_root / (t.get("src_path") or "")): t for t in store_pid["tracks"]}
    existing_set = set(existing)

    if _ordered_srcs(mgr, store_pid) == [str(p) for p in want]:
        return {"status": "up-to-date", "count": len(existing_set)}

    adds = [p for p in want if str(p) not in existing_set]
    removes = [t for p, t in existing.items() if str(p) not in want_set]

    if len(adds) > budget:
        return {"status": "over-limit",
                "detail": f"needs {len(adds)} new tracks but only {budget} of {MAX_TRACKS} remain"}

    added = removed = 0
    for t in sorted(removes, key=lambda t: t["index"], reverse=True):
        mgr.remove_track(pid, t["index"])
        removed += 1
    for src in adds:
        mgr.add_track(pid, src, total=len(want))
        added += 1

    if _ordered_srcs(mgr, store_pid) != [str(p) for p in want]:
        _reorder_to(mgr, pid, want)

    print(f"    [{name}] +{added} -{removed} kept {len(existing_set) - removed}")
    return {"status": "reconciled", "count": len(want)}


def repad_card(dest_root: Path, source_root: Path) -> int:
    """Rename all tracks on the card to use correct zero-padding based on playlist length."""
    from echolist.naming import track_filename
    mgr = open_manager(dest_root, source_root)
    try:
        total_renamed = 0
        for pid, pl in mgr.store.playlists.items():
            tracks = pl["tracks"]
            if not tracks:
                continue
            pad = len(str(len(tracks)))
            folder = pl["folder"]
            renamed = 0
            for t in tracks:
                old_name = t["copy_name"]
                title = old_name.split(" - ", 1)[-1].rsplit(".", 1)[0]
                ext = Path(old_name).suffix
                new_name = track_filename(t["index"], title, ext, pad)
                if old_name != new_name:
                    src = dest_root / "Playlists" / folder / old_name
                    dst = dest_root / "Playlists" / folder / new_name
                    src.rename(dst)
                    t["copy_name"] = new_name
                    renamed += 1
            if renamed:
                print(f"  [{pl['name']}] renamed {renamed}/{len(tracks)} tracks")
                total_renamed += renamed
            else:
                print(f"  [{pl['name']}] already correctly padded ({len(tracks)} tracks)")
        mgr.store.save()
        mgr.save_snapshot()
        print(f"\ntotal renamed: {total_renamed}")
        return 0
    finally:
        mgr.release_lock()


def plan_sync(dest_root: Path, source_root: Path, playlist_dir: Path,
              selected: list[str], dry_run: bool, reset: bool) -> int:
    from echolist.manager import PlaylistManager

    if reset and not dry_run:
        reset_workspace(dest_root)

    workspace_config = dest_root / "Playlists" / ".echolist" / "config.json"
    mgr = None
    if workspace_config.exists() or not dry_run:
        mgr = open_manager(dest_root, source_root)

    try:
        # Existing card state
        existing_by_pid: dict[str, set[str]] = {}
        if mgr is not None:
            src_root = Path(mgr.config.source_root).resolve()
            for pid, pl in mgr.store.playlists.items():
                existing_by_pid[pid] = {str(src_root / (t.get("src_path") or ""))
                                        for t in pl["tracks"]}
        grand_total = sum(len(v) for v in existing_by_pid.values())
        from echolist.naming import playlist_id

        exit_code = 0
        synced = reconciled = up_to_date = skipped = 0
        for name in selected:
            pid = playlist_id(name)
            if dry_run:
                state = (len(existing_by_pid.get(pid, set())),
                         "exists" if pid in existing_by_pid else "new")
                print(f"- '{name}': {state} on card")
                continue
            want = load_selected_m3u(name, playlist_dir, source_root)
            budget = MAX_TRACKS - grand_total
            res = sync_playlist(mgr, pid, name, want, budget)
            if res["status"] == "synced":
                synced += res["count"]
                grand_total += res["count"]
            elif res["status"] == "reconciled":
                reconciled += 1
                grand_total = sum(len(p["tracks"]) for p in mgr.store.playlists.values())
            elif res["status"] == "up-to-date":
                up_to_date += 1
            else:
                skipped += 1
                print(f"- '{name}': {res['detail']}")
                exit_code = 1

        print(f"\nsummary: {synced} track(s) copied, {reconciled} reconciled, "
              f"{up_to_date} up-to-date, {skipped} skipped")
        print(f"card workspace total: {grand_total} / {MAX_TRACKS}")
        if not dry_run and exit_code == 0:
            mgr.save_snapshot()
            print("snapshot saved")
        return exit_code
    finally:
        if mgr is not None:
            mgr.release_lock()


def main() -> int:
    ap = argparse.ArgumentParser(description="Echo NANO sync pipeline")
    ap.add_argument("--list", action="store_true", help="list foobar playlists and exit")
    ap.add_argument("--playlists", default="Top Rated",
                    help="comma-separated playlist names to convert/sync "
                         "(use 'all' for every playlist except whole-library dupes)")
    ap.add_argument("--convert-only", action="store_true", help="only regenerate .m3u files")
    ap.add_argument("--sync-only", action="store_true", help="only sync to the SD card")
    ap.add_argument("--reset", action="store_true", help="wipe card workspace before syncing")
    ap.add_argument("--yes", action="store_true", help="confirm destructive --reset")
    ap.add_argument("--repad", action="store_true",
                    help="rename existing card tracks to correct zero-padded filenames and exit")
    ap.add_argument("--dry-run", action="store_true", help="print plans without writing")
    ap.add_argument("--profile", default=str(DEFAULT_PROFILE))
    ap.add_argument("--source-root", default=str(DEFAULT_SOURCE_ROOT))
    ap.add_argument("--playlist-dir", default=str(DEFAULT_PLAYLIST_DIR))
    ap.add_argument("--dest", default=str(DEFAULT_DEST))
    ap.add_argument("--echolist-src", default=str(DEFAULT_ECHOLIST_SRC))
    args = ap.parse_args()

    _add_echolist_to_path(Path(args.echolist_src))
    profile = Path(args.profile)
    source_root = Path(args.source_root)
    playlist_dir = Path(args.playlist_dir)
    dest_root = Path(args.dest)

    index = load_playlist_index(profile)
    all_names = [n for n in index.values() if n not in DUPES_OF_WHOLE_LIBRARY]

    if args.list:
        print(f"{'playlist':30} {'tracks':>7}")
        for name in all_names:
            guid = next(g for g, n in index.items() if n == name)
            fplite = get_fplite_path(profile, guid)
            count = -1
            if fplite.exists():
                count = len(parse_fplite(fplite, source_root)[0])
            print(f"{name:30} {count:>7}")
        return 0

    if args.repad:
        print(f"== repad: -> {dest_root} ==")
        return repad_card(dest_root, source_root)

    if args.playlists.lower() == "all":
        selected = all_names
    else:
        selected = [resolve_fplite_name(s.strip(), index)
                    for s in args.playlists.split(",") if s.strip()]

    exit_code = 0

    if not args.sync_only:
        print("== convert: fplite -> .m3u ==")
        for r in convert_playlists(profile, source_root, playlist_dir, selected, args.dry_run):
            if "error" in r:
                print(f"- '{r['name']}': ERROR {r['error']}")
                exit_code = 1
                continue
            status = "OK" if not r["missing"] else f"WARNING {len(r['missing'])} unresolved"
            print(f"- '{r['name']}': {r['tracks']} tracks -> {r['out']}  [{status}]")
            if r["missing"]:
                exit_code = 1

    if not args.convert_only:
        if not dest_root.exists():
            print(f"ERROR: destination not mounted: {dest_root}")
            return 1
        if args.reset and not args.dry_run and not args.yes:
            print("--reset requires --yes (it wipes dest/Playlists on the card)")
            return 2
        print(f"\n== sync: -> {dest_root} ==")
        exit_code = exit_code or plan_sync(dest_root, source_root, playlist_dir,
                                           selected, args.dry_run, args.reset)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())