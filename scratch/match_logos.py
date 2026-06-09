import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'const fozLogos = \{(.*?)\};', html, re.DOTALL)
foz_logos = {}
if match:
    obj_str = match.group(1)
    for line in obj_str.split('\n'):
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip().strip('"').strip("'")
            val = parts[1].strip().strip(',').strip('"').strip("'")
            foz_logos[key.lower()] = val

with open('scratch/user_opz_list.txt', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

with open('scratch/opz_logos_table.md', 'w', encoding='utf-8') as f:
    f.write('| Nama Lembaga OPZ | File Logo |\n')
    f.write('| --- | --- |\n')
    for line in lines:
        lower_line = line.lower()
        if lower_line in foz_logos:
            logo = foz_logos[lower_line]
            logo_name = logo.replace('logos/', '')
            f.write(f'| {line} | `{logo_name}` |\n')
        else:
            # Let's check if the name without parenthesis is there
            no_paren = re.sub(r'\(.*?\)', '', lower_line).strip()
            if no_paren in foz_logos:
                logo = foz_logos[no_paren]
                logo_name = logo.replace('logos/', '')
                f.write(f'| {line} | `{logo_name}` |\n')
            else:
                f.write(f'| {line} | ❌ *Tidak ada logo* |\n')
