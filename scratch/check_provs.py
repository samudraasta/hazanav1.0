import csv

provinces = set()
with open('/Users/samudra/Library/CloudStorage/OneDrive-ForumZakat/Downloads/Kurban OPZ/2026/data_fixed.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        provs = row.get('PROVINSI', '')
        if provs:
            for p in provs.split('\n'):
                p = p.strip().upper()
                if p:
                    provinces.add(p)

print(f"Total provinces mapped: {len(provinces)}")
print(sorted(provinces))
