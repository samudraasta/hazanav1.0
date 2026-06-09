with open('kurban2026.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the border from logos
css = css.replace("border: 1px solid #e2e8f0;", "border: none;")

with open('kurban2026.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Removed stroke from logos")
