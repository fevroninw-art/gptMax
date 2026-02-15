import os
from flask import Flask, request, jsonify, Response
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")
APP_TITLE = os.getenv("APP_TITLE", "GPT в MAX")

HTML = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{APP_TITLE}</title>

  <meta property="og:title" content="{APP_TITLE}" />
  <meta property="og:description" content="Задай вопрос — получи ответ от GPT." />
  <meta name="description" content="Задай вопрос — получи ответ от GPT." />

  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 0; background:#f6f7fb; }}
    .wrap {{ max-width: 720px; margin: 0 auto; padding: 16px; }}
    .card {{ background:#fff; border-radius:16px; padding:16px; box-shadow: 0 6px 20px rgba(0,0,0,.06); }}
    h1 {{ font-size: 20px; margin: 0 0 12px; }}
    textarea {{ width: 100%; min-height: 110px; padding: 12px; border-radius: 12px; border: 1px solid #ddd; resize: vertical; }}
    button {{ width: 100%; margin-top: 10px; padding: 12px; border-radius: 12px; border: 0; font-size: 16px; }}
    pre {{ white-space: pre-wrap; word-wrap: break-word; background:#0b1020; color:#e8e8e8; padding:12px; border-radius:12px; margin-top: 12px; }}
    .muted {{ color:#666; font-size: 12px; margin-top: 10px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>{APP_TITLE}</h1>
      <textarea id="q" placeholder="Напиши вопрос..."></textarea>
      <button id="btn">Отправить</button>
      <pre id="a" style="display:none"></pre>
      <div class="muted">Совет: закрепи эту ссылку в группе MAX.</div>
    </div>
  </div>

<script>
const btn = document.getElementById("btn");
const q = document.getElementById("q");
const a = document.getElementById("a");

btn.onclick = async () => {{
  const text = q.value.trim();
  if (!text) return;

  btn.disabled = true;
  btn.textContent = "Думаю...";
  a.style.display = "block";
  a.textContent = "";

  try {{
    const r = await fetch("/chat", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ question: text }})
    }});
    const j = await r.json();
    a.textContent = j.answer || "Нет ответа";
  }} catch (e) {{
    a.textContent = "Ошибка связи с сервером";
  }} finally {{
    btn.disabled = false;
    btn.textContent = "Отправить";
  }}
}};
</script>
</body>
</html>
"""

@app.get("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"answer": "Напиши вопрос текстом."}), 400

    resp = client.responses.create(
        model=MODEL,
        input=question
    )

    answer = (resp.output_text or "").strip() or "..."
    return jsonify({"answer": answer})


@app.get("/health")
def health():
    return "ok", 200
