# 🤖 AI Models Setup Guide

Your chatbot now supports **multiple AI models**! Here's how to set them up:

## 🎯 Quick Start (No Setup Required)

The chatbot works immediately with **rule-based responses** - no API keys needed!

## 🧠 AI Model Options

### 1️⃣ OpenAI GPT (Recommended for Best Quality)

**Models**: GPT-4, GPT-4o, GPT-4o-mini, GPT-3.5-turbo

**Setup**:
1. Go to https://platform.openai.com/api-keys
2. Create an account and add payment method
3. Generate an API key
4. Edit `.env` file and add:
   ```
   OPENAI_API_KEY=sk-your-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

**Cost**: 
- GPT-4o-mini: ~$0.15 per 1M input tokens (cheapest, recommended)
- GPT-3.5-turbo: ~$0.50 per 1M tokens
- GPT-4: ~$30 per 1M tokens

---

### 2️⃣ Google Gemini AI (Free Tier Available!)

**Models**: gemini-pro, gemini-1.5-pro

**Setup**:
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Edit `.env` file and add:
   ```
   GEMINI_API_KEY=your-key-here
   GEMINI_MODEL=gemini-pro
   ```

**Cost**: 
- **FREE tier**: 15 requests per minute, 1500 per day
- Paid tier available for higher limits

---

### 3️⃣ Ollama (Local, Free, Private)

**Models**: llama3.2, mistral, phi, etc.

**Setup**:
1. Download from https://ollama.ai/
2. Install and run Ollama
3. Run: `python setup_ollama.py`
4. No API key needed!

**Pros**: Free, private, works offline
**Cons**: Requires powerful computer, slower than cloud APIs

---

### 4️⃣ Hugging Face (Free Fallback)

**Models**: DialoGPT-medium

**Setup**:
1. Go to https://huggingface.co/settings/tokens
2. Create account and generate token
3. Edit `.env` file and add:
   ```
   HUGGING_FACE_API_KEY=your-token-here
   ```

**Cost**: Free (with rate limits)

---

## 🔄 How the Fallback Works

The chatbot tries models in this order:

```
1. Ollama (if installed)
   ↓ (if fails)
2. OpenAI GPT (if API key set)
   ↓ (if fails)
3. Google Gemini (if API key set)
   ↓ (if fails)
4. Hugging Face (if API key set)
   ↓ (if fails)
5. Rule-based responses (always works)
```

## 💡 Recommendations

**For Best Experience**:
- Add **Google Gemini** (free tier is generous!)
- Or add **OpenAI GPT-4o-mini** (cheap and excellent)

**For Privacy**:
- Use **Ollama** (runs locally, no data sent to cloud)

**For Free Usage**:
- Use **rule-based responses** (no setup)
- Or **Google Gemini free tier**

## 🚀 Testing Your Setup

1. Start the chatbot: `python app/chatbot.py`
2. Open http://localhost:5000
3. Type: "Hello, what AI model are you using?"
4. Check the terminal for which model responded

## 📝 Example .env File

```bash
# Choose one or more:

# OpenAI (Best quality, paid)
OPENAI_API_KEY=sk-proj-abc123...
OPENAI_MODEL=gpt-4o-mini

# Google Gemini (Good quality, free tier!)
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-pro

# Hugging Face (Free fallback)
HUGGING_FACE_API_KEY=hf_abc123...
```

## ❓ Need Help?

- Check the main README.md for more details
- Ensure your `.env` file is in the project root
- Restart the chatbot after adding API keys
- Check terminal output for error messages
