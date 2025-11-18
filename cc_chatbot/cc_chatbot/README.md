# 🤖 Cloud Chatbot with Multi-AI Intelligence

A smart chatbot powered by **multiple AI models** including OpenAI GPT, Google Gemini, and Ollama, with intelligent fallback for maximum reliability.

## 🚀 Features

- **🧠 Multiple AI Models**: Supports OpenAI GPT-4/GPT-3.5, Google Gemini, Ollama, and Hugging Face
- **☁️ Cloud-Themed Personality**: Friendly "Cloudy" assistant with cloud computing knowledge  
- **🔄 Smart Fallback Chain**: Ollama → OpenAI GPT → Google Gemini → Hugging Face → Rule-based
- **💾 Memory System**: Remembers user names and context
- **🎨 Beautiful UI**: Modern, responsive web interface with XSS protection
- **⚡ Fast & Secure**: Enter key support, loading states, error handling

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Ollama** installed on your system

## 🛠️ Installation

### Step 1: Install Ollama
1. Go to [https://ollama.ai/](https://ollama.ai/)
2. Download Ollama for Windows
3. Install and run the application

### Step 2: Setup the Chatbot
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the setup script to download AI model
python setup_ollama.py
```

### Step 3: Run the Chatbot
```bash
python app/chatbot.py
```

Visit `http://localhost:5000` in your browser to start chatting!

## 🎯 How It Works

### Intelligence Levels (in order of priority):

1. **🧠 Ollama AI Model** (Local, Free)
   - Uses `llama3.2:1b` model for intelligent responses
   - Runs locally on your machine, no API key needed
   - Fast and private

2. **🤖 OpenAI GPT** (Cloud, Paid)
   - Supports GPT-4, GPT-4o, GPT-4o-mini, GPT-3.5-turbo
   - Most advanced AI responses
   - Requires API key from OpenAI

3. **✨ Google Gemini AI** (Cloud, Free/Paid)
   - Uses Gemini Pro or Gemini 1.5 Pro
   - Google's powerful AI model
   - Requires API key (free tier available)

4. **🤗 Hugging Face API** (Cloud, Free)
   - Uses DialoGPT model
   - Requires API key (optional)

5. **📝 Rule-Based Responses** (Always Available)
   - Simple pattern matching for basic conversations
   - Always works, no dependencies or API keys needed

## 🔧 Configuration

### Change AI Model
Edit `app/chatbot.py` line 12:
```python
OLLAMA_MODEL = "llama3.2:1b"  # Change to any model you have
```

Popular models you can try:
- `llama3.2:1b` - Fast, lightweight (1GB)
- `llama3.2:3b` - Better quality (2GB) 
- `llama3.1:8b` - High quality (4.7GB)
- `mistral:7b` - Alternative model (4.1GB)

### Add API Keys (Optional)

Edit the `.env` file to add your API keys:

```bash
# OpenAI GPT (GPT-4, GPT-3.5-turbo, etc.)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini  # or gpt-4, gpt-3.5-turbo

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro  # or gemini-1.5-pro

# Hugging Face (optional fallback)
HUGGING_FACE_API_KEY=your_hf_token_here
```

**Where to get API keys:**
- **OpenAI**: https://platform.openai.com/api-keys (Paid, $0.15-$60 per 1M tokens)
- **Google Gemini**: https://makersuite.google.com/app/apikey (Free tier available!)
- **Hugging Face**: https://huggingface.co/settings/tokens (Free)

## 💬 Example Conversations

**User**: "My name is John, tell me about cloud computing"  
**Cloudy**: "Nice to meet you, John! Cloud computing offers scalable, on-demand access to computing resources..."

**User**: "What's my name?"  
**Cloudy**: "Your name is John! I remember you! 😊"

**User**: "Explain quantum physics in simple terms"  
**Cloudy**: "Quantum physics is like the rules for the tiniest particles in the universe..."

## 🐛 Troubleshooting

### Ollama Not Working?
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama service
ollama serve

# Pull the model manually
ollama pull llama3.2:1b
```

### Python Dependencies Issues?
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 🎨 Customization

### Change Personality
Edit the `system_prompt` in `get_ollama_response()` function to customize Cloudy's personality.

### Add New Features
- Modify `app/chatbot.py` for backend logic
- Edit `templates/index.html` for UI changes
- Add new routes for additional functionality

## 📁 Project Structure
```
cloud_chatbot/
├── app/
│   ├── chatbot.py          # Main Flask application
│   └── templates/
│       └── index.html      # Web interface
├── requirements.txt        # Python dependencies
├── setup_ollama.py        # Setup script
└── README.md              # This file
```

## 🤝 Contributing

Feel free to fork this project and add new features:
- Voice input/output
- Multiple language support
- Database integration for persistent memory
- Docker containerization

## 📄 License

This project is open source and available under the MIT License.

---

**Made with ❤️ and ☁️ by the Cloud Chatbot Team**
