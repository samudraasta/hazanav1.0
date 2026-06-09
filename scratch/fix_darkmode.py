with open('kurban2026.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace hardcoded white backgrounds with the CSS variable
css = css.replace('background: white;', 'background: var(--bg-card);')
css = css.replace('background-color: white;', 'background-color: var(--bg-card);')
css = css.replace('background: #fff;', 'background: var(--bg-card);')
css = css.replace('background: #ffffff;', 'background: var(--bg-card);')

with open('kurban2026.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Fixed white backgrounds to var(--bg-card)")
