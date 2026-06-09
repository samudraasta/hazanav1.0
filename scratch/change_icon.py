files = ['index.html', 'ramadan.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace in the sidebar menu only
    # Example: <i class="fas fa-sheep"></i> <span>Dashboard Kurban</span>
    html = html.replace('<i class="fas fa-sheep"></i> <span>Dashboard Kurban</span>', '<i class="fas fa-goat"></i> <span>Dashboard Kurban</span>')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Icon changed to goat.")
