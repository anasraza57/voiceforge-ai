## 🗣️ Voice Cloner SaaS MVP (Hybrid Stack)

This project uses Node.js (API), Python (AI inference), and React (UI-ready) with Docker for scalable TTS & cloning.

### 🔧 Run Locally
```bash
docker-compose up --build
```

Send requests via Postman or curl:
```bash
curl -X POST http://localhost:3001/api/tts \
  -F "voice_sample=@example.wav" \
  -F "text=Hello, how are you?" --output result.wav
```