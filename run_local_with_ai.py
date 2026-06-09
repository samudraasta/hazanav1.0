import http.server
import socketserver
import json
import urllib.request
import os

PORT = 8080
DIRECTORY = "."

# Kunci API Gemini Anda
# Skrip ini akan otomatis mencari FOZI_API_KEY di environment komputer Anda.
# Jika Anda belum men-set FOZI_API_KEY di terminal, Anda bisa menempelkannya langsung
# pada baris di bawah ini sebagai teks, contoh: API_KEY = "AIzaSy..."
API_KEY = os.environ.get("FOZI_API_KEY", "") 

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/.netlify/functions/ask-gemini':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                body = json.loads(post_data.decode('utf-8'))
                prompt = body.get('prompt', '')
                context_data = body.get('contextData', '')
                
                if not API_KEY:
                    self.send_error_json(500, "FOZI_API_KEY belum dikonfigurasi di file run_local_with_ai.py")
                    return
                
                # Sistem Prompt
                system_instruction = f"""Kamu adalah Fozza, AI Asisten Kurban untuk Forum Zakat. 
Tugasmu adalah menjawab pertanyaan user berdasarkan data kurban berikut ini.
Gunakan bahasa yang profesional, ramah, ringkas, dan mudah dipahami.
Bila ditanya total, jumlahkan data bila perlu.
Bila data tidak ada di bawah ini, sampaikan bahwa datanya belum tersedia.

DATA KURBAN:
{context_data}"""

                # Siapkan request ke Gemini
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"
                payload = {
                    "contents": [{
                        "role": "user",
                        "parts": [{"text": system_instruction + "\n\nPertanyaan User: " + prompt}]
                    }]
                }
                
                req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                
                try:
                    response = urllib.request.urlopen(req)
                    response_data = json.loads(response.read().decode('utf-8'))
                    
                    reply_text = "Maaf, saya tidak bisa memproses jawaban saat ini."
                    if 'candidates' in response_data and response_data['candidates']:
                        reply_text = response_data['candidates'][0]['content']['parts'][0]['text']
                        
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"reply": reply_text}).encode('utf-8'))
                    
                except urllib.error.HTTPError as e:
                    error_msg = e.read().decode('utf-8')
                    self.send_error_json(500, f"Error dari Gemini API: {error_msg}")
                    
            except Exception as e:
                self.send_error_json(500, f"Internal Server Error: {str(e)}")
        else:
            self.send_error(404, "File not found")

    def send_error_json(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode('utf-8'))

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"🚀 Server lokal dengan AI berjalan di http://localhost:{PORT}")
    print("Tekan Ctrl+C untuk menghentikan server.")
    if not API_KEY:
        print("⚠️  PERINGATAN: FOZI_API_KEY belum terisi! Silakan edit file run_local_with_ai.py")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
