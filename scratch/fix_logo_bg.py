with open('kurban2026.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update .logo-item img
old_logo_item = """.logo-item img {
  width: 90px; /* Lebih besar */
  height: 52px;
  object-fit: contain;
  background: transparent;
  border: none; /* Tanpa stroke */
  padding: 0;
  box-shadow: none; /* Tanpa bayangan kotak */
}"""

new_logo_item = """.logo-item img {
  width: 90px;
  height: 52px;
  object-fit: contain;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}"""

if old_logo_item in css:
    css = css.replace(old_logo_item, new_logo_item)

# 2. Update .marquee-item img
old_marquee = """.marquee-item img {
  width: 65px;
  height: 65px;
  border-radius: 50%;
  object-fit: contain;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #f8fafc;
}"""

new_marquee = """.marquee-item img {
  width: 65px;
  height: 65px;
  border-radius: 50%;
  object-fit: contain;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: white;
  padding: 3px;
  border: 1px solid #e2e8f0;
}"""

if old_marquee in css:
    css = css.replace(old_marquee, new_marquee)

# 3. Remove dark mode overrides for logo background
css = css.replace("body.dark-mode .marquee-item img { background: #334155; }", "")
css = css.replace("body.dark-mode .logo-item img { filter: brightness(0.9) contrast(1.1); }", "/* logo filter removed */")

with open('kurban2026.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Logo backgrounds explicitly set to white!")
