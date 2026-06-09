import csv
import collections
import re

with open('scratch/data_online.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    countries = collections.Counter()
    for row in reader:
        col = row.get('8. Negara Penyaluran Kurban di Luar Negeri', '')
        if col:
            # simple split by comma, newline or 'dan'
            parts = re.split(r',|\n| dan | & |;', col)
            for p in parts:
                p = p.strip()
                if p:
                    countries[p] += 1
    
    for c, count in countries.most_common():
        print(f"{count}: {c}")
