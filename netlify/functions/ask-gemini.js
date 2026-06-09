exports.handler = async function(event, context) {
  // Only allow POST
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const apiKey = process.env.FOZI_API_KEY || process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, body: JSON.stringify({ error: "API Key not configured." }) };
  }

  try {
    const body = JSON.parse(event.body);
    const { prompt, contextData } = body;

    if (!prompt) {
      return { statusCode: 400, body: JSON.stringify({ error: "Prompt is required." }) };
    }

    // Prepare system prompt for Gemini
    const systemInstruction = `Kamu adalah Fozza, AI Asisten Kurban untuk Forum Zakat. 
Tugasmu adalah menjawab pertanyaan user berdasarkan data kurban berikut ini.
Gunakan bahasa yang profesional, ramah, ringkas, dan mudah dipahami.
Bila ditanya total, jumlahkan data bila perlu.
Bila data tidak ada di bawah ini, sampaikan bahwa datanya belum tersedia.

DATA KURBAN:
${contextData}`;

    // Google Gemini API Request Payload
    const payload = {
      contents: [
        {
          role: "user",
          parts: [{ text: systemInstruction + "\n\nPertanyaan User: " + prompt }]
        }
      ]
    };

    // Call Gemini API using native fetch
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key=${apiKey}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("Gemini API Error:", data);
      return { statusCode: 500, body: JSON.stringify({ error: "Gagal memproses ke Gemini API.", details: data }) };
    }

    // Extract text from Gemini response
    let replyText = "Maaf, saya tidak bisa memproses jawaban saat ini.";
    if (data.candidates && data.candidates[0].content && data.candidates[0].content.parts) {
      replyText = data.candidates[0].content.parts[0].text;
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ reply: replyText })
    };
  } catch (error) {
    console.error("Function Error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error" })
    };
  }
};
