import csv
import sys

rows = []
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Lembaga Anda', '').strip()
        if not name:
            continue
        
        def parse_num(s):
            if not s: return 0
            s = s.strip().replace('.', '').replace(',', '').replace('%', '').replace('-', '').replace(' ', '')
            try: return int(s)
            except: return 0
        
        penghimpunan = parse_num(row.get('1. Total Penghimpunan Kurban (Rupiah)', ''))
        pekurban = parse_num(row.get('2. Total Pekurban (Orang)', ''))
        penerima = parse_num(row.get('3. Total Penerima Manfaat (Orang)', ''))
        kambing = parse_num(row.get('4. Total Domba/Kambing (Ekor)', ''))
        sapi = parse_num(row.get('5. Total Sapi/Kerbau (ekor)', ''))
        unta = parse_num(row.get('6. Total Unta (ekor)', ''))
        
        total_hewan = kambing + sapi + unta
        
        # Rasio penerima per hewan
        rasio_per_hewan = penerima / total_hewan if total_hewan > 0 else 0
        
        # Rasio penerima per pekurban
        rasio_per_pekurban = penerima / pekurban if pekurban > 0 else 0
        
        # Rasio penghimpunan per hewan (harga rata2 per ekor)
        harga_per_ekor = penghimpunan / total_hewan if total_hewan > 0 else 0
        
        # Rasio penghimpunan per pekurban
        ticket = penghimpunan / pekurban if pekurban > 0 else 0
        
        rows.append({
            'name': name,
            'penghimpunan': penghimpunan,
            'pekurban': pekurban,
            'penerima': penerima,
            'kambing': kambing,
            'sapi': sapi,
            'unta': unta,
            'total_hewan': total_hewan,
            'rasio_per_hewan': rasio_per_hewan,
            'rasio_per_pekurban': rasio_per_pekurban,
            'harga_per_ekor': harga_per_ekor,
            'ticket': ticket
        })

# Sort and display anomalies
print("=" * 100)
print("🔍 ANALISA ANOMALI DATA KURBAN OPZ")
print("=" * 100)

# 1. Rasio Penerima per Hewan Kurban (logika: 1 kambing ~15-40 orang, 1 sapi ~70-200 orang)
print("\n📌 ANOMALI 1: Rasio Penerima per Hewan Kurban (terlalu tinggi > 100 jiwa/ekor)")
print("-" * 100)
print(f"{'Lembaga':<45} {'Kambing':>8} {'Sapi':>6} {'Total':>6} {'Penerima':>10} {'Rasio/Ekor':>12}")
print("-" * 100)
anomalies1 = sorted([r for r in rows if r['rasio_per_hewan'] > 100], key=lambda x: -x['rasio_per_hewan'])
for r in anomalies1:
    print(f"{r['name'][:44]:<45} {r['kambing']:>8} {r['sapi']:>6} {r['total_hewan']:>6} {r['penerima']:>10,} {r['rasio_per_hewan']:>10,.0f} j/e")

# 2. Rasio Penerima per Pekurban (terlalu tinggi)
print(f"\n📌 ANOMALI 2: Rasio Penerima per Pekurban (terlalu tinggi > 200 jiwa/pekurban)")
print("-" * 100)
print(f"{'Lembaga':<45} {'Pekurban':>10} {'Penerima':>10} {'Rasio':>12}")
print("-" * 100)
anomalies2 = sorted([r for r in rows if r['rasio_per_pekurban'] > 200], key=lambda x: -x['rasio_per_pekurban'])
for r in anomalies2:
    print(f"{r['name'][:44]:<45} {r['pekurban']:>10,} {r['penerima']:>10,} {r['rasio_per_pekurban']:>10,.0f} j/pk")

# 3. Harga per ekor terlalu murah (< 500rb) atau terlalu mahal (> 50jt)
print(f"\n📌 ANOMALI 3: Harga rata-rata per ekor tidak wajar (<500rb atau >50jt)")
print("-" * 100)
print(f"{'Lembaga':<45} {'Penghimpunan':>15} {'Total Ekor':>10} {'Harga/Ekor':>15}")
print("-" * 100)
anomalies3 = sorted([r for r in rows if r['total_hewan'] > 0 and (r['harga_per_ekor'] < 500000 or r['harga_per_ekor'] > 50000000)], key=lambda x: x['harga_per_ekor'])
for r in anomalies3:
    print(f"{r['name'][:44]:<45} {r['penghimpunan']:>15,} {r['total_hewan']:>10} {r['harga_per_ekor']:>13,.0f} Rp")

# 4. Pekurban > total hewan (logikanya 1 pekurban minimal 1 ekor atau 1/7 sapi)
print(f"\n📌 ANOMALI 4: Pekurban jauh lebih banyak dari total hewan (rasio > 7:1)")
print("-" * 100)
print(f"{'Lembaga':<45} {'Pekurban':>10} {'Total Ekor':>10} {'Rasio Pk/Ek':>12}")
print("-" * 100)
anomalies4 = sorted([r for r in rows if r['total_hewan'] > 0 and (r['pekurban'] / r['total_hewan']) > 7], key=lambda x: -(x['pekurban'] / x['total_hewan']))
for r in anomalies4:
    rasio = r['pekurban'] / r['total_hewan']
    print(f"{r['name'][:44]:<45} {r['pekurban']:>10,} {r['total_hewan']:>10} {rasio:>10,.1f}:1")

# Summary stats
print(f"\n{'=' * 100}")
print(f"📊 RINGKASAN")
print(f"Total OPZ: {len(rows)}")
total_penerima = sum(r['penerima'] for r in rows)
total_pekurban = sum(r['pekurban'] for r in rows)
total_hewan = sum(r['total_hewan'] for r in rows)
print(f"Total Penerima: {total_penerima:,}")
print(f"Total Pekurban: {total_pekurban:,}")
print(f"Total Hewan: {total_hewan:,}")
print(f"Rasio Global Penerima/Pekurban: 1:{total_penerima/total_pekurban:.0f}" if total_pekurban > 0 else "")
print(f"Rasio Global Penerima/Hewan: {total_penerima/total_hewan:.0f} jiwa/ekor" if total_hewan > 0 else "")
