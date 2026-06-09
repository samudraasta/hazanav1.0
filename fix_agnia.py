import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Agnia Care
html = html.replace('"LAZNAS Agnia Care": "logos/LAZNAS Agnia Care.png"', '"LAZNAS Agnia Care": "logos/LAZNAS Agnia Care.png",\n            "LAZIS Agnia Care": "logos/LAZNAS Agnia Care.png"')

# Solo Peduli
html = html.replace('"LAZ SOLOPEDULI": "logos/solopeduli.png"', '"LAZ SOLOPEDULI": "logos/solopeduli.png",\n            "Solo Peduli": "logos/solopeduli.png"')

# Saku Yatim
html = html.replace('"LAZ SAKU YATIM INDONESIA": "logos/Yayasan Rumah Perubahan Indonesia (Saku Yatim).png"', '"LAZ SAKU YATIM INDONESIA": "logos/Yayasan Rumah Perubahan Indonesia (Saku Yatim).png",\n            "Saku Yatim": "logos/Yayasan Rumah Perubahan Indonesia (Saku Yatim).png"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
