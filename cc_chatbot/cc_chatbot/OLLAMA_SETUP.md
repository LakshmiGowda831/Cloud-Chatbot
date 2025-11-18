# 🤖 Ollama Setup Guide for Cloudy AI Chatbot

## Current Status
Your chatbot is now configured to use **Ollama as the primary AI model**, which runs locally on your computer and uses your system resources.

## What's Happening Now
- ⬇️ **Downloading**: `llama3.2:3b` model (2GB) - this may take 10-15 minutes
- 🔧 **Configured**: Chatbot will prioritize Ollama over cloud services
- 💻 **Local AI**: No internet required for AI responses once setup

## Benefits of Using Ollama
✅ **Privacy**: All AI processing happens on your computer  
✅ **No API Costs**: Free to use once installed  
✅ **Offline Capable**: Works without internet connection  
✅ **Fast Responses**: Direct access to your hardware  
✅ **Customizable**: You control the model and parameters  

## Model Information
- **Model**: `llama3.2:3b` (3 billion parameters)
- **Size**: ~2GB download
- **Quality**: Good balance of speed and intelligence
- **RAM Usage**: ~4-6GB when running

## How to Check Progress

### Option 1: Use the Management Tool
```bash
python manage_ollama.py
```

### Option 2: Manual Commands
```bash
# Check download progress
"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe" ps

# List available models
"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe" list

# Test a model
"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe" run llama3.2:3b "Hello!"
```

## After Download Completes

1. **Start the Chatbot**:
   ```bash
   python app/chatbot.py
   ```

2. **You'll see**:
   ```
   ✅ Ollama: Available with 1 model(s)
      🤖 Primary Model: llama3.2:3b
      ✅ llama3.2:3b is ready!
   ```

3. **Test it**: Open browser and chat - responses will come from your local Ollama!

## Troubleshooting

### If Ollama Service Won't Start
```bash
# Manually start Ollama service
"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe" serve
```

### If Model Download Fails
```bash
# Retry download
"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe" pull llama3.2:3b
```

### If You Want a Different Model
```bash
# Smaller, faster model (1GB)
"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe" pull llama3.2:1b

# Larger, smarter model (4GB)
"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe" pull llama3.1:8b
```

## Performance Tips

### For Better Speed:
- Close other heavy applications
- Ensure 8GB+ RAM available
- Use SSD storage if possible

### For Better Quality:
- Upgrade to larger model (8b or 13b)
- Increase `num_predict` in chatbot.py
- Adjust `temperature` for creativity

## Configuration Files

### Main Config: `app/chatbot.py`
```python
OLLAMA_MODEL = "llama3.2:3b"  # Change model here
```

### Response Parameters:
```python
options={
    'temperature': 0.8,      # Creativity (0.1-1.0)
    'num_predict': 300,      # Max response length
    'repeat_penalty': 1.1,   # Reduce repetition
}
```

## Next Steps

1. ⏳ **Wait** for download to complete
2. 🚀 **Start** the chatbot: `python app/chatbot.py`
3. 💬 **Test** local AI responses
4. 🎛️ **Customize** model settings if needed
5. 📊 **Monitor** system resources during use

## Need Help?

- Run `python manage_ollama.py` for interactive management
- Check the console output when starting the chatbot
- Monitor system RAM usage (should be <8GB total)

---
**Note**: The first response from Ollama may be slower as it loads the model into memory. Subsequent responses will be much faster!
