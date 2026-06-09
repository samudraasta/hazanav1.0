const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const newMappingStr = `
{
  "Itqan Peduli": "https://forumzakat.org/wp-content/uploads/2022/12/128.-Itqan-100x57.png",
  "ZIS Yayasan Annur Insan Pembangkitan (YANIP)": "https://forumzakat.org/wp-content/uploads/2025/12/yanip-100x57.png",
  "Baitul Maal BMT Beringharjo": "https://forumzakat.org/wp-content/uploads/2025/12/bmt-beringharjo-100x57.png",
  "Yuk Peduli": "https://forumzakat.org/wp-content/uploads/2022/12/119.-Yuk-Peduli-100x57.png",
  "Explore! Humanity": "https://forumzakat.org/wp-content/uploads/2022/12/182.-Explore-100x57.png",
  "Amaliah Astra": "https://forumzakat.org/wp-content/uploads/2025/12/amaliah-astra-100x57.png",
  "Pelopor Kepedulian": "https://forumzakat.org/wp-content/uploads/2022/12/97.-PELOPOR-100x57.png",
  "Yayasan Rute Langkah Amanah": "https://forumzakat.org/wp-content/uploads/2025/12/rute-langkah-amanah-100x57.png",
  "LAZ DPU Kaltim": "https://forumzakat.org/wp-content/uploads/2022/12/81.-DPU-Kaltim-100x57.png",
  "LAZ SAKU YATIM INDONESIA": "https://forumzakat.org/wp-content/uploads/2022/12/188.-Saku-Yatim-100x57.png",
  "LAZ Lidzikri": "https://forumzakat.org/wp-content/uploads/2022/12/50.-Lidzikri-100x57.png",
  "LAZ DASI NTB": "https://forumzakat.org/wp-content/uploads/2022/12/39.-DASI-NTB-100x57.png",
  "LAZIS Jateng": "https://forumzakat.org/wp-content/uploads/2022/12/24.-LAZIS-JATENG-100x57.png",
  "Harapan Amal Mulia": "https://forumzakat.org/wp-content/uploads/2022/12/88.-mulia-100x57.png",
  "LAZ YASA Malang": "https://forumzakat.org/wp-content/uploads/2022/12/55.-YASA-Malang-100x57.png",
  "LAZ Sahabat Kebaikan Umat (SAKU)": "https://forumzakat.org/wp-content/uploads/2022/12/159.-SAKU-100x57.png",
  "LAZIS Muhammadiyah (LAZISMU)": "https://forumzakat.org/wp-content/uploads/2022/12/12.-lazismu-100x57.png",
  "BSI Maslahat": "https://forumzakat.org/wp-content/uploads/2022/12/18.-BSI-Maslahat-100x57.png",
  "LAZNAS YDSF": "https://forumzakat.org/wp-content/uploads/2022/12/09.-YDSF-100x57.png",
  "LAZ Masjid Raya Bintaro (LAZ MRBJ)": "https://forumzakat.org/wp-content/uploads/2022/12/173.-LAZ-MRBJ-100x57.png",
  "LAZIS UNISIA": "https://forumzakat.org/wp-content/uploads/2022/12/155.-LAZIS-UNISIA-100x57.png",
  "LAZ Al Bunyan": "https://forumzakat.org/wp-content/uploads/2022/12/45.-Al-Bunyan-100x57.png",
  "LAZIS Sultan Agung": "https://forumzakat.org/wp-content/uploads/2022/12/85.-Sultan-Agung-100x57.png",
  "Sinergi Foundation": "https://forumzakat.org/wp-content/uploads/2022/12/68.-Sinergi-Fond-300x171.png",
  "LAZ SOLOPEDULI": "https://forumzakat.org/wp-content/uploads/2022/12/34.-solopeduli-100x57.png",
  "Inisiatif Zakat Indonesia (IZI)": "https://forumzakat.org/wp-content/uploads/2022/12/03.-IZI-100x57.png",
  "Yayasan Gugus Karya Mandiri": "https://forumzakat.org/wp-content/uploads/2023/03/164.-Gugus-Karya-Mandiri-100x57.png",
  "ZIS Indosat": "https://forumzakat.org/wp-content/uploads/2022/12/36.-ZIS-Indosat-100x57.png",
  "LAZNAS Mizan Amanah": "https://forumzakat.org/wp-content/uploads/2022/12/129.-Mizan-100x57.png",
  "LAZ RIZKI": "https://forumzakat.org/wp-content/uploads/2022/12/105.-RIZKI-100x57.png",
  "Bangkit Foundation": "https://forumzakat.org/wp-content/uploads/2022/12/27.-Bangkit-Fond-300x171.png",
  "LAZ BMBU Kota Bontang": "https://forumzakat.org/wp-content/uploads/2022/12/156.-BMBU-100x57.png",
  "LAZ Persada Jatim Indonesia": "https://forumzakat.org/wp-content/uploads/2022/12/193.-Persada-100x57.png"
}`;

const newMap = JSON.parse(newMappingStr);

const match = html.match(/const fozLogos = (\{[\s\S]*?\});/);
if (match) {
    let oldMap = {};
    eval('oldMap = ' + match[1]);
    const merged = { ...oldMap, ...newMap };
    const replacement = 'const fozLogos = ' + JSON.stringify(merged, null, 12) + ';';
    const newHtml = html.replace(/const fozLogos = \{[\s\S]*?\};/, replacement);
    fs.writeFileSync('index.html', newHtml, 'utf8');
    console.log("Replaced successfully!");
} else {
    console.log("Could not find fozLogos block");
}
