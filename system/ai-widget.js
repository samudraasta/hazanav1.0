// AI Assistant Widget Logic
(function() {
  // Sementara di-hide sesuai permintaan
  return;

  const aiHtml = `
    <div class="ai-fab" id="ai-fab">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"></path>
        <path d="M20 3v4"></path>
        <path d="M22 5h-4"></path>
        <path d="M4 17v2"></path>
        <path d="M5 18H3"></path>
      </svg>
    </div>
    <div class="ai-chat-window" id="ai-chat-window">
      <div class="ai-header">
        <div style="display:flex; align-items:center; gap:0.5rem;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"></path>
            <path d="M20 3v4"></path>
            <path d="M22 5h-4"></path>
            <path d="M4 17v2"></path>
            <path d="M5 18H3"></path>
          </svg> Fozza, AI Asisten
        </div>
        <div class="close-btn" id="ai-close"><i class="fas fa-times"></i></div>
      </div>
      <div class="ai-body" id="ai-body">
        <div class="chat-msg bot">
          Assalamu'alaikum Warahmatullahi Wabarakatuh! 🙏<br><br>
          Ahlan wa sahlan, perkenalkan saya <strong>Fozza</strong>. Alhamdulillah, saya telah mempelajari seluruh data kurban di dashboard ini.<br><br>
          Insyaallah, saya siap membantu Anda.
        </div>
      </div>
      <div class="ai-input-area">
        <input type="text" id="ai-input" placeholder="Tanya sesuatu...">
        <button id="ai-send"><i class="fas fa-paper-plane"></i></button>
      </div>
    </div>
  `;

  const container = document.createElement('div');
  container.innerHTML = aiHtml;
  document.body.appendChild(container);

  const aiFab = document.getElementById('ai-fab');
  const aiChat = document.getElementById('ai-chat-window');
  const aiClose = document.getElementById('ai-close');
  const aiInput = document.getElementById('ai-input');
  const aiSend = document.getElementById('ai-send');
  const aiBody = document.getElementById('ai-body');

  aiFab.addEventListener('click', () => { aiChat.classList.add('active'); aiInput.focus(); });
  aiClose.addEventListener('click', () => { aiChat.classList.remove('active'); });

  function addMsg(text, sender) {
    const d = document.createElement('div');
    d.className = `chat-msg ${sender}`;
    // Basic Markdown parser for bold and bullets
    let formattedText = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/(?:^|\n)\* (.*)/g, '<br>• $1')
      .replace(/\n/g, '<br>');
    // Clean up duplicate breaks
    formattedText = formattedText.replace(/<br><br>•/g, '<br>•').replace(/^<br>/, '');
    d.innerHTML = formattedText;
    aiBody.appendChild(d);
    aiBody.scrollTop = aiBody.scrollHeight;
  }

  function showTyping() {
    const d = document.createElement('div');
    d.className = `chat-msg bot typing-indicator`;
    d.id = 'typing-indicator';
    d.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> AI sedang berpikir...';
    aiBody.appendChild(d);
    aiBody.scrollTop = aiBody.scrollHeight;
  }

  function removeTyping() {
    const d = document.getElementById('typing-indicator');
    if (d) d.remove();
  }

  async function processQuery(q) {
    let data = window.appTableData || [];
    if(data.length === 0) return "Maaf, data belum selesai dimuat.";
    
    let totalPenghimpunan = 0;
    let contextData = data.map(d => {
      totalPenghimpunan += d.penghimpunan;
      return `- ${d.nama}: Himpun Rp${d.penghimpunan}, ${d.pekurban} pekurban, ${d.penerima} penerima.`;
    }).join('\n');
    
    // Inject total aggregating to save Gemini's calculation time
    contextData = `TOTAL SELURUH PENGHIMPUNAN DARI SEMUA LEMBAGA: Rp${totalPenghimpunan}\n\n` + contextData;
    
    try {
      const response = await fetch('/.netlify/functions/ask-gemini', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: q, contextData: contextData })
      });
      
      const textResponse = await response.text();
      try {
        const result = JSON.parse(textResponse);
        if (response.ok) {
          return result.reply;
        } else {
          console.error("API Error:", result);
          return "Server AI Error: " + (result.error || "") + " " + (result.details ? JSON.stringify(result.details) : JSON.stringify(result));
        }
      } catch (parseErr) {
        if (textResponse.includes("Function timeout") || response.status === 502 || textResponse.includes("<html")) {
          return "⏳ Mohon maaf, pertanyaan Anda membutuhkan waktu hitung yang terlalu lama sehingga diputus oleh server (Timeout 10 detik). Coba tanyakan pertanyaan yang lebih spesifik atau sederhana.";
        }
        throw new Error("Gagal mem-parsing JSON: " + textResponse.substring(0, 50));
      }
    } catch (e) {
      console.error("Fetch Error:", e);
      return "Gagal menghubungi server AI. Error: " + e.message;
    }
  }

  async function handleSend() {
    let val = aiInput.value.trim();
    if(!val) return;
    
    addMsg(val, 'user');
    aiInput.value = '';
    aiInput.disabled = true;
    
    showTyping();
    
    let ans = await processQuery(val);
    
    removeTyping();
    addMsg(ans, 'bot');
    aiInput.disabled = false;
    aiInput.focus();
  }

  aiSend.addEventListener('click', handleSend);
  aiInput.addEventListener('keypress', (e) => {
    if(e.key === 'Enter') handleSend();
  });
})();
