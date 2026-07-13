#!/usr/bin/env python3
import hashlib
import argparse
import fnmatch
import sys
from pathlib import Path

def calculate_sha256(file_path, show_progress=False):
    """Calculates the SHA-256 hash of a file, optionally showing a live progress bar."""
    file_size = file_path.stat().st_size
    sha256_hash = hashlib.sha256()
    bytes_read = 0
    
    # Truncate filename for progress display to avoid terminal wrapping issues
    display_name = file_path.name if len(file_path.name) <= 40 else file_path.name[:37] + "..."
    
    # Read in 64KB chunks for faster processing of large files
    with open(file_path, "rb") as f:
        while True:
            byte_block = f.read(65536)  
            if not byte_block:
                break
            sha256_hash.update(byte_block)
            bytes_read += len(byte_block)
            
            if show_progress and file_size > 0:
                percent = (bytes_read / file_size) * 100
                # \r returns the cursor to the start of the line to update in place
                sys.stdout.write(f"\r  Progress: {percent:5.1f}% | {display_name}")
                sys.stdout.flush()
                
    if show_progress:
        # Clear the progress line so the final status message prints cleanly
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()
        
    return sha256_hash.hexdigest()

def main():
    # --- Argument Parsing for Wildcards ---
    parser = argparse.ArgumentParser(description="Create and verify SHA-256 checksums.")
    parser.add_argument(
        'patterns', 
        nargs='*', 
        default=['*'], 
        help='Wildcard patterns to match files (e.g., "*.rar"). Default is "*" (all files).'
    )
    args = parser.parse_args()
    
    current_dir = Path('.')
    checksum_ext = '.sha256'
    
    # Filter files based on the provided wildcard patterns
    files_to_process = [
        f for f in current_dir.iterdir()
        if f.is_file() 
        and not f.name.endswith(checksum_ext)
        and any(fnmatch.fnmatch(f.name, p) for p in args.patterns)
    ]
    
    if not files_to_process:
        print("No files found matching the specified pattern(s).")
        return

    print(f"Found {len(files_to_process)} file(s) to process.\n")

    for file_path in files_to_process:
        checksum_path = file_path.parent / (file_path.name + checksum_ext)
        
        if not checksum_path.exists():
            # --- CASE 1: CREATE ---
            print(f"Creating checksum for: {file_path.name}")
            try:
                file_hash = calculate_sha256(file_path, show_progress=True)
                
                with open(checksum_path, 'w') as cf:
                    cf.write(f"{file_hash}  {file_path.name}\n")
                    
                print(f"[CREATED] {checksum_path.name}")
                
            except PermissionError:
                print(f"[ERROR] Permission denied: {file_path.name}")
            except Exception as e:
                print(f"[ERROR] Failed to create checksum for {file_path.name}: {e}")
                
        else:
            # --- CASE 2: VERIFY ---
            print(f"Verifying checksum for: {file_path.name}")
            try:
                with open(checksum_path, 'r') as cf:
                    first_line = cf.readline().strip()
                    stored_hash = first_line.split()[0] 
                
                actual_hash = calculate_sha256(file_path, show_progress=True)
                
                if actual_hash == stored_hash:
                    print(f"[OK]       {file_path.name} matches its checksum.")
                else:
                    print(f"[FAILED]   {file_path.name} has been modified!")
                    print(f"           Expected: {stored_hash}")
                    print(f"           Actual:   {actual_hash}")
                    
            except IndexError:
                print(f"[ERROR] Checksum file {checksum_path.name} is empty or malformed.")
            except PermissionError:
                print(f"[ERROR] Permission denied reading {file_path.name} or {checksum_path.name}")
            except Exception as e:
                print(f"[ERROR] Failed to verify {file_path.name}: {e}")
        
        print("-" * 60) # Separator for readability

if __name__ == '__main__':
    main()
