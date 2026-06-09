import re

with open('ramadan.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The grid template might be 4 columns. We should change it to 3 columns.
# It's probably in kurban2026.css or inline style. If inline: `grid-template-columns: repeat(4, 1fr);`
html = html.replace('grid-template-columns: repeat(4, 1fr);', 'grid-template-columns: repeat(3, 1fr);')

# The 4th card starts with `<div class="stat-card" style="padding: 1rem 1.5rem;">`
# and has `<div class="stat-label">Total Penyaluran</div>` inside.
# We will use regex to remove that entire div.
# We need to find the specific block.
pattern = re.compile(r'(\s*<div class="stat-card" style="padding: 1rem 1.5rem;">\s*<div class="stat-label">Total Penyaluran</div>.*?</div>\s*</div>)', re.DOTALL)
html = pattern.sub('', html)

# We also need to hide the table column for "Total Penyaluran" if the user meant 3 cards. 
# But wait, user said "Iya 3 aja" in response to "kotak ke-4 diganti... atau dihapus saja sehingga hanya 3 kotak?". 
# They meant the card. The table column for "Total Penyaluran" can remain because it's good data.
# Let's just remove the card.

with open('ramadan.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Removed 4th card successfully.")
