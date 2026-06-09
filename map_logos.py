import os
import csv
import json
import re

logos_dir = 'logos'
csv_file = 'data.csv'

# 1. Get all OPZ names from CSV
opz_names = set()
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Lembaga Anda', '').strip()
        if name:
            opz_names.add(name)

# 2. Get all logo files
logo_files = os.listdir(logos_dir)

# Helper function for matching
def simplify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '', text)
    # common prefixes to strip for matching
    text = re.sub(r'^(laz|laznas|lazis|yayasan|baitul|maal|lembaga|amil|zakat|infaq|sedekah|shodaqoh|rumah)', '', text)
    text = re.sub(r'(indonesia|nasional|daerah|provinsi|kabupaten|kota|pusat)$', '', text)
    return text

mapping = {}
unmatched = []

for opz in sorted(opz_names):
    match = None
    opz_clean = simplify(opz)
    
    # direct exact match
    for lf in logo_files:
        lf_name = os.path.splitext(lf)[0]
        # try exact without extension
        if opz.lower() == lf_name.lower():
            match = lf
            break
        # try exact with common words stripped
        if simplify(opz) == simplify(lf_name) and simplify(opz) != '':
            match = lf
            break

    # substring match
    if not match:
        for lf in logo_files:
            lf_name = os.path.splitext(lf)[0]
            if len(opz_clean) > 4 and opz_clean in simplify(lf_name):
                match = lf
                break
            if len(simplify(lf_name)) > 4 and simplify(lf_name) in opz_clean:
                match = lf
                break
                
    # manual fallbacks
    if not match:
        if "alwashliyah" in opz.lower():
            for lf in logo_files:
                if "alwashliyah" in lf.lower(): match = lf; break
        if "agnia" in opz.lower():
            for lf in logo_files:
                if "agnia" in lf.lower(): match = lf; break
        if "ikadi" in opz.lower():
            for lf in logo_files:
                if "ikadi" in lf.lower(): match = lf; break
        if "yatim mandiri" in opz.lower():
            for lf in logo_files:
                if "yatim mandiri" in lf.lower(): match = lf; break
                
    if match:
        mapping[opz] = "logos/" + match
    else:
        unmatched.append(opz)

print(f"Mapped {len(mapping)} OPZ logos. Unmatched: {len(unmatched)}")
for u in unmatched:
    print("-", u)

with open('mapping_local.json', 'w') as f:
    json.dump(mapping, f, indent=2)

