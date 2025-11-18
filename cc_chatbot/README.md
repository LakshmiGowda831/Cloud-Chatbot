# 🤖 Cloudy AI Chatbot

A sophisticated, multi-AI-powered chatbot with a cloud-themed personality that combines multiple AI models for intelligent, reliable conversations.

![Cloudy AI](https://img.shields.io/badge/Cloudy-AI_Chatbot-blue?style=for-the-badge&logo=cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-red?style=for-the-badge&logo=flask&logoColor=white)

## ✨ Features

- **🧠 Multi-AI Intelligence**: Supports OpenAI GPT-4, Google Gemini, Ollama, and Hugging Face
- **☁️ Cloud-Themed Personality**: Friendly "Cloudy" assistant with cloud computing expertise
- **🔄 Smart Fallback System**: Automatic failover between AI models for maximum reliability
- **💾 Conversation Memory**: Remembers user context and conversation history
- **🎨 Modern Web UI**: Beautiful, responsive interface with real-time chat
- **🔍 Web Search Integration**: DuckDuckGo search for current information
- **⚡ Security Features**: XSS protection and input sanitization
- **📱 Mobile Responsive**: Works seamlessly on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Git (for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cc_chatbot/cc_chatbot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the chatbot**
   ```bash
   python app/chatbot.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 AI Model Priority

The chatbot automatically tries AI models in this order:

1. **🦙 Ollama (Local, Free)**
   - Uses `llama3.2:1b` model by default
   - Runs locally on your machine
   - No API key required
   - Private and fast

2. **🤖 OpenAI GPT (Cloud, Paid)**
   - Supports GPT-4, GPT-4o, GPT-3.5-turbo
   - Most advanced responses
   - Requires API key

3. **✨ Google Gemini (Cloud, Free/Paid)**
   - Uses Gemini Pro or Gemini 1.5 Pro
   - Google's powerful AI
   - Free tier available

4. **🤗 Hugging Face (Cloud, Free)**
   - Uses DialoGPT model
   - Optional API key

5. **📝 Rule-Based (Always Available)**
   - Intelligent pattern matching
   - Works offline
   - Covers common topics

## 🔧 Configuration

### API Keys Setup

Create/edit the `.env` file:

```bash
# OpenAI GPT Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Google Gemini Configuration  
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro

# Hugging Face (Optional)
HUGGING_FACE_API_KEY=your_hf_token_here
```

### Ollama Setup (Optional but Recommended)

1. **Install Ollama**
   ```bash
   # Download from https://ollama.ai/
   # Or use the setup script
   python setup_ollama.py
   ```

2. **Download AI models**
   ```bash
   python manage_ollama.py
   ```

3. **Available models**
   - `llama3.2:1b` - Fast, lightweight (1GB)
   - `llama3.2:3b` - Better quality (2GB)
   - `llama3.1:8b` - High quality (4.7GB)
   - `mistral:7b` - Alternative model (4.1GB)

## 📁 Project Structure

```
cc_chatbot/
├── app/
│   ├── chatbot.py              # Main Flask application
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Modern UI styling
│   │   └── js/
│   │       └── script.js       # Interactive frontend
│   └── templates/
│       └── index.html          # Chat interface
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── setup_ollama.py            # Ollama setup script
├── manage_ollama.py           # Model management
└── README.md                  # This file
```

## 🎨 UI Features

- **Real-time Chat**: Instant messaging interface
- **Typing Indicators**: Shows when AI is thinking
- **Message History**: Scrollable conversation log
- **New Chat Button**: Start fresh conversations
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during API calls
- **Responsive Design**: Works on desktop and mobile

## 🧩 Intelligent Responses

The chatbot excels at:

- **☁️ Cloud Computing**: In-depth knowledge of AWS, Azure, GCP
- **💻 Programming**: Python, algorithms, debugging help
- **🔬 Science**: Physics, chemistry, biology explanations
- **📊 Mathematics**: Calculus, statistics, problem-solving
- **🌐 Web Search**: Current events and real-time information
- **💬 Natural Conversation**: Context-aware responses

## 🔒 Security Features

- **XSS Protection**: Sanitized user inputs
- **CSRF Protection**: Secure session management
- **Input Validation**: Prevents malicious inputs
- **Safe Defaults**: Secure configuration out of the box

## 🛠️ Development

### Running Tests
```bash
python test_chatbot.py
```

### Debug Mode
The app runs in debug mode by default. Check `debug.log` for:
- API call details
- Error messages
- Conversation logs
- Performance metrics

### Customization

1. **Change AI Model Priority**
   Edit `app/chatbot.py` to reorder the fallback chain

2. **Modify Personality**
   Update system prompts in the AI response functions

3. **Add New Responses**
   Extend `get_intelligent_fallback()` function

## 📊 Performance

- **Response Time**: <2 seconds with local models
- **Memory Usage**: ~4-6GB with Ollama
- **CPU Usage**: Minimal for rule-based responses
- **Network**: Optional (only for cloud AI models)

## 🚀 Deployment

### Local Development
```bash
python app/chatbot.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.chatbot:app
```

### Docker (Coming Soon)
```dockerfile
# Dockerfile example coming soon
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

**Q: Chatbot not responding?**
A: Check debug.log for errors. Ensure at least one AI model is configured.

**Q: Ollama not working?**
A: Run `python manage_ollama.py` to check status and download models.

**Q: API key errors?**
A: Verify your .env file contains correct API keys.

**Q: Slow responses?**
A: Use local Ollama model for faster responses.

### Getting Help

- Check the debug log file
- Ensure all dependencies are installed
- Verify API keys are correct
- Test with different AI models

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/cc_chatbot&type=Date)](https://star-history.com/#your-username/cc_chatbot&Date)

---

**Made with ❤️ by the Cloudy AI Team**

*Experience the future of conversational AI with multiple intelligence layers working together for the best possible responses.*
