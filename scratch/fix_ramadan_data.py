import re

with open('ramadan.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix data headers mapping
html = html.replace("let name = (row['Lembaga Anda'] || '').trim();", "let name = (row['Nama LAZ / BAZ'] || '').trim();")
html = html.replace("let provStr = (row['7. Provinsi Penyaluran (Dalam Negeri)'] || '').toLowerCase();", "let provStr = (row['Provinsi'] || row['6. Wilayah Penyaluran Ramadan 1447 H / 2026 (Kab/Kota atau Provinsi)'] || '').toLowerCase();")
html = html.replace("let negStr = (row['8. Negara Penyaluran Kurban di Luar Negeri'] || '').toLowerCase();", "let negStr = (row['Negara'] || '').toLowerCase();")

# 2. Fix Table Headers
html = html.replace('<th class="sortable col-num" style="text-align: center;" data-col="setara">Setara D/K <i class="fas fa-sort"></i></th>', '')
html = html.replace('<th class="sortable col-num" style="text-align: center;" data-col="pekurban">Pekurban <i class="fas fa-sort"></i></th>', '<th class="sortable col-num" style="text-align: center;" data-col="pekurban">Muzakki/Donatur <i class="fas fa-sort"></i></th>')
html = html.replace('colspan="7"', 'colspan="6"')

# 3. Fix Table Row Data in JS
html = html.replace('<td class="col-num">Rp ${formatRupiahShort(o.setara)}</td>', '')

# 4. Remove small cards for Domba/Kambing and Sapi/Kerbau
# The cards look like this:
# <div class="stat-card" style="padding: 1rem 1.5rem;">
#    <div class="stat-label">Domba / Kambing (Ekor)</div>
#    <div class="stat-value" id="val-kambing" style="font-size: 1.6rem;">0</div>...
# We can use regex to remove them.
pattern1 = re.compile(r'\s*<div class="stat-card"[^>]*>\s*<div class="stat-label">Domba / Kambing \(Ekor\)</div>.*?</div>\s*</div>', re.DOTALL)
html = pattern1.sub('', html)

pattern2 = re.compile(r'\s*<div class="stat-card"[^>]*>\s*<div class="stat-label">Sapi / Kerbau / Unta \(Ekor\)</div>.*?</div>\s*</div>', re.DOTALL)
html = pattern2.sub('', html)

# Make sure the grid for small stats is adjusted if needed. It's inline or CSS class.
# We'll just let CSS handle it (auto fill/fit).

with open('ramadan.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("ramadan.html data mapping and table fixed.")
