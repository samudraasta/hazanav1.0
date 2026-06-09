import re

files = ['index.html', 'ramadan.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove autoplay attribute
    html = html.replace('<audio id="mars-audio" autoplay loop preload="auto">', '<audio id="mars-audio" loop preload="auto">')
    
    # The JS initially tries to play and sets the icon based on promise.
    # We want it to NOT play initially, just set the icon to mute.
    # Let's replace the initial play block.
    # It looks like:
    # marsAudio.play().then(() => {
    #    audioBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
    # }).catch(error => {
    #    // Auto-play was prevented
    #    audioBtn.innerHTML = '<i class="fas fa-volume-mute"></i>';
    # });
    
    pattern = re.compile(r'marsAudio\.play\(\)\.then\(\(\) => \{.*?\}\)\.catch\(error => \{.*?\}\);', re.DOTALL)
    replacement = "audioBtn.innerHTML = '<i class=\"fas fa-volume-mute\"></i>';"
    html = pattern.sub(replacement, html)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Autoplay disabled in all HTML files.")
