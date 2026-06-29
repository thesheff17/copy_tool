#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

# do you want to log info to a json file
# by default this is on
JSON_LOG = True

# display google timer link
# by default this is off
GOOGLE_TIMER_LINK = False

def append_to_json_file(data, filename):
    # 1. Initialize an empty list if the file doesn't exist or is empty
    file_data = []
    
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                # Handle the case where the file has corrupted/invalid JSON
                print(f"Warning: {filename} contained invalid JSON. Overwriting.")
                file_data = []

    # 2. Append your new data (assumes the root of your JSON is a list)
    if isinstance(file_data, list):
        file_data.append(data)
    else:
        # If the file exists but root is a dict, convert it or handle accordingly
        file_data = [file_data, data]

    # 3. Write the entire updated list back to the file
    with open(filename, "w") as file:
        json.dump(file_data, file, indent=4)

def copy_with_progress(source_dir, dest_dir):
    if source_dir.endswith("/"):
        source_dir = source_dir[0:-1]

    if dest_dir.endswith("/"):
        dest_dir = dest_dir[0:-1]

    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    if not source_path.exists():
        print(f"error: source directory '{source_dir}' does not exist.")
        sys.exit(1)

    if not dest_path.exists():
        print(f"error: dest directory '{dest_dir}' does not exist.")
        sys.exit(1)
    print ("copy_tool.py started...")
    print("scanning source directory and calculating total size of files. please wait...")
    files_to_copy = []
    total_size = 0

    for root, dirs, files in os.walk(source_path):
        for file in files:
            src_file = Path(root) / file
            rel_path = src_file.relative_to(source_path)
            dst_file = dest_path / rel_path
            
            file_size = src_file.stat().st_size
            files_to_copy.append((src_file, dst_file, file_size))
            total_size += file_size

    total_files = len(files_to_copy)
    print(f"Found {total_files:,} files to copy ({total_size / (1024**2):,.2f} MB).\n")

    if total_files == 0:
        print("nothing to copy.")
        return

    bytes_copied = 0
    files_copied = 0
    link_printed = False  # Track if the timer link has been displayed
    script_start_time = time.time()  # Captures the start of the copy process

    for src_f, dst_f, f_size in files_to_copy:
        try:
            # Recreate directory structure
            dst_f.parent.mkdir(parents=True, exist_ok=True)
            
            # Format and truncate filename for display
            current_file_name = src_f.name
            if len(current_file_name) > 20:
                current_file_name = current_file_name[:17] + "..."

            # Track stats
            files_copied += 1
            files_remaining = total_files - files_copied
            
            # Calculations
            percentage = (bytes_copied / total_size) * 100 if total_size > 0 else 100
            elapsed_time = time.time() - script_start_time
            
            # ETA based on processing time per file
            if files_copied > 0:
                time_per_file = elapsed_time / files_copied
                eta_seconds = files_remaining * time_per_file
                eta_minutes, eta_seconds = divmod(int(eta_seconds), 60)
                eta_str = f"{eta_minutes:02d}M:{eta_seconds:02d}S"
            else:
                eta_str = "--:--"


            if GOOGLE_TIMER_LINK:
                # Print Google Timer link once after crossing 10% completion
                if percentage >= 10.0 and not link_printed:
                    
                    # adding + 5 min
                    timer_total_min = int(eta_minutes) + 5
                    
                    # Create a URL-safe query string for Google
                    google_url = f"https://www.google.com/search?q=timer+for+{timer_total_min}+minutes"
                    
                    # Printing a newline breaks the overwrite cycle cleanly so the link stays visible
                    print(f"\n\n[10% completed] timer link:\n{google_url}\n")
                    link_printed = True

            # what you see on the terminal
            status_line = (
                f"\rcopying file: {current_file_name:<20} | "
                f"{percentage:.1f}% | "
                f"copied: {files_copied:,}/{total_files:,} ({files_remaining:,} file(s) left) | "
                f"estimated time remaining: {eta_str}\033[K"
            )
            sys.stdout.write(status_line)
            sys.stdout.flush()

            # Execute copy operation
            shutil.copy2(src_f, dst_f)
            bytes_copied += f_size
            
        except Exception as e:
            print(f"\nError copying {src_f}: {e}")

    # Calculate final elapsed time execution after copy
    total_elapsed_time = time.time() - script_start_time

    # Calculate average throughput in MB/s
    if total_elapsed_time > 0:
        total_size_mb = total_size / (1024**2)
        speed_mb_s = total_size_mb / total_elapsed_time
    else:
        speed_mb_s = 0.0
    
    # Break down total seconds into days, hours, minutes, and seconds
    days, remainder = divmod(int(total_elapsed_time), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Dynamically build the output string so it looks clean (e.g., skips "0d 0h" if short)
    time_parts = []
    if days > 0:
        time_parts.append(f"{days} day(s)")
    if hours > 0 or days > 0:
        time_parts.append(f"{hours} hour(s)")
    if minutes > 0 or hours > 0 or days > 0:
        time_parts.append(f"{minutes} minute(s)")
    time_parts.append(f"{seconds} second(s)")
    
    time_str = " ".join(time_parts)

    print(f"\n\ncopy_tool.py completed. copied: {files_copied:,} out of {total_files:,} files in {time_str} copy speed: {speed_mb_s:.2f} MB/s.")

    if JSON_LOG:
        # Generate and write JSON log
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "src_directory": str(source_path.resolve()),
            "dest_directory": str(dest_path.resolve()),
            "total_files_copied": files_copied,
            "total_size_mb": round(total_size_mb, 2),
            "final_speed_mb_s": round(speed_mb_s, 2),
            "total_time_seconds": round(total_elapsed_time, 2)
        }
        append_to_json_file(log_data, "copy_tool.json")

def main():
    parser = argparse.ArgumentParser(
        description="copy files from A to B with estimated elasped time."
    )
    parser.add_argument(
        "source", 
        type=str, 
        help="The path to the source directory you want to copy files from."
    )
    parser.add_argument(
        "destination", 
        type=str, 
        help="The destination directory to copy files to."
    )

    args = parser.parse_args()
    copy_with_progress(args.source, args.destination)


if __name__ == "__main__":
    main()