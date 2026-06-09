import os
import re

# Read OPZ list
with open('scratch/user_opz_list.txt', 'r', encoding='utf-8') as f:
    opz_list = [line.strip() for line in f if line.strip()]

# Parse index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'const fozLogos = \{(.*?)\};', html, re.DOTALL)
if not match:
    print("fozLogos not found")
    exit()

obj_str = match.group(1)

mappings = {}
for line in obj_str.split('\n'):
    if ':' in line:
        parts = line.split(':', 1)
        key = parts[0].strip().strip('"').strip("'")
        val = parts[1].strip().strip(',').strip('"').strip("'")
        mappings[key.lower()] = val

rename_plan = {}
for opz in opz_list:
    lower_opz = opz.lower()
    # match by exact name or exact name without parenthesis
    found_old_file = None
    if lower_opz in mappings:
        found_old_file = mappings[lower_opz]
    else:
        no_paren = re.sub(r'\(.*?\)', '', lower_opz).strip()
        if no_paren in mappings:
            found_old_file = mappings[no_paren]

    if found_old_file:
        ext = os.path.splitext(found_old_file)[1]
        if not ext: ext = '.png'
        # If it's a weird extension like .png.jpeg, simplify
        if ext.lower() == '.jpeg' and found_old_file.endswith('.png.jpeg'):
            ext = '.jpg'
        
        safe_opz = opz.replace('/', '_').replace(':', '_').replace('"', '')
        new_file = f"logos/{safe_opz}{ext}"
        
        # Only add to plan if different
        if found_old_file != new_file:
            # We must be careful if two OPZ map to the SAME old file
            # e.g. "Griya Yatim dan Dhuafa (GYD)" and "LAZNAS Rumah Yatim Ar-Rohman" both use "Rumah Yatim.png"
            # If so, the first one gets the rename, the second one might fail or we should copy it.
            # Let's just do a simple copy instead of rename so we don't break shared logos.
            rename_plan[opz] = (found_old_file, new_file)

import shutil

new_html = html
for opz, (old_file, new_file) in rename_plan.items():
    if os.path.exists(old_file):
        if not os.path.exists(new_file):
            shutil.copy2(old_file, new_file)
            print(f"Copied {old_file} -> {new_file}")
    else:
        print(f"File not found: {old_file}")
    
    # We need to update ONLY the keys that correspond to this OPZ
    # To be safe, we will find the specific line for this OPZ in the HTML and replace it.
    
    # regex to find the line: "OPZ Name": "old_file",
    opz_pattern = re.escape(opz)
    old_file_pattern = re.escape(old_file)
    
    # We replace: "OPZ Name": "old_file" with "OPZ Name": "new_file"
    pattern = rf'("{opz_pattern}":\s*"){old_file_pattern}(")'
    new_html, count = re.subn(pattern, rf'\1{new_file}\2', new_html, flags=re.IGNORECASE)
    
    if count == 0:
        # try without parenthesis
        no_paren = re.sub(r'\(.*?\)', '', opz).strip()
        no_paren_pattern = re.escape(no_paren)
        pattern = rf'("{no_paren_pattern}":\s*"){old_file_pattern}(")'
        new_html, count = re.subn(pattern, rf'\1{new_file}\2', new_html, flags=re.IGNORECASE)
        

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated index.html")
