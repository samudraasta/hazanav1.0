import urllib.request
import csv
import io

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQJta5FINk6bb9i9AQLnR2gVifQLd7fR5jb3WHtJonGiD-1VPIGX9IAr4nh856MYYYJ5eGGwaIpA2Ix/pub?gid=1395490505&single=true&output=csv'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    content = response.read().decode('utf-8')

reader = csv.reader(io.StringIO(content))
headers = next(reader)
for i, h in enumerate(headers):
    if 'Pertumbuhan' in h:
        print(f"Header {i}: {repr(h)}")
