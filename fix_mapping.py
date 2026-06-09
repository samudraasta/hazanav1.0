import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix IZI
html = html.replace('"Inisiatif Zakat Indonesia (IZI)": "logos/Inisiatif Zakat Indonesia.png"', '"Inisiatif Zakat Indonesia (IZI)": "logos/Inisiatif Zakat Indonesia.png"')
html = html.replace('"Inisiatif Zakat Indonesia (IZI)": "logos/Rumah Zakat.png"', '"Inisiatif Zakat Indonesia (IZI)": "logos/Inisiatif Zakat Indonesia.png"')

# Fix Inovasi
html = html.replace('"Inovasi Zakat Indonesia": "logos/Inisiatif Zakat Indonesia.png"', '"Inovasi Zakat Indonesia": "logos/Inovasi Zakat Indonesia.png"')
html = html.replace('"Inovasi Zakat Indonesia": "logos/Rumah Zakat.png"', '"Inovasi Zakat Indonesia": "logos/Inovasi Zakat Indonesia.png"')

# Fix Saku Yatim
html = html.replace('"LAZ SAKU YATIM INDONESIA": "logos/Rumah Yatim.png"', '"LAZ SAKU YATIM INDONESIA": "logos/Yayasan Rumah Perubahan Indonesia (Saku Yatim).png"')

# Fix Zakat Sukses
html = html.replace('"LAZ Zakat Sukses": "logos/Inisiatif Zakat Indonesia.png"', '"LAZ Zakat Sukses": "logos/Zakat Sukses.png"')
html = html.replace('"LAZ Zakat Sukses": "logos/Rumah Zakat.png"', '"LAZ Zakat Sukses": "logos/Zakat Sukses.png"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
