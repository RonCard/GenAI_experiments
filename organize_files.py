#!/usr/bin/env python3
“””
File Organizer
Scans a directory and moves files into subfolders based on their file type/extension.
“””

import os
import shutil
import argparse
from pathlib import Path
from collections import defaultdict

def organize_files(target_dir: str, dry_run: bool = False) -> None:
target_path = Path(target_dir).resolve()

```
if not target_path.exists():
    print(f"Error: Directory '{target_path}' does not exist.")
    return
if not target_path.is_dir():
    print(f"Error: '{target_path}' is not a directory.")
    return

files = [f for f in target_path.iterdir() if f.is_file()]

if not files:
    print("No files found in the directory.")
    return

moved = defaultdict(list)
skipped = []

for file in files:
    # Skip this script itself if it lives in the same directory
    if file.name == Path(__file__).name:
        skipped.append(file.name)
        continue

    extension = file.suffix.lstrip(".").lower()
    folder_name = extension if extension else "no_extension"
    dest_folder = target_path / folder_name

    if dry_run:
        print(f"[DRY RUN] Would move: {file.name}  →  {folder_name}/")
        moved[folder_name].append(file.name)
        continue

    dest_folder.mkdir(exist_ok=True)
    dest_file = dest_folder / file.name

    # Avoid overwriting: append a counter if a file with the same name exists
    counter = 1
    while dest_file.exists():
        stem = file.stem
        dest_file = dest_folder / f"{stem}_{counter}{file.suffix}"
        counter += 1

    shutil.move(str(file), str(dest_file))
    moved[folder_name].append(dest_file.name)

# ── Summary ────────────────────────────────────────────────────────────────
print(f"\n{'[DRY RUN] ' if dry_run else ''}Results for: {target_path}\n")
print(f"  {'Files that would be moved' if dry_run else 'Files moved'}: "
      f"{sum(len(v) for v in moved.values())}")
print(f"  Folders {'to be ' if dry_run else ''}created/used: {len(moved)}")

if moved:
    print("\n  Breakdown by folder:")
    for folder, names in sorted(moved.items()):
        print(f"    📁 {folder}/  ({len(names)} file{'s' if len(names) != 1 else ''})")
        for name in names:
            print(f"       • {name}")

if skipped:
    print(f"\n  Skipped (this script): {', '.join(skipped)}")

if not dry_run:
    print("\nDone! ✓")
```

def main():
parser = argparse.ArgumentParser(
description=“Organize files in a directory into subfolders by file type.”
)
parser.add_argument(
“directory”,
nargs=”?”,
default=”.”,
help=“Path to the directory to organize (default: current directory)”
)
parser.add_argument(
“–dry-run”,
action=“store_true”,
help=“Preview changes without moving any files”
)

```
args = parser.parse_args()
organize_files(args.directory, dry_run=args.dry_run)
```

if **name** == “**main**”:
main()
