import os
import re
import json

with open('opz_list.txt', 'r', encoding='utf-8') as f:
    opz_list = [line.strip() for line in f if line.strip()]

logo_files = os.listdir('logos')

# Helper function
def simplify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '', text)
    text = re.sub(r'^(laz|laznas|lazis|yayasan|baitul|maal|lembaga|amil|zakat|infaq|sedekah|shodaqoh|rumah)', '', text)
    text = re.sub(r'(indonesia|nasional|daerah|provinsi|kabupaten|kota|pusat)$', '', text)
    return text

mapping = {}
unmatched = []

for opz in sorted(opz_list):
    match = None
    opz_clean = simplify(opz)
    
    # 1. exact match
    for lf in logo_files:
        lf_name = os.path.splitext(lf)[0]
        if opz.lower() == lf_name.lower():
            match = lf
            break
        if simplify(opz) == simplify(lf_name) and simplify(opz) != '':
            match = lf
            break

    # 2. substring match
    if not match:
        for lf in logo_files:
            lf_name = os.path.splitext(lf)[0]
            if len(opz_clean) > 4 and opz_clean in simplify(lf_name):
                match = lf
                break
            if len(simplify(lf_name)) > 4 and simplify(lf_name) in opz_clean:
                match = lf
                break
                
    if match:
        mapping[opz] = "logos/" + match
    else:
        unmatched.append(opz)

print(f"Matched {len(mapping)} out of {len(opz_list)}")
with open('mapping_179.json', 'w') as f:
    json.dump(mapping, f, indent=2)

with open('missing_179.txt', 'w') as f:
    for u in unmatched:
        f.write(u + "\n")
