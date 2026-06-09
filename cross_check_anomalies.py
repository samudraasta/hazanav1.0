import csv

def parse_num(s):
    if not s: return 0
    s = s.strip().replace('Rp', '').replace('.', '').replace(',', '').replace('%', '').replace(' ', '')
    s = s.replace('-', '')
    try: return int(s)
    except: return 0

# Load 2025 Data
data_2025 = {}
with open('data_2025.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Lembaga Anda', '').strip()
        if not name: continue
        
        penghimpunan_key = next((k for k in row.keys() if 'Total Pengihimpunan Kurban (Rupiah)' in k or 'Total Penghimpunan' in k), None)
        penghimpunan = parse_num(row.get(penghimpunan_key, '')) if penghimpunan_key else 0
        
        pekurban = parse_num(row.get('Total Pekurban (Orang)', ''))
        penerima = parse_num(row.get('Total Penerima Manfaat (Orang)', ''))
        
        data_2025[name.lower()] = {
            'name': name,
            'penghimpunan': penghimpunan,
            'pekurban': pekurban,
            'penerima': penerima
        }

# Load 2026 Data and cross-reference
cross_checks = []

with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Lembaga Anda', '').strip()
        if not name: continue
        
        penghimpunan_26 = parse_num(row.get('1. Total Penghimpunan Kurban (Rupiah)', ''))
        pekurban_26 = parse_num(row.get('2. Total Pekurban (Orang)', ''))
        penerima_26 = parse_num(row.get('3. Total Penerima Manfaat (Orang)', ''))
        himpunan_lalu_klaim = parse_num(row.get('9. Total Penghimpunan Kurban Tahun Sebelumnya (1446 H/2025) (Rupiah)', ''))
        
        pic = row.get('Nama PIC', '').strip()
        wa = row.get('No WhatsApp', '').strip()
        
        if name.lower() in data_2025:
            d25 = data_2025[name.lower()]
            
            # 1. Klaim 2025 vs Realita 2025 (discrepancy)
            klaim_diff = abs(himpunan_lalu_klaim - d25['penghimpunan'])
            klaim_diff_pct = (klaim_diff / d25['penghimpunan']) * 100 if d25['penghimpunan'] > 0 else 0
            
            # 2. Real YoY Growth 2026 vs 2025
            real_growth_himpunan = ((penghimpunan_26 - d25['penghimpunan']) / d25['penghimpunan']) * 100 if d25['penghimpunan'] > 0 else 0
            real_growth_pekurban = ((pekurban_26 - d25['pekurban']) / d25['pekurban']) * 100 if d25['pekurban'] > 0 else 0
            real_growth_penerima = ((penerima_26 - d25['penerima']) / d25['penerima']) * 100 if d25['penerima'] > 0 else 0
            
            cross_checks.append({
                'name': name,
                'pic': pic, 'wa': wa,
                'himpunan_25_asli': d25['penghimpunan'],
                'himpunan_25_klaim': himpunan_lalu_klaim,
                'klaim_diff': klaim_diff,
                'klaim_diff_pct': klaim_diff_pct,
                'himpunan_26': penghimpunan_26,
                'growth_himpunan': real_growth_himpunan,
                'penerima_25': d25['penerima'],
                'penerima_26': penerima_26,
                'growth_penerima': real_growth_penerima,
                'pekurban_25': d25['pekurban'],
                'pekurban_26': pekurban_26,
                'growth_pekurban': real_growth_pekurban
            })

print("# Hasil Cross-Check Data 2026 vs 2025")
print()
print(f"Ditemukan **{len(cross_checks)} lembaga** yang mengisi data di tahun 2025 dan 2026. Berikut adalah anomali dari hasil perbandingan:")
print()

# 1. Klaim Tahun Lalu Berbeda Signifikan
print("## 1. Discrepancy Klaim Data Tahun Lalu")
print("Lembaga yang data 'Penghimpunan Tahun Lalu' di form 2026 berbeda jauh (>10%) dari data asli yang mereka laporkan di tahun 2025.")
print()
print("| Lembaga | Laporan Asli 2025 | Klaim di Form 2026 | Selisih | PIC |")
print("|---------|------------------:|-------------------:|--------:|-----|")
a1 = sorted([c for c in cross_checks if c['klaim_diff_pct'] > 10], key=lambda x: -x['klaim_diff_pct'])
for c in a1:
    print(f"| {c['name']} | Rp {c['himpunan_25_asli']:,} | Rp {c['himpunan_25_klaim']:,} | {c['klaim_diff_pct']:.0f}% | {c['pic']} ({c['wa']}) |")
if not a1: print("| (Tidak ada anomali) | | | | |")

# 2. Pertumbuhan Ekstrem
print()
print("## 2. Pertumbuhan/Penurunan Sangat Ekstrem (YoY)")
print("Lembaga dengan lonjakan >300% atau penurunan >70% dari tahun sebelumnya yang perlu diverifikasi ulang.")
print()
print("| Lembaga | Himpunan 2025 | Himpunan 2026 | Real Growth | PIC |")
print("|---------|--------------:|--------------:|------------:|-----|")
a2 = sorted([c for c in cross_checks if c['growth_himpunan'] > 300 or c['growth_himpunan'] < -70], key=lambda x: -x['growth_himpunan'])
for c in a2:
    sign = "+" if c['growth_himpunan'] > 0 else ""
    print(f"| {c['name']} | Rp {c['himpunan_25_asli']:,} | Rp {c['himpunan_26']:,} | **{sign}{c['growth_himpunan']:.0f}%** | {c['pic']} ({c['wa']}) |")
if not a2: print("| (Tidak ada anomali) | | | | |")

# 3. Anomali Penerima Manfaat
print()
print("## 3. Anomali Lonjakan Penerima Manfaat")
print("Penerima manfaat melonjak drastis (>5x lipat) tanpa diikuti kenaikan penghimpunan yang setara. Sangat mungkin salah input di 2026.")
print()
print("| Lembaga | Penerima 2025 | Penerima 2026 | Growth Penerima | Growth Himpunan | PIC |")
print("|---------|--------------:|--------------:|----------------:|----------------:|-----|")
a3 = sorted([c for c in cross_checks if c['growth_penerima'] > 400], key=lambda x: -x['growth_penerima'])
for c in a3:
    print(f"| {c['name']} | {c['penerima_25']:,} | {c['penerima_26']:,} | +{c['growth_penerima']:.0f}% | +{c['growth_himpunan']:.0f}% | {c['pic']} ({c['wa']}) |")
if not a3: print("| (Tidak ada anomali) | | | | | |")
