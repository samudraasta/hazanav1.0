import os
import json
import csv
from difflib import get_close_matches
import re

# 1. Read OPZ list from data_fixed.csv
opz_names = set()
with open('data_fixed.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) > 1 and row[1].strip():
            opz_names.add(row[1].strip())

# 2. List all files in logos_standard
logo_files = os.listdir('logos_standard')
logo_files = [f for f in logo_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg'))]

# Create a clean mapping dictionary for fuzzy matching
clean_to_file = {}
for f in logo_files:
    clean_name = re.sub(r'[^a-z0-9]', '', f.split('.')[0].lower())
    clean_to_file[clean_name] = f
    
    # Also index by replacing spaces
    clean_name2 = f.split('.')[0].lower().strip()
    clean_to_file[clean_name2] = f

mapping = {}
unmapped = []

for name in opz_names:
    clean_name = re.sub(r'[^a-z0-9]', '', name.lower())
    clean_name2 = name.lower().strip()
    
    # Exact match first
    if f"{name}.png" in logo_files:
        mapping[name] = f"{name}.png"
        continue
    if f"{name}.jpg" in logo_files:
        mapping[name] = f"{name}.jpg"
        continue
        
    if clean_name in clean_to_file:
        mapping[name] = clean_to_file[clean_name]
        continue
        
    if clean_name2 in clean_to_file:
        mapping[name] = clean_to_file[clean_name2]
        continue
        
    # Fuzzy match
    all_clean_keys = list(clean_to_file.keys())
    matches = get_close_matches(clean_name, all_clean_keys, n=1, cutoff=0.7)
    if matches:
        mapping[name] = clean_to_file[matches[0]]
        continue
        
    matches2 = get_close_matches(clean_name2, all_clean_keys, n=1, cutoff=0.7)
    if matches2:
        mapping[name] = clean_to_file[matches2[0]]
        continue
        
    unmapped.append(name)

with open('standard_logo_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2)

print(f"Mapped {len(mapping)} logos.")
print(f"Unmapped: {len(unmapped)}")
print(unmapped)
