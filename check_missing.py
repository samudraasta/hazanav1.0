import csv
import re

# Read data.csv and get unique Lembaga
unique_lembagas = set()
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        lembaga = row['Lembaga Anda'].strip()
        unique_lembagas.add(lembaga)

# Read index.html and extract keys from fozLogos
foz_logos_keys = set()
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
    match = re.search(r'const fozLogos\s*=\s*{(.*?)\n\s*};', html, re.DOTALL)
    if match:
        obj_str = match.group(1)
        # Extract keys (e.g. "Dompet Dhuafa": ...)
        keys = re.findall(r'"([^"]+)":', obj_str)
        foz_logos_keys.update(keys)

# Identify missing
missing = []
for l in unique_lembagas:
    # check if exact match (case insensitive) exists in fozLogos
    if not any(k.lower() == l.lower() for k in foz_logos_keys):
        missing.append(l)

print("Total missing:", len(missing))
for m in sorted(missing):
    print("-", m)
