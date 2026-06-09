import csv

rows = []
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Lembaga Anda', '').strip()
        if not name:
            continue
        
        def parse_num(s):
            if not s: return 0
            s = s.strip().replace('.', '').replace(',', '').replace('%', '').replace(' ', '')
            s = s.replace('-', '')
            try: return int(s)
            except: return 0
        
        def parse_growth(s):
            if not s: return None
            s = s.strip().replace('%', '').replace(' ', '')
            try: return int(s)
            except: return None
        
        penghimpunan = parse_num(row.get('1. Total Penghimpunan Kurban (Rupiah)', ''))
        pekurban = parse_num(row.get('2. Total Pekurban (Orang)', ''))
        penerima = parse_num(row.get('3. Total Penerima Manfaat (Orang)', ''))
        kambing = parse_num(row.get('4. Total Domba/Kambing (Ekor)', ''))
        sapi = parse_num(row.get('5. Total Sapi/Kerbau (ekor)', ''))
        unta = parse_num(row.get('6. Total Unta (ekor)', ''))
        himpunan_lalu = parse_num(row.get('9. Total Penghimpunan Kurban Tahun Sebelumnya (1446 H/2025) (Rupiah)', ''))
        growth = parse_growth(row.get('Pertumbuhan', ''))
        pic = row.get('Nama PIC', '').strip()
        wa = row.get('No WhatsApp', '').strip()
        skala = row.get('SKALA', '').strip()
        
        total_hewan = kambing + sapi + unta
        rasio_per_hewan = penerima / total_hewan if total_hewan > 0 else 0
        rasio_per_pekurban = penerima / pekurban if pekurban > 0 else 0
        harga_per_ekor = penghimpunan / total_hewan if total_hewan > 0 else 0
        
        rows.append({
            'name': name, 'skala': skala, 'pic': pic, 'wa': wa,
            'penghimpunan': penghimpunan, 'pekurban': pekurban, 
            'penerima': penerima, 'kambing': kambing, 'sapi': sapi, 
            'unta': unta, 'total_hewan': total_hewan,
            'himpunan_lalu': himpunan_lalu, 'growth': growth,
            'rasio_per_hewan': rasio_per_hewan,
            'rasio_per_pekurban': rasio_per_pekurban,
            'harga_per_ekor': harga_per_ekor,
        })

# --- Output Markdown ---
print("# Laporan Anomali Data Kurban OPZ 1447H / 2026")
print()
print("> Dokumen ini berisi daftar data yang **berpotensi salah input (human error)** berdasarkan pengecekan logika.")
print("> Silakan verifikasi langsung ke PIC masing-masing lembaga.")
print()

# ANOMALI 1: Penerima per Hewan sangat tinggi
print("## 1. Rasio Penerima per Hewan Kurban Tidak Wajar")
print()
print("**Logika:** 1 ekor kambing (~15-20kg daging) bisa menjangkau ±15-40 jiwa. 1 ekor sapi (~200kg daging) ±100-200 jiwa.")
print("Jika rasio melebihi **200 jiwa/ekor**, kemungkinan besar ada salah input di kolom penerima atau kolom hewan.")
print()
print("| No | Lembaga | Skala | Kambing | Sapi | Total Ekor | Penerima | Rasio/Ekor | PIC | WA |")
print("|:--:|---------|-------|--------:|-----:|-----------:|---------:|-----------:|-----|-----|")
a1 = sorted([r for r in rows if r['rasio_per_hewan'] > 200], key=lambda x: -x['rasio_per_hewan'])
for i, r in enumerate(a1, 1):
    print(f"| {i} | {r['name']} | {r['skala']} | {r['kambing']:,} | {r['sapi']:,} | {r['total_hewan']:,} | {r['penerima']:,} | **{r['rasio_per_hewan']:,.0f}** | {r['pic']} | {r['wa']} |")

# ANOMALI 2: Penerima per Hewan tinggi (100-200)
print()
print("### Perlu Dicek (rasio 100-200 jiwa/ekor — mungkin olahan)")
print()
print("| No | Lembaga | Skala | Kambing | Sapi | Total Ekor | Penerima | Rasio/Ekor | PIC | WA |")
print("|:--:|---------|-------|--------:|-----:|-----------:|---------:|-----------:|-----|-----|")
a1b = sorted([r for r in rows if 100 < r['rasio_per_hewan'] <= 200], key=lambda x: -x['rasio_per_hewan'])
for i, r in enumerate(a1b, 1):
    print(f"| {i} | {r['name']} | {r['skala']} | {r['kambing']:,} | {r['sapi']:,} | {r['total_hewan']:,} | {r['penerima']:,} | **{r['rasio_per_hewan']:,.0f}** | {r['pic']} | {r['wa']} |")

