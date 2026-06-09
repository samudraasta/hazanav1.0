import csv

file_path = '/Users/samudra/.gemini/antigravity/brain/82723891-e9fc-454a-82d4-77c267cd0cf8/.system_generated/steps/674/content.md'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = 0
for i, line in enumerate(lines):
    if line.startswith('Timestamp'):
        start_idx = i
        break

csv_lines = lines[start_idx:]
reader = csv.reader(csv_lines)
headers = next(reader)
print("Headers:")
for i, h in enumerate(headers):
    print(f"{i}: {repr(h)}")

row = next(reader)
print("\nRow:")
for i, d in enumerate(row):
    print(f"{i}: {repr(d)}")
