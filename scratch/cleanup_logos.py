import os
import re

# Read the artifact markdown table to get the exact canonical filenames
valid_files = set()
with open('scratch/opz_logos_table.md', 'r', encoding='utf-8') as f:
    for line in f:
        if '|' in line and 'Nama Lembaga OPZ' not in line and '---' not in line:
            parts = line.split('|')
            if len(parts) >= 3:
                file_part = parts[2].strip()
                # file_part looks like: `FileName.png` or ❌ *Tidak ada logo*
                if '❌' not in file_part:
                    # extract filename inside backticks
                    match = re.search(r'`(.*?)`', file_part)
                    if match:
                        valid_files.add(match.group(1))

# Check logos_standard folder
folder = 'logos_standard'
deleted_count = 0
retained_count = 0

for filename in os.listdir(folder):
    if filename == '.DS_Store':
        continue
        
    filepath = os.path.join(folder, filename)
    if os.path.isfile(filepath):
        if filename not in valid_files:
            os.remove(filepath)
            deleted_count += 1
        else:
            retained_count += 1

print(f"Retained {retained_count} logos.")
print(f"Deleted {deleted_count} unused logos.")
