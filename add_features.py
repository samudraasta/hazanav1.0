import re

with open('kurban2026.css', 'r') as f:
    css = f.read()

# Add Dark Mode and Footer CSS
dark_css = """
/* Dark Mode Overrides */
body.dark-mode {
  --bg-app: #0f172a;
  --bg-card: #1e293b;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-dark: #f1f5f9;
  --border-color: #334155;
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.3);
  --shadow-md: 0 8px 20px rgba(0,0,0,0.4);
}
body.dark-mode .nav-pills { background: #334155; }
body.dark-mode .nav-btn { color: #cbd5e1; }
body.dark-mode .tab-nav { background: #334155; }
body.dark-mode .modal-header { background: #1e293b; border-bottom: 1px solid #334155;}
body.dark-mode .logo-item img { filter: brightness(0.9) contrast(1.1); }
body.dark-mode .stat-label { color: #cbd5e1; }
body.dark-mode .logos-section { background: #1e293b; }

/* Toggle Buttons */
.header-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.action-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: var(--shadow-sm);
}
.action-btn:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
  border-color: var(--primary);
}
body.dark-mode .action-btn:hover {
  background: var(--primary-dark);
  color: white;
}

/* Footer Credit */
.footer-credit {
  text-align: center;
  margin-top: 3rem;
  padding: 1.5rem 0;
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 500;
  border-top: 1px dashed var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.footer-credit i {
  color: var(--primary);
  font-size: 1.1rem;
}
"""

if "body.dark-mode" not in css:
    with open('kurban2026.css', 'a') as f:
        f.write("\n" + dark_css)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add buttons
buttons_html = """
      <div class="header-actions">
        <button id="audio-toggle" class="action-btn" title="Nyalakan Mars Zakat">
          <i class="fas fa-volume-mute"></i>
        </button>
        <button id="theme-toggle" class="action-btn" title="Ganti Tema">
          <i class="fas fa-moon"></i>
        </button>
      </div>
"""
if 'class="header-actions"' not in html:
    html = html.replace('<div class="page-title">', '<div class="page-header" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">\n      <div class="page-title">')
    html = html.replace('</div>\n    </div>\n\n    <!-- Stats Row 1 -->', '</div>\n' + buttons_html + '    </div>\n\n    <!-- Stats Row 1 -->')

# Add Audio tag & Footer
audio_footer_html = """
    <div class="footer-credit">
      <i class="fas fa-handshake"></i> Jabat Erat Forum Zakat
    </div>
    
    <audio id="mars-audio" loop preload="none">
       <!-- Nanti ganti dengan URL Mars Zakat -->
       <source src="mars_zakat.mp3" type="audio/mpeg">
    </audio>
  </div>
"""
if 'class="footer-credit"' not in html:
    html = html.replace('</div>\n\n  <!-- Fullscreen Map Modal -->', audio_footer_html + '\n\n  <!-- Fullscreen Map Modal -->')

# Add JS logic
js_logic = """
    // Dark Mode Logic
    const themeBtn = document.getElementById('theme-toggle');
    if (localStorage.getItem('theme') === 'dark') {
      document.body.classList.add('dark-mode');
      themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
    }
    themeBtn.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
      } else {
        localStorage.setItem('theme', 'light');
        themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
      }
    });

    // Audio Logic
    const audioBtn = document.getElementById('audio-toggle');
    const marsAudio = document.getElementById('mars-audio');
    let isPlaying = false;
    audioBtn.addEventListener('click', () => {
      if (isPlaying) {
        marsAudio.pause();
        audioBtn.innerHTML = '<i class="fas fa-volume-mute"></i>';
        isPlaying = false;
      } else {
        marsAudio.play().catch(e => alert('Pastikan file mars_zakat.mp3 ada di folder ini!'));
        audioBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
        isPlaying = true;
      }
    });
"""
if 'Dark Mode Logic' not in html:
    html = html.replace('// Start Fetching Data', js_logic + '\n      // Start Fetching Data')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
