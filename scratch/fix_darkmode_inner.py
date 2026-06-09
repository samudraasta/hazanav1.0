with open('kurban2026.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = "body.dark-mode .logos-section { background: #1e293b; }"
replacement = target + """
body.dark-mode .country-item,
body.dark-mode .leaderboard-item,
body.dark-mode .map-placeholder {
  background: rgba(255, 255, 255, 0.05);
}
body.dark-mode .insight-section {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-color: #334155;
}
body.dark-mode .btn:hover { background: rgba(255, 255, 255, 0.1); }
body.dark-mode .marquee-item img { background: #334155; }
"""

if target in css:
    css = css.replace(target, replacement)
    with open('kurban2026.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Inner dark mode fixes applied successfully!")
else:
    print("Target string not found!")
