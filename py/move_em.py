#!/usr/bin/env python3
import hashlib
import argparse
import sys
import shutil
from pathlib import Path

def calculate_sha256(file_path, show_progress=False):
    """Calculates the SHA-256 hash of a file, optionally showing a live progress bar."""
    file_size = file_path.stat().st_size
    sha256_hash = hashlib.sha256()
    bytes_read = 0
    
    display_name = file_path.name if len(file_path.name) <= 40 else file_path.name[:37] + "..."
    
    with open(file_path, "rb") as f:
        while True:
            byte_block = f.read(65536)  
            if not byte_block:
                break
            sha256_hash.update(byte_block)
            bytes_read += len(byte_block)
            
            if show_progress and file_size > 0:
                percent = (bytes_read / file_size) * 100
                sys.stdout.write(f"\r  Progress: {percent:5.1f}% | {display_name}")
                sys.stdout.flush()
                
    if show_progress:
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()
        
    return sha256_hash.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Safely move files with verified checksums.")
    parser.add_argument('source', help='The source directory containing the files and .sha256 files.')
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    dest_dir = Path.cwd()

    # --- Safety Checks ---
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"[ERROR] Source path '{source_dir}' does not exist or is not a directory.")
        sys.exit(1)

    if source_dir == dest_dir:
        print("[ERROR] Source and destination directories are the same. Aborting.")
        sys.exit(1)

    # Find files that have a corresponding .sha256 file
    files_to_process = []
    for f in source_dir.iterdir():
        if f.is_file() and not f.name.endswith('.sha256'):
            checksum_file = f.parent / (f.name + '.sha256')
            if checksum_file.exists():
                files_to_process.append(f)

    if not files_to_process:
        print("No files with corresponding .sha256 checksums found in the source directory.")
        return

    print(f"Found {len(files_to_process)} file(s) with checksums to process.\n")
    
    moved_count = 0
    skipped_count = 0
    failed_count = 0

    for src_file in files_to_process:
        dest_file = dest_dir / src_file.name
        src_checksum = src_file.parent / (src_file.name + '.sha256')
        dest_checksum = dest_dir / src_checksum.name

        print(f"Processing: {src_file.name}")

        # 1. Check for destination collisions
        if dest_file.exists():
            print(f"[SKIP] A file named '{dest_file.name}' already exists in the destination. Skipping to prevent overwrite.")
            skipped_count += 1
            print("-" * 60)
            continue

        # 2. Read the expected hash from the source checksum file
        try:
            with open(src_checksum, 'r') as cf:
                expected_hash = cf.readline().strip().split()[0]
        except Exception as e:
            print(f"[ERROR] Could not read checksum file {src_checksum.name}: {e}")
            failed_count += 1
            print("-" * 60)
            continue

        # 3. Copy the file to the destination
        try:
            # copy2 preserves metadata like timestamps
            shutil.copy2(src_file, dest_file)
        except Exception as e:
            print(f"[ERROR] Failed to copy file: {e}")
            failed_count += 1
            print("-" * 60)
            continue

        # 4. Verify the copied file
        print("Verifying copied file...")
        try:
            actual_hash = calculate_sha256(dest_file, show_progress=True)
        except Exception as e:
            print(f"[ERROR] Failed to calculate hash of copied file: {e}")
            dest_file.unlink() # Clean up the bad copy
            failed_count += 1
            print("-" * 60)
            continue

        # 5. Compare and act
        if actual_hash == expected_hash:
            print(f"[OK] Checksum verified successfully!")
            
            # Move the checksum file to the destination so the record is preserved
            shutil.move(src_checksum, dest_checksum)
            
            # Remove the original file from the source
            src_file.unlink()
            
            print(f"         Moved to: {dest_dir}")
            moved_count += 1
        else:
            print(f"[FAILED] Checksum mismatch! The copied file is corrupted.")
            print(f"         Expected: {expected_hash}")
            print(f"         Actual:   {actual_hash}")
            print(f"         Source files left intact. Cleaning up failed copy...")
            
            # Clean up the failed copy in the destination
            dest_file.unlink()
            failed_count += 1
            
        print("-" * 60)

    # --- Summary ---
    print("\n=== SUMMARY ===")
    print(f"Successfully moved: {moved_count}")
    print(f"Skipped (already exists): {skipped_count}")
    print(f"Failed (mismatch or error): {failed_count}")

if __name__ == '__main__':
    main()
