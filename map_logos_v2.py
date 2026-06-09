import json

with open('mapping_local.json', 'r') as f:
    mapping = json.load(f)

mapping['Baitul Maal BMT Beringharjo'] = 'logos/LOGO-BMT-Beringharjo.png'
mapping['DSM Bali'] = 'logos/DSM dompet sosial.png'
mapping['LAZ Darul Hikam'] = 'logos/laz daarul hikam.png'
mapping['LAZ Generasi Rabbani'] = 'logos/rabbaniyyin care.png'
mapping['LAZ MKU'] = 'logos/LAZ Membangun Keluarga Utama (LAZ MKU).png'
mapping['LAZIS Muhammadiyah (LAZISMU)'] = 'logos/lazismu.png'
mapping['LAZNAS LMI'] = 'logos/LMI.png'
mapping['LAZNAS YDSF'] = 'logos/YDSF.png'
# The missing ones are LAZ BMBU Kota Bontang and LAZNAS IKADI

with open('mapping_local.json', 'w') as f:
    json.dump(mapping, f, indent=2)

print("Updated mapping.")
