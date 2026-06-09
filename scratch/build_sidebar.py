import os
import re

css_path = 'kurban2026.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Append sidebar styles if not already there
if '.dashboard-layout' not in css:
    sidebar_css = """
/* Dashboard Layout & Sidebar */
body {
  margin: 0;
  padding: 0;
}

.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-body);
}

.sidebar {
  width: 80px;
  background-color: #10b981;
  color: white;
  transition: width 0.3s ease;
  overflow: hidden;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  padding-top: 2rem;
  box-shadow: 4px 0 15px rgba(0,0,0,0.05);
  z-index: 100;
  position: relative;
}

.sidebar:hover {
  width: 250px;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  padding: 0 20px;
  margin-bottom: 3rem;
  overflow: hidden;
}

.sidebar-logo img {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.sidebar-logo span {
  margin-left: 15px;
  font-weight: 800;
  font-size: 1.2rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.sidebar:hover .sidebar-logo span {
  opacity: 1;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sidebar-menu li a {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.sidebar-menu li a i {
  width: 40px;
  font-size: 1.2rem;
  text-align: center;
  flex-shrink: 0;
}

.sidebar-menu li a span {
  margin-left: 5px;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.3s;
}

.sidebar:hover .sidebar-menu li a span {
  opacity: 1;
}

.sidebar-menu li a:hover, .sidebar-menu li.active a {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border-left-color: white;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  height: 100vh;
}

.app-container {
  /* Reset max-width if necessary, or let it center within main */
  max-width: 1440px;
  margin: 0 auto;
  width: 100%;
}
"""
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write("\n" + sidebar_css)
    print("Added sidebar CSS.")

html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Wrap in dashboard layout
if '<div class="dashboard-layout">' not in html:
    sidebar_html = """  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <!-- Temporary logo, using an icon if image not available -->
        <img src="logos_standard/Forum Zakat.png" alt="FOZ Logo" onerror="this.style.display='none'; this.nextElementSibling.style.marginLeft='0';">
        <span>FORUM ZAKAT</span>
      </div>
      <ul class="sidebar-menu">
        <li class="active"><a href="index.html"><i class="fas fa-sheep"></i> <span>Dashboard Kurban</span></a></li>
        <li><a href="ramadan.html"><i class="fas fa-moon"></i> <span>Dashboard Ramadhan</span></a></li>
      </ul>
    </aside>
    <main class="main-content">
"""
    
    html = html.replace('<body>', '<body>\n' + sidebar_html)
    
    # Close tags at the end of body
    html = html.replace('</body>', '    </main>\n  </div>\n</body>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html layout.")

print("Done building sidebar framework.")
