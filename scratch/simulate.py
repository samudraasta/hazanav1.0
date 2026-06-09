import urllib.request
import csv
import io
import re

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQJta5FINk6bb9i9AQLnR2gVifQLd7fR5jb3WHtJonGiD-1VPIGX9IAr4nh856MYYYJ5eGGwaIpA2Ix/pub?gid=1395490505&single=true&output=csv"
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
except Exception as e:
    import ssl
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, context=context) as response:
         content = response.read().decode('utf-8')

reader = csv.DictReader(io.StringIO(content))
for row in reader:
    growth_key = None
    for k in row.keys():
        if k and 'pertumbuhan' in k.lower() and 'nilai' not in k.lower():
            growth_key = k
            break
    
    raw_grow = row.get(growth_key, '') if growth_key else ''
    if not raw_grow:
        raw_grow = '0'
        
    growth_str = raw_grow.replace('%', '').replace(',', '.').strip()
    try:
        growth = float(growth_str)
    except:
        growth = 0
        
    name = row.get('Nama LAZ / BAZ', '')
    if 'Dompet Dhuafa' in name or 'Rumah Zakat' in name:
        print(f"Name: {name}, raw_grow: {repr(raw_grow)}, growthStr: {repr(growth_str)}, growth: {growth}")
