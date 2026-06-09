import csv
import re
import json

# Read FOZ HTML and extract URLs
with open('foz.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract URLs from HTML
urls = re.findall(r'src="(https://forumzakat.org/wp-content/uploads/[^"]+\.png)"', html)
urls = list(set(urls))

url_map = {}
for u in urls:
    # Get basename of the logo and sanitize it
    basename = u.split('/')[-1].replace('-100x57', '').replace('.png', '').lower()
    basename = re.sub(r'^\d+\.-', '', basename)
    basename = basename.replace('-', ' ').strip()
    url_map[u] = basename

# Read CSV and get unique OPZ names from "Lembaga Anda"
opz_names = set()
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Lembaga Anda')
        if name and name.strip():
            opz_names.add(name.strip())

def simplify(name):
    # Strip common prefixes/suffixes and geographic terms
    words_to_remove = [
        'laznas', 'lazis', 'laz', 'yayasan', 'foundation', 'pusat', 
        'nasional', 'daerah', 'kabupaten', 'kota', 'provinsi', 
        'indonesia', 'zakat', 'infaq', 'shadaqah', 'sedekah'
    ]
    name = name.lower()
    for w in words_to_remove:
        name = re.sub(r'\b' + w + r'\b', '', name)
    
    # Clean up non-alphanumeric chars
    name = re.sub(r'[^a-z0-9\s]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def get_candidate_acronyms(name):
    # Standard cleanup for acronym check
    words_to_remove = ['laznas', 'lazis', 'laz', 'yayasan', 'foundation', 'pusat', 'nasional', 'daerah', 'kabupaten', 'kota', 'provinsi']
    name_clean = name.lower()
    for w in words_to_remove:
        name_clean = re.sub(r'\b' + w + r'\b', '', name_clean)
    name_clean = re.sub(r'[^a-z0-9\s]', ' ', name_clean)
    name_clean = re.sub(r'\s+', ' ', name_clean).strip()
    
    words = [w for w in name_clean.split() if w]
    if not words:
        return []
    
    candidates = []
    # Candidate 1: All words (e.g. "Sahabat Yatim Indonesia" -> "syi")
    candidates.append("".join([w[0] for w in words]))
    
    # Candidate 2: Without "indonesia" if it is at the end (e.g. "Sahabat Yatim Indonesia" -> "sy")
    if len(words) >= 3 and words[-1] == 'indonesia':
        candidates.append("".join([w[0] for w in words[:-1]]))
        
    return [c for c in candidates if len(c) >= 2]

# Hand-crafted high-priority overrides for tricky matches or specific logos
manual_overrides = {
    "Dompet Dhuafa": "https://forumzakat.org/wp-content/uploads/2022/12/01.-DD-100x57.png",
    "Rumah Zakat": "https://forumzakat.org/wp-content/uploads/2022/12/02.-RZ-100x57.png",
    "Inisiatif Zakat Indonesia (IZI)": "https://forumzakat.org/wp-content/uploads/2022/12/03.-IZI-100x57.png",
    "LAZNAS YDSF": "https://forumzakat.org/wp-content/uploads/2022/12/09.-YDSF-100x57.png",
    "LAZIS Muhammadiyah (LAZISMU)": "https://forumzakat.org/wp-content/uploads/2022/12/12.-lazismu-100x57.png",
    "BSI Maslahat": "https://forumzakat.org/wp-content/uploads/2022/12/18.-BSI-Maslahat-100x57.png",
    "LAZIS JATENG": "https://forumzakat.org/wp-content/uploads/2022/12/24.-LAZIS-JATENG-100x57.png",
    "LAZIS Jateng": "https://forumzakat.org/wp-content/uploads/2022/12/24.-LAZIS-JATENG-100x57.png",
    "ZIS Indosat": "https://forumzakat.org/wp-content/uploads/2022/12/36.-ZIS-Indosat-100x57.png",
    "LAZ DASI NTB": "https://forumzakat.org/wp-content/uploads/2022/12/39.-DASI-NTB-100x57.png",
    "DSM Bali": "https://forumzakat.org/wp-content/uploads/2022/12/41.-DSM-100x57.png",
    "LAZ Al Bunyan": "https://forumzakat.org/wp-content/uploads/2022/12/45.-Al-Bunyan-100x57.png",
    "LAZ Lidzikri": "https://forumzakat.org/wp-content/uploads/2022/12/50.-Lidzikri-100x57.png",
    "LAZ Ummul Quro": "https://forumzakat.org/wp-content/uploads/2022/12/54.-LAZ-UQ-100x57.png",
    "LAZ YASA Malang": "https://forumzakat.org/wp-content/uploads/2022/12/55.-YASA-Malang-100x57.png",
    "Sinergi Foundation": "https://forumzakat.org/wp-content/uploads/2022/12/68.-Sinergi-Fond-100x57.png",
    "Rumah Amal Salman": "https://forumzakat.org/wp-content/uploads/2022/12/76.-RA-Salman-100x57.png",
    "LAZ DPU Kaltim": "https://forumzakat.org/wp-content/uploads/2022/12/81.-DPU-Kaltim-100x57.png",
    "LAZIS Sultan Agung": "https://forumzakat.org/wp-content/uploads/2022/12/85.-Sultan-Agung-100x57.png",
    "Pelopor Kepedulian": "https://forumzakat.org/wp-content/uploads/2022/12/97.-PELOPOR-100x57.png",
    "Baitulmaal Munzalan Indonesia": "https://forumzakat.org/wp-content/uploads/2025/12/BMI-100x57.png",
    "Amaliah Astra": "https://forumzakat.org/wp-content/uploads/2025/12/amaliah-astra-100x57.png",
    "Baitul Maal BMT Beringharjo": "https://forumzakat.org/wp-content/uploads/2025/12/bmt-beringharjo-100x57.png",
    "LAZNAS LMI": "https://forumzakat.org/wp-content/uploads/2025/12/lmi-1-100x57.png",
    "LAZNAS Mizan Amanah": "https://forumzakat.org/wp-content/uploads/2022/12/129.-Mizan-100x57.png",
    "BAMUIS BNI": "https://forumzakat.org/wp-content/uploads/2022/12/14.-BIMUIS-BNI.png",
    "LAZIS UNISIA": "https://forumzakat.org/wp-content/uploads/2022/12/155.-LAZIS-UNISIA.png",
    "LAZ Harapan Dhuafa": "https://forumzakat.org/wp-content/uploads/2022/12/32.-harfa.png",
    "MAI Foundation": "https://forumzakat.org/wp-content/uploads/2022/12/06.-MAI-Fond.png",
    "LAZIS Baiturrahman": "https://forumzakat.org/wp-content/uploads/2022/12/166.-Baiturrahaman.png",
    "LAZ RIZKI": "https://forumzakat.org/wp-content/uploads/2022/12/105.-RIZKI-100x57.png",
    "Yuk Peduli": "https://forumzakat.org/wp-content/uploads/2022/12/119.-Yuk-Peduli.png",
    "LAZ SAKU YATIM INDONESIA": "https://forumzakat.org/wp-content/uploads/2022/12/188.-Saku-Yatim.png",
    "Itqan Peduli": "https://forumzakat.org/wp-content/uploads/2022/12/128.-Itqan-100x57.png",
    "ZIS Yayasan Annur Insan Pembangkitan (YANIP)": "https://forumzakat.org/wp-content/uploads/2025/12/yanip-100x57.png",
    "Explore! Humanity": "https://forumzakat.org/wp-content/uploads/2022/12/182.-Explore-100x57.png",
    "Yayasan Rute Langkah Amanah": "https://forumzakat.org/wp-content/uploads/2025/12/rute-langkah-amanah-100x57.png",
    "LAZ Sahabat Kebaikan Umat (SAKU)": "https://forumzakat.org/wp-content/uploads/2022/12/159.-SAKU-100x57.png",
    "LAZ Masjid Raya Bintaro (LAZ MRBJ)": "https://forumzakat.org/wp-content/uploads/2022/12/173.-LAZ-MRBJ-100x57.png",
    "LAZ SOLOPEDULI": "https://forumzakat.org/wp-content/uploads/2022/12/34.-solopeduli-100x57.png",
    "Yayasan Gugus Karya Mandiri": "https://forumzakat.org/wp-content/uploads/2023/03/164.-Gugus-Karya-Mandiri-100x57.png",
    "LAZ BMBU Kota Bontang": "https://forumzakat.org/wp-content/uploads/2022/12/156.-BMBU-100x57.png",
    "LAZ Persada Jatim Indonesia": "https://forumzakat.org/wp-content/uploads/2022/12/193.-Persada-100x57.png",
    
    # Newly identified matches during research
    "Sahabat Yatim Indonesia": "https://forumzakat.org/wp-content/uploads/2022/12/163.-SY.png",
    "Infaq Berkah": "https://forumzakat.org/wp-content/uploads/2022/12/120.-IBQ.png",
    "Inovasi Zakat Indonesia": "https://forumzakat.org/wp-content/uploads/2022/12/190.-Inovazi.png",
    "LAZ Azka Al Baitul Amien Jember": "https://forumzakat.org/wp-content/uploads/2022/12/147.-Aska.png",
    "LAZ Zakat Sukses": "https://forumzakat.org/wp-content/uploads/2022/12/56.-ZS.png",
    "LAZIS Syuhada": "https://forumzakat.org/wp-content/uploads/2022/12/58.-MS.png",
    "Sukoharjo Peduli": "https://forumzakat.org/wp-content/uploads/2022/12/146.-lazsukoharjo.png",
    "TAMAN ZAKAT INDONESIA": "https://forumzakat.org/wp-content/uploads/2022/12/127.-TZ.png",
    "LAZIS NURUL FALAH": "https://forumzakat.org/wp-content/uploads/2022/12/57.-NF.png",
    "Pondok Sedekah Indonesia": "https://forumzakat.org/wp-content/uploads/2022/12/63.-PSI.png",
    "Rumah Sosial KUTUB (R-SIK)": "https://forumzakat.org/wp-content/uploads/2022/12/99.-RSK.png",
    "LAZ Sahabat Kebaikan Umat (SAKU)": "https://forumzakat.org/wp-content/uploads/2022/12/159.-SAKU-100x57.png"
}

mapping = {}

for opz in sorted(opz_names):
    # Check manual overrides first
    if opz in manual_overrides:
        mapping[opz] = manual_overrides[opz]
        continue
        
    keyword = simplify(opz)
    acronyms = get_candidate_acronyms(opz)
    best_u = None
    
    # 1. Exact match with simplified name
    for u, basename in url_map.items():
        simplified_basename = simplify(basename)
        if keyword and simplified_basename and keyword == simplified_basename:
            best_u = u
            break
            
    # 2. Acronym match
    if not best_u and acronyms:
        for u, basename in url_map.items():
            simplified_basename = simplify(basename)
            if simplified_basename in acronyms:
                best_u = u
                break

    # 3. Conservative Substring match (min length 4)
    if not best_u:
        # Exclude very common words from being matched as single substrings to avoid false positives
        excluded_words = {'rumah', 'peduli', 'berbagi', 'asnaf', 'sosial', 'umat', 'bersama', 'mitra', 'amal', 'salman', 'kasih', 'insan'}
        for u, basename in url_map.items():
            simplified_basename = simplify(basename)
            if not simplified_basename or not keyword or keyword in excluded_words or simplified_basename in excluded_words:
                continue
            if len(simplified_basename) >= 4 and (simplified_basename in keyword or keyword in simplified_basename):
                best_u = u
                break

    if best_u:
        mapping[opz] = best_u

# Print the clean JavaScript object representation
print("--- JavaScript Object ---")
js_lines = []
for k, v in sorted(mapping.items()):
    # Escape quotes
    k_esc = k.replace('"', '\\"')
    js_lines.append(f'            "{k_esc}": "{v}",')
print("\n".join(js_lines))
