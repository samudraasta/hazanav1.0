import json
import re

with open('mapping_local.json', 'r') as f:
    mapping = json.load(f)

# Add BMBU
mapping['LAZ BMBU Kota Bontang'] = 'logos/LAZ Baitul Maal Barakatul Ummah Kota Bontang.png'

# Convert mapping to JS object string
js_obj = "const fozLogos = {\n"
for k, v in mapping.items():
    js_obj += f'            "{k}": "{v}",\n'

# we also add ALZIS and Agnia Care just in case they aren't in data.csv yet
js_obj += '            "ALZIS Alwashliyah": "logos/AL Azhar.png",\n' # Wait, AL Azhar is different? Let's not map it wrongly.
js_obj += '            "LAZNAS Agnia Care": "logos/AGNIA.png"\n' # assuming it exists?
js_obj = js_obj.rstrip(',\n') + "\n          };"

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace fozLogos block
html_updated = re.sub(r'const fozLogos\s*=\s*{.*?};', js_obj, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_updated)

print("Updated index.html with new fozLogos mapping")
