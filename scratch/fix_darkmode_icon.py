with open('kurban2026.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = "body.dark-mode .marquee-item img { background: #334155; }"
replacement = target + "\nbody.dark-mode .stat-icon.dark { background: rgba(255, 255, 255, 0.1); color: #f8fafc; }"

if target in css:
    css = css.replace(target, replacement)
    with open('kurban2026.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Icon dark mode fix applied successfully!")
else:
    print("Target string not found!")
