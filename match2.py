import csv
import re
import json

urls = set()
with open('all_urls.txt', 'r', encoding='utf-8') as f:
    for line in f:
        urls.add(line.strip())

url_map = {}
for u in urls:
    basename = u.split('/')[-1].replace('-100x57', '').replace('.png', '').lower()
    basename = re.sub(r'^\d+\.-', '', basename)
    basename = basename.replace('-', ' ')
    url_map[u] = basename

opz_names = set()
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Nama OPZ') and row['Nama OPZ'].strip():
            opz_names.add(row['Nama OPZ'].strip())

def simplify(name):
    words_to_remove = ['laznas', 'lazis', 'laz', 'yayasan', 'foundation', 'pusat', 'nasional', 'daerah', 'kabupaten', 'kota', 'provinsi']
    name = name.lower()
    for w in words_to_remove:
        name = re.sub(r'\b' + w + r'\b', '', name)
    
    acronym = re.search(r'\((.*?)\)', name)
    if acronym:
        return acronym.group(1).strip()
    return name.strip()

mapping = {}
for opz in opz_names:
    keyword = simplify(opz)
    best_u = None
    
    for u, basename in url_map.items():
        if keyword and keyword in basename:
            best_u = u
            break
        if basename and basename in keyword and len(basename) >= 3:
            best_u = u
            break
            
    if best_u:
        mapping[opz] = best_u

print(json.dumps(mapping, indent=2))