# ANOMALI 3: Harga per ekor tidak wajar
print()
print("## 2. Harga Rata-rata per Ekor Tidak Wajar")
print()
print("**Logika:** Harga kambing ±Rp 2-5 juta, sapi ±Rp 15-35 juta. Jika rata-rata per ekor <Rp 500rb atau >Rp 50jt, ada kemungkinan salah input.")
print()
print("| No | Lembaga | Skala | Penghimpunan | Total Ekor | Harga/Ekor | Dugaan Masalah | PIC | WA |")
print("|:--:|---------|-------|-------------:|-----------:|-----------:|----------------|-----|-----|")
a3 = sorted([r for r in rows if r['total_hewan'] > 0 and (r['harga_per_ekor'] < 500000 or r['harga_per_ekor'] > 50000000)], key=lambda x: x['harga_per_ekor'])
for i, r in enumerate(a3, 1):
    dugaan = "Terlalu murah" if r['harga_per_ekor'] < 500000 else "Terlalu mahal"
    print(f"| {i} | {r['name']} | {r['skala']} | Rp {r['penghimpunan']:,} | {r['total_hewan']:,} | **Rp {r['harga_per_ekor']:,.0f}** | {dugaan} | {r['pic']} | {r['wa']} |")

# ANOMALI 4: Penerima sangat besar (>100rb) perlu dicek
print()
print("## 3. Jumlah Penerima Manfaat Sangat Besar (>100.000 jiwa)")
print()
print("**Logika:** Angka penerima yang sangat besar perlu diverifikasi — apakah benar penerima daging kurban, atau termasuk penerima program lain?")
print()
print("| No | Lembaga | Skala | Pekurban | Penerima | Total Ekor | Rasio/Ekor | PIC | WA |")
print("|:--:|---------|-------|--------:|---------:|-----------:|-----------:|-----|-----|")
a4 = sorted([r for r in rows if r['penerima'] > 100000], key=lambda x: -x['penerima'])
for i, r in enumerate(a4, 1):
    print(f"| {i} | {r['name']} | {r['skala']} | {r['pekurban']:,} | **{r['penerima']:,}** | {r['total_hewan']:,} | {r['rasio_per_hewan']:,.0f} | {r['pic']} | {r['wa']} |")

# ANOMALI 5: Pertumbuhan sangat tinggi (>300%)
print()
print("## 4. Pertumbuhan Sangat Tinggi (>300%)")
print()
print("**Logika:** Pertumbuhan >300% bisa jadi benar (lembaga baru berkembang), tapi perlu dicek apakah data tahun lalu benar.")
print()
print("| No | Lembaga | Skala | Tahun Ini | Tahun Lalu | Growth | PIC | WA |")
print("|:--:|---------|-------|----------:|-----------:|-------:|-----|-----|")
a5 = sorted([r for r in rows if r['growth'] is not None and r['growth'] > 300], key=lambda x: -x['growth'])
for i, r in enumerate(a5, 1):
    print(f"| {i} | {r['name']} | {r['skala']} | Rp {r['penghimpunan']:,} | Rp {r['himpunan_lalu']:,} | **+{r['growth']}%** | {r['pic']} | {r['wa']} |")

# ANOMALI 6: Penghimpunan 0 atau sangat kecil tapi ada hewan
print()
print("## 5. Penghimpunan Sangat Kecil tapi Hewan Banyak")
print()
print("**Logika:** Jika penghimpunan < Rp 10 juta tapi total hewan > 10 ekor, kemungkinan salah input nominal.")
print()
print("| No | Lembaga | Skala | Penghimpunan | Total Ekor | Harga/Ekor | PIC | WA |")
print("|:--:|---------|-------|-------------:|-----------:|-----------:|-----|-----|")
a6 = sorted([r for r in rows if r['penghimpunan'] < 10000000 and r['total_hewan'] > 10], key=lambda x: x['harga_per_ekor'])
for i, r in enumerate(a6, 1):
    print(f"| {i} | {r['name']} | {r['skala']} | **Rp {r['penghimpunan']:,}** | {r['total_hewan']:,} | Rp {r['harga_per_ekor']:,.0f} | {r['pic']} | {r['wa']} |")

print()
print("---")
print()
print("## Ringkasan Dampak Anomali terhadap Insight")
print()

# Calculate with and without top anomaly
total_penerima = sum(r['penerima'] for r in rows)
total_pekurban = sum(r['pekurban'] for r in rows)
total_hewan = sum(r['total_hewan'] for r in rows)

# Without Al-Qoyyim
tp_clean = total_penerima - 3200000 + 3200  # assume 3200 instead of 3.2M
print(f"| Metrik | Dengan Anomali | Tanpa Koreksi Al-Qoyyim |")
print(f"|--------|---------------:|------------------------:|")
print(f"| Total Penerima | {total_penerima:,} | {tp_clean:,} |")
print(f"| Rasio Penerima/Pekurban | 1:{total_penerima/total_pekurban:.0f} | 1:{tp_clean/total_pekurban:.0f} |")
print(f"| Rasio Penerima/Hewan | {total_penerima/total_hewan:.0f} jiwa/ekor | {tp_clean/total_hewan:.0f} jiwa/ekor |")

