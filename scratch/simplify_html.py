import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove fozLogos definition
html = re.sub(r'\s*const fozLogos = \{.*?\};\n', '\n', html, flags=re.DOTALL)

# Simplify logoUrl assignment
old_logic = """             let localLogoUrl = `logos_standard/${lembaga}.png`;
             let logoUrl = localLogoUrl;
             for (let key in fozLogos) {
                 if (key.toLowerCase() === lembaga.toLowerCase()) {
                     logoUrl = fozLogos[key];
                     break;
                 }
             }"""

new_logic = """             let logoUrl = `logos_standard/${lembaga}.png`;"""

html = html.replace(old_logic, new_logic)

# Also check for logos/ fallback if user edited it to logos_standard
old_logic2 = """             let localLogoUrl = `logos/${lembaga}.png`;
             let logoUrl = localLogoUrl;
             for (let key in fozLogos) {
                 if (key.toLowerCase() === lembaga.toLowerCase()) {
                     logoUrl = fozLogos[key];
                     break;
                 }
             }"""
html = html.replace(old_logic2, new_logic)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html simplified!")
