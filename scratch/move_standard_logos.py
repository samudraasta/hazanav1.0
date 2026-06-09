import os
import re
import shutil

html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
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
        mappings[key] = val

os.makedirs('logos_standard', exist_ok=True)

unique_files = set(mappings.values())
new_html = html
moved_files = set()

for old_val in unique_files:
    if old_val.startswith('logos/'):
        filename = old_val[len('logos/'):]
        old_path = old_val
        new_path = f"logos_standard/{filename}"
        
        if os.path.exists(old_path):
            if old_path not in moved_files:
                # We move the file instead of copy so it truly cleans up the old folder
                # Wait, some might be original files that just happened to be standard.
                # To be absolutely safe and not destroy originals, let's copy first, 
                # but the user said "dimasukkan ke 1 folder", so they want them isolated.
                # We will copy them to logos_standard. If they want to delete the rest later, they can.
                shutil.copy2(old_path, new_path)
                moved_files.add(old_path)
            
            # replace in HTML exactly
            pattern = rf'"{re.escape(old_val)}"'
            new_html = re.sub(pattern, f'"{new_path}"', new_html)
        else:
            print(f"Warning: {old_path} not found")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Copied {len(moved_files)} referenced logos to logos_standard/ and updated index.html")
