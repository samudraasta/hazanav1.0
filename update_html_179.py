import json
import re

with open('mapping_179.json', 'r') as f:
    mapping_179 = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract existing fozLogos
match = re.search(r'const fozLogos\s*=\s*{(.*?)\n\s*};', html, re.DOTALL)
if not match:
    print("Could not find fozLogos")
    exit(1)

existing_block = match.group(1)
# we can safely just append the new keys to the existing block if they aren't already there
existing_keys = re.findall(r'"([^"]+)":', existing_block)

new_lines = []
for k, v in mapping_179.items():
    if k not in existing_keys:
        new_lines.append(f'            "{k}": "{v}"')

if new_lines:
    appended_block = existing_block + ",\n" + ",\n".join(new_lines)
    html = html.replace(existing_block, appended_block)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Added {len(new_lines)} new mappings.")
else:
    print("No new mappings to add.")
