import os
import shutil

html_path = 'index.html'
ramadan_path = 'ramadan.html'

shutil.copy(html_path, ramadan_path)

with open(ramadan_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title and Headers
html = html.replace('<title>Kurban OPZ Anggota FOZ</title>', '<title>Ramadhan OPZ Anggota FOZ</title>')
html = html.replace('<h1>Kurban OPZ Anggota FOZ</h1>', '<h1>Ramadhan OPZ Anggota FOZ</h1>')
html = html.replace('Ringkasan data penghimpunan dan penyaluran kurban 1447 H / 2026', 'Ringkasan data penghimpunan dan penyaluran Ramadhan 1447 H / 2026')

# 2. Update Sidebar Active State
html = html.replace('<li class="active"><a href="index.html"><i class="fas fa-sheep"></i> <span>Dashboard Kurban</span></a></li>', '<li><a href="index.html"><i class="fas fa-sheep"></i> <span>Dashboard Kurban</span></a></li>')
html = html.replace('<li><a href="ramadan.html"><i class="fas fa-moon"></i> <span>Dashboard Ramadhan</span></a></li>', '<li class="active"><a href="ramadan.html"><i class="fas fa-moon"></i> <span>Dashboard Ramadhan</span></a></li>')

# 3. Update URL
old_url = "const rawUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQzIND5CL0y6ye7QeP_4R0gq9Qi2M1fF7hrHzaWWMykMTN7T5Z5mmEH4ly2xC6xjPk2CbMfEP5s3Pue/pub?gid=1807251763&single=true&output=csv';"
new_url = "const rawUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQJta5FINk6bb9i9AQLnR2gVifQLd7fR5jb3WHtJonGiD-1VPIGX9IAr4nh856MYYYJ5eGGwaIpA2Ix/pub?gid=1395490505&single=true&output=csv';"
if old_url in html:
    html = html.replace(old_url, new_url)
else:
    # Just in case the old URL string is slightly different
    html = html.replace('https://docs.google.com/spreadsheets/d/e/2PACX-1vQzIND5CL0y6ye7QeP_4R0gq9Qi2M1fF7hrHzaWWMykMTN7T5Z5mmEH4ly2xC6xjPk2CbMfEP5s3Pue/pub?gid=1807251763&single=true&output=csv', 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQJta5FINk6bb9i9AQLnR2gVifQLd7fR5jb3WHtJonGiD-1VPIGX9IAr4nh856MYYYJ5eGGwaIpA2Ix/pub?gid=1395490505&single=true&output=csv')

# 4. Update Card Labels
html = html.replace('<div class="stat-label">Total Pekurban</div>', '<div class="stat-label">Total Muzakki</div>')
html = html.replace('<div class="stat-label">Total Setara Kambing</div>', '<div class="stat-label">Total Penyaluran</div>')
html = html.replace('<i class="fas fa-sheep stat-icon"></i>', '<i class="fas fa-hand-holding-heart stat-icon"></i>')

# 5. Update Table Headers
html = html.replace('<th>Pekurban</th>', '<th>Muzakki</th>')
html = html.replace('<th>Penerima</th>', '<th>Penerima Manfaat</th>')
html = html.replace('<th>Setara Kambing</th>', '<th>Total Penyaluran</th>')

# 6. Update JS Parsing Logic
html = html.replace("let himpunan = parseIndonesianNumber(row['1. Total Penghimpunan Kurban (Rupiah)']);", "let himpunan = parseIndonesianNumber(row['2. Total Capaian Penghimpunan Ramadan 1447 H / 2026 (Rupiah)']);")
html = html.replace("let himpunanLalu = parseIndonesianNumber(row['9. Total Penghimpunan Kurban Tahun Sebelumnya (1446 H/2025) (Rupiah)']);", "let himpunanLalu = parseIndonesianNumber(row['2. Total Capaian Penghimpunan Ramadan 1446 H / 2025 (Tahun Lalu) (Rupiah)']);")
html = html.replace("let rowPekurban = parseIndonesianNumber(row['2. Total Pekurban (Orang)']);", "let rowPekurban = parseIndonesianNumber(row['3. Total Donatur/Muzakki Ramadan 1447 H / 2026 (Orang)']);")
html = html.replace("let rowPenerima = parseIndonesianNumber(row['3. Total Penerima Manfaat (Orang)']);", "let rowPenerima = parseIndonesianNumber(row['5. Total Penerima Manfaat Ramadan 1447 H / 2026 (Orang)']);")

# Replace Setara Kambing calc with Total Penyaluran
setara_logic = """              let rowKambing = parseIndonesianNumber(row['4. Total Domba/Kambing (Ekor)']);
              let rowSapi = parseIndonesianNumber(row['5. Total Sapi/Kerbau (ekor)']);
              let rowUnta = parseIndonesianNumber(row['6. Total Unta (ekor)']);
              let rowSetara = rowKambing + (rowSapi * 7) + (rowUnta * 10);"""
new_setara_logic = """              let rowSetara = parseIndonesianNumber(row['4. Total Penyaluran Ramadan 1447 H / 2026 (Rupiah)']);"""
html = html.replace(setara_logic, new_setara_logic)

# Replace 'Ekor' with Rupiah formatting for Penyaluran
html = html.replace("document.getElementById('total-setara').innerText = totalSetara.toLocaleString('id-ID');", "document.getElementById('total-setara').innerText = 'Rp ' + formatRupiahShort(totalSetara);")
html = html.replace("<td>${o.setara.toLocaleString('id-ID')} ekor</td>", "<td>Rp ${formatRupiahShort(o.setara)}</td>")

# Also change the sorting string for table header if any
html = html.replace("let colMap = { nama: 'nama', skala: 'skala', penghimpunan: 'penghimpunan', pertumbuhan: 'pertumbuhan', setara: 'setara', pekurban: 'pekurban', penerima: 'penerima' };", "let colMap = { nama: 'nama', skala: 'skala', penghimpunan: 'penghimpunan', pertumbuhan: 'pertumbuhan', setara: 'setara', pekurban: 'pekurban', penerima: 'penerima' };")

with open(ramadan_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("ramadan.html generated successfully.")
