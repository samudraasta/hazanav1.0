import os
import hashlib
from collections import defaultdict

folder = 'logos_standard'
hashes = defaultdict(list)

for filename in os.listdir(folder):
    if filename.endswith('.png'):
        filepath = os.path.join(folder, filename)
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        hashes[file_hash].append(filename)

# Filter for duplicates
duplicates = {k: v for k, v in hashes.items() if len(v) > 1}

if not duplicates:
    print("Tidak ada gambar duplikat.")
else:
    print("Ditemukan gambar kembar:")
    for file_hash, files in duplicates.items():
        print(f"\nHash: {file_hash}")
        for f in files:
            print(f" - {f}")
