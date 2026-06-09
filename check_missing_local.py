import csv
import re

# Get all unique OPZ names from CSV
opz_names = set()
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Lembaga Anda', '').strip()
        if name:
            opz_names.add(name)

# Extract mapped names from index.html
mapped_names = set()
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
    match = re.search(r'const fozLogos\s*=\s*{(.*?)\n\s*};', html, re.DOTALL)
    if match:
        obj_str = match.group(1)
        # Find keys
        keys = re.findall(r'"([^"]+)":', obj_str)
        mapped_names.update(keys)

missing = []
for opz in opz_names:
    if opz not in mapped_names:
        missing.append(opz)

print("Still Missing:", len(missing))
for m in sorted(missing):
    print("-", m)
