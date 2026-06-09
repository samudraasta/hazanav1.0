import re
import csv

missing = [
"ALZIS Alwashliyah",
"Baitul Maal Timoho Sejahtera",
"Goedang Zakat Al- Khairaat",
"Indonesia Beramal Sholeh (IBS)",
"Indonesia Berbagi",
"LAZ As-Salam Timika",
"LAZ Assyifa Peduli",
"LAZ Darul Hikam",
"LAZ Generasi Rabbani",
"LAZ Hidayah Berbagi Indonesia",
"LAZ IBNU SINA",
"LAZ KESEJAHTERAAN UMAT",
"LAZ Pundi Surga",
"LAZIS Khoiru Ummah",
"Lazisnur",
"Sahabat Asnaf Indonesia"
]

with open('foz.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all img src
urls = re.findall(r'src="(https://forumzakat\.org/wp-content/uploads/[^"]+)"', html)
basenames = [u.split('/')[-1].lower() for u in urls]
url_map = dict(zip(basenames, urls))

for m in missing:
    terms = re.split(r'\s+', m.lower())
    found = False
    for t in terms:
        if len(t) < 4: continue
        if t in ['lazis', 'baitul', 'maal', 'zakat', 'indonesia', 'sahabat', 'peduli', 'berbagi', 'yayasan']: continue
        
        for bn, url in url_map.items():
            if t in bn:
                print(f"Match for {m}: {url}")
                found = True
                break
        if found: break
    if not found:
        print(f"No match for {m}")
