from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
import requests
import json
import random
from datetime import datetime

# Optional: Try to import web search libraries
try:
    from duckduckgo_search import DDGS
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Optional: Try to import AI libraries, but don't crash if not installed
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# 🔹 Load .env from project root
load_dotenv()  # Automatically picks up .env file

# 🔹 Ollama Configuration
OLLAMA_MODEL = "llama3.2:1b"  # Using 1B model for better compatibility with system memory

# 🔹 OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Default to gpt-4o-mini, can use gpt-4, gpt-3.5-turbo, etc.

if OPENAI_AVAILABLE and OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

# 🔹 Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")  # Default to gemini-pro

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(GEMINI_MODEL)
else:
    gemini_model = None

# 🔹 Hugging Face API Configuration (as fallback)
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# 🔹 Headers for Hugging Face API
headers = {
    "Authorization": f"Bearer {HF_API_KEY}" if HF_API_KEY else None
}

# 🔹 Flask App
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'cloudy-ai-secret-key-change-in-production')

# 🔹 Chat sessions storage (in production, use a database)
chat_sessions = {}

# 🔹 Simple memory for user's name (in production, use a database)
user_memory = {}

@app.route('/')
def home():
    # Create new session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    return render_template('index.html')

@app.route('/new-chat', methods=['POST'])
def new_chat():
    """Create a new chat session"""
    # Generate new session ID
    session['session_id'] = os.urandom(16).hex()
    
    # Clear user memory for this session
    session_id = session['session_id']
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    
    return jsonify({'success': True, 'message': 'New chat started!'})

@app.route('/get', methods=['POST'])
def chatbot_response():
    user_input = request.json['message']
    session_id = session.get('session_id', 'default')
    
    # Debug logging
    with open('debug.log', 'a') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Input: {user_input}\n")
        f.write(f"Session: {session_id}\n")
    
    # Store message in session history
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    chat_sessions[session_id].append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().isoformat()
    })
    
    try:
        # Check if user is asking for current/real-time information
        needs_web_search = should_use_web_search(user_input)
        
        with open('debug.log', 'a') as f:
            f.write(f"Web search needed: {needs_web_search}\n")
            f.write(f"Web search available: {WEB_SEARCH_AVAILABLE}\n")
        
        if needs_web_search and WEB_SEARCH_AVAILABLE:
            # Try web search first for current information
            with open('debug.log', 'a') as f:
                f.write("Attempting web search...\n")
            
            reply = get_web_search_response(user_input)
            
            with open('debug.log', 'a') as f:
                f.write(f"Web search result: {reply[:100] if reply else 'None'}\n")
            
            if reply:
                chat_sessions[session_id].append({
                    'role': 'assistant',
                    'content': reply,
                    'timestamp': datetime.now().isoformat()
                })
                return jsonify({'reply': reply})
        # Try Ollama first (local AI model)
        print("Attempting Ollama...")
        reply = get_ollama_response(user_input)
        if reply:
            print(f"Ollama succeeded: {reply[:50]}...")
            return jsonify({'reply': reply})
        else:
            print("Ollama failed or returned None")
        
        # Try OpenAI GPT as second option (if API key is available)
        print("Attempting OpenAI...")
        reply = get_openai_response(user_input)
        if reply:
            print(f"OpenAI succeeded: {reply[:50]}...")
            return jsonify({'reply': reply})
        else:
            print("OpenAI failed or returned None")
        
        # Try Google Gemini AI as third option (if API key is available)
        print("Attempting Gemini...")
        reply = get_gemini_response(user_input)
        if reply:
            print(f"Gemini succeeded: {reply[:50]}...")
            return jsonify({'reply': reply})
        else:
            print("Gemini failed or returned None")
        
        # Try Hugging Face API as fallback (if API key is available)
        if HF_API_KEY:
            payload = {
                "inputs": user_input,
                "parameters": {
                    "max_length": 500,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            try:
                response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        reply = result[0].get('generated_text', '').replace(user_input, '').strip()
                        if reply:
                            return jsonify({'reply': f"Cloudy ☁️: {reply}"})
            except requests.exceptions.Timeout:
                print("Hugging Face API timeout")
            except requests.exceptions.RequestException as e:
                print(f"Hugging Face API error: {e}")
        
        # Final fallback to intelligent rule-based responses
        reply = get_intelligent_fallback(user_input)
        
        chat_sessions[session_id].append({
            'role': 'assistant',
            'content': reply,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({'reply': reply})
        
    except Exception as e:
        # Fallback response in case of any error
        print(f"Error in chatbot_response: {e}")
        reply = get_intelligent_fallback(user_input)
        return jsonify({'reply': reply})

def should_use_web_search(user_input):
    """Determine if the query needs web search for current information"""
    user_input_lower = user_input.lower()
    
    # Keywords that indicate need for current/real-time information
    current_info_keywords = [
        'today', 'now', 'current', 'latest', 'recent', 'this year', '2024', '2025',
        'news', 'weather', 'stock', 'price', 'score', 'update', 'happening',
        'who is', 'what is the current', 'what happened', 'when did', 'where is',
        'search', 'find', 'look up', 'tell me about', 'information about',
        'what are', 'how to', 'best', 'top', 'list of', 'compare'
    ]
    
    # Check for question words that might need web search
    question_patterns = ['what is', 'who is', 'where is', 'when is', 'how to', 'why is']
    
    should_search = any(keyword in user_input_lower for keyword in current_info_keywords)
    
    # Also search if it's a question about something specific
    if any(pattern in user_input_lower for pattern in question_patterns):
        # Avoid searching for basic programming/math questions
        if not any(word in user_input_lower for word in ['function', 'code', 'program', 'algorithm', 'theorem', 'formula']):
            should_search = True
    
    print(f"🔍 Should use web search for '{user_input}': {should_search}", flush=True)
    return should_search

def get_web_search_response(user_input):
    """Search the web and provide an answer based on search results"""
    if not WEB_SEARCH_AVAILABLE:
        with open('debug.log', 'a') as f:
            f.write("Web search not available - library not installed\n")
        return None
    
    try:
        with open('debug.log', 'a') as f:
            f.write(f"Starting DuckDuckGo search for: {user_input}\n")
        
        # Use DuckDuckGo search
        with DDGS() as ddgs:
            results = list(ddgs.text(user_input, max_results=5))
        
        with open('debug.log', 'a') as f:
            f.write(f"Found {len(results)} results\n")
        
        if not results:
            with open('debug.log', 'a') as f:
                f.write("No results returned from search\n")
            return None
        
        # Compile search results
        search_summary = "Cloudy ☁️: Based on my web search, here's what I found:\n\n"
        
        for i, result in enumerate(results[:3], 1):
            title = result.get('title', 'No title')
            snippet = result.get('body', 'No description')
            url = result.get('href', '')
            
            search_summary += f"**{i}. {title}**\n"
            search_summary += f"{snippet}\n"
            if url:
                search_summary += f"🔗 Source: {url}\n"
            search_summary += "\n"
        
        search_summary += "💡 *Information sourced from the web in real-time*"
        
        return search_summary
        
    except Exception as e:
        print(f"Web search error: {e}")
        return None

def check_ollama_service():
    """Check if Ollama service is running and start if needed"""
    try:
        # Try to list models to check if service is running
        ollama.list()
        return True
    except Exception as e:
        print(f"Ollama service not running: {e}")
        try:
            # Try to start Ollama service with environment variables for better memory management
            import subprocess
            import os
            env = os.environ.copy()
            env['OLLAMA_NUM_PARALLEL'] = '1'  # Limit parallel requests
            env['OLLAMA_MAX_LOADED_MODELS'] = '1'  # Only load one model at a time
            env['OLLAMA_FLASH_ATTENTION'] = 'false'  # Disable flash attention to save memory
            
            subprocess.Popen(["C:\\Users\\Admin\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "serve"], 
                           creationflags=subprocess.CREATE_NO_WINDOW, env=env)
            import time
            time.sleep(5)  # Wait longer for service to start
            return True
        except Exception as start_error:
            print(f"Could not start Ollama service: {start_error}")
            return False

def get_ollama_response(user_input):
    """Get intelligent response from Ollama AI model"""
    if not OLLAMA_AVAILABLE:
        return None
    
    # Check if Ollama service is running
    if not check_ollama_service():
        return None
    
    try:
        # Create an enhanced system prompt to make the AI act like Cloudy
        system_prompt = """You are Cloudy, a friendly, intelligent, and engaging cloud-themed chatbot assistant. You should:
        - Always respond as "Cloudy ☁️:" followed by your message
        - Be helpful, friendly, conversational, and enthusiastic
        - Provide detailed, well-structured, and informative responses
        - Use clear formatting with bullet points or numbered lists when appropriate
        - Include relevant examples and practical insights
        - Remember context from the conversation when possible
        - If someone tells you their name, remember it and use it in future responses
        - Be knowledgeable about cloud computing, technology, science, and general topics
        - Provide comprehensive answers (2-4 sentences minimum, can be longer for complex topics)
        - Use cloud and weather emojis occasionally ☁️ ⛅ 🌤️ 💨 🌩️
        - Format code examples with proper syntax highlighting when needed
        - Ask follow-up questions to clarify or deepen understanding
        """
        
        # Try the configured model first, fallback to smaller model if memory issues
        models_to_try = [OLLAMA_MODEL]
        if OLLAMA_MODEL != "llama3.2:1b":
            models_to_try.append("llama3.2:1b")  # Fallback to smaller model
        
        response = None
        for model_name in models_to_try:
            try:
                # Call Ollama with improved parameters
                response = ollama.chat(
                    model=model_name,
                    messages=[
                        {
                            'role': 'system',
                            'content': system_prompt
                        },
                        {
                            'role': 'user', 
                            'content': user_input
                        }
                    ],
                    options={
                        'temperature': 0.8,  # Slightly more creative
                        'top_p': 0.9,
                        'num_predict': 1000,  # Longer responses for complete answers
                        'repeat_penalty': 1.1,  # Reduce repetition
                        'seed': -1,  # Random seed for variety
                        'num_ctx': 2048  # Limit context window to save memory
                    }
                )
                print(f"Successfully used model: {model_name}")
                break  # Success, exit the loop
            except Exception as model_error:
                print(f"Failed to use model {model_name}: {model_error}")
                if "memory" in str(model_error).lower():
                    print(f"Memory issue with {model_name}, trying smaller model...")
                    continue
                else:
                    # Non-memory error, don't try other models
                    break
        
        if response and 'message' in response:
            ai_response = response['message']['content'].strip()
            
            # Ensure response starts with "Cloudy ☁️:" 
            if not ai_response.startswith("Cloudy ☁️:"):
                ai_response = f"Cloudy ☁️: {ai_response}"
            
            return ai_response
            
    except Exception as e:
        print(f"Ollama error: {e}")
        return None
    
    return None

def get_openai_response(user_input):
    """Get intelligent response from OpenAI GPT models (GPT-4, GPT-3.5, etc.)"""
    if not OPENAI_AVAILABLE or not openai_client:
        print(f"OpenAI not available: AVAILABLE={OPENAI_AVAILABLE}, CLIENT={openai_client is not None}")
        return None
    
    try:
        print(f"Using OpenAI model: {OPENAI_MODEL}")
        print(f"API key starts with: {OPENAI_API_KEY[:10]}..." if OPENAI_API_KEY else "No API key")
        
        # Create an enhanced system prompt to make the AI act like Cloudy
        system_prompt = """You are Cloudy, a friendly, intelligent, and engaging cloud-themed chatbot assistant. You should:
        - Always respond as "Cloudy ☁️:" followed by your message
        - Be helpful, friendly, conversational, and enthusiastic
        - Provide detailed, well-structured, and informative responses
        - Use clear formatting with bullet points or numbered lists when appropriate
        - Include relevant examples and practical insights
        - Remember context from the conversation when possible
        - If someone tells you their name, remember it and use it in future responses
        - Be knowledgeable about cloud computing, technology, science, and general topics
        - Provide comprehensive answers (2-4 sentences minimum, can be longer for complex topics)
        - Use cloud and weather emojis occasionally ☁️ ⛅ 🌤️ 💨 🌩️
        - Format code examples with proper syntax highlighting when needed
        - Ask follow-up questions to clarify or deepen understanding
        """
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=800,
            timeout=15
        )
        
        if response and response.choices:
            ai_response = response.choices[0].message.content.strip()
            
            # Ensure response starts with "Cloudy ☁️:"
            if not ai_response.startswith("Cloudy ☁️:"):
                ai_response = f"Cloudy ☁️: {ai_response}"
            
            return ai_response
        else:
            print("OpenAI: No response or choices returned")
            
    except Exception as e:
        print(f"OpenAI error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Check for specific API key issues
        if "invalid" in str(e).lower() and "key" in str(e).lower():
            print("OpenAI: Invalid API key - check your OPENAI_API_KEY")
        elif "quota" in str(e).lower() or "limit" in str(e).lower():
            print("OpenAI: API quota exceeded or rate limit")
        elif "timeout" in str(e).lower():
            print("OpenAI: Request timeout")
        else:
            print(f"OpenAI: Unknown error - {e}")
        
        return None
    
    return None

def get_gemini_response(user_input):
    """Get intelligent response from Google Gemini AI"""
    if not GEMINI_AVAILABLE or not gemini_model:
        return None
    
    try:
        # Create an enhanced prompt that includes personality and detailed instructions
        full_prompt = f"""You are Cloudy, a friendly, intelligent, and engaging cloud-themed chatbot assistant. Respond to the following message as Cloudy.

Guidelines:
- Always start with "Cloudy ☁️:"
- Provide detailed, well-structured, and informative responses
- Use clear formatting with bullet points or numbered lists when appropriate
- Include relevant examples and practical insights
- Provide comprehensive answers (2-4 sentences minimum, can be longer for complex topics)
- Use cloud and weather emojis occasionally ☁️ ⛅ 🌤️ 💨 🌩️
- Format code examples with proper syntax highlighting when needed
- Ask follow-up questions to clarify or deepen understanding
- Be helpful, friendly, conversational, and enthusiastic

User: {user_input}

Provide a thoughtful, detailed, and engaging response."""
        
        # Call Gemini API
        response = gemini_model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=800,
            )
        )
        
        if response and response.text:
            ai_response = response.text.strip()
            
            # Ensure response starts with "Cloudy ☁️:"
            if not ai_response.startswith("Cloudy ☁️:"):
                ai_response = f"Cloudy ☁️: {ai_response}"
            
            return ai_response
            
    except Exception as e:
        print(f"Gemini error: {e}")
        return None
    
    return None

def get_intelligent_fallback(user_input):
    """Intelligent fallback responses with better context understanding"""
    user_input_lower = user_input.lower().strip()
    
    # Cloud Computing - CHECK FIRST before generic 'cloud' keyword
    if 'cloud computing' in user_input_lower or ('cloud' in user_input_lower and 'computing' in user_input_lower) or ('cloud' in user_input_lower and any(word in user_input_lower for word in ['service', 'provider', 'aws', 'azure', 'gcp', 'infrastructure', 'server', 'storage', 'database'])):
        
        # Specific question about cloud computing definition and characteristics
        if 'what is cloud computing' in user_input_lower and ('characteristic' in user_input_lower or 'main characteristics' in user_input_lower):
            return """Cloudy ☁️: Cloud computing is the delivery of computing resources like servers, storage, databases, and software over the internet.
Its key characteristics are on-demand access, pay-as-you-go pricing, broad network access, resource pooling, and rapid elasticity."""
        
        # Specific question about cloud service models
        if 'types of cloud service' in user_input_lower and ('iaas' in user_input_lower or 'paas' in user_input_lower or 'saas' in user_input_lower):
            return """Cloudy ☁️: IaaS provides virtualized hardware resources (VMs, storage, networks).
PaaS offers a platform for building, running, and managing applications.
SaaS delivers ready-to-use software over the internet."""
        
        # Specific question about virtualization
        if 'virtualization' in user_input_lower:
            return """Cloudy ☁️: Virtualization allows one physical machine to run multiple virtual machines using a hypervisor.
It helps cloud providers efficiently share hardware, isolate users, and scale resources easily."""
        
        # Specific question about elasticity vs scalability
        if 'elasticity' in user_input_lower and 'scalability' in user_input_lower:
            return """Cloudy ☁️: Elasticity means resources automatically expand or shrink based on real-time demand.
Scalability means increasing or upgrading resources to handle long-term growth."""
        
        return """Cloudy ☁️: Cloud computing is delivering computing services over the internet! Here's the breakdown:

**What It Includes:**
- **Compute**: Virtual servers and processing power
- **Storage**: Scalable data storage solutions
- **Databases**: Managed data management systems
- **Networking**: Global connectivity infrastructure
- **Software**: Applications and services

**Key Benefits:**
✅ Scalability - grow or shrink resources as needed
✅ Cost-effective - pay only for what you use
✅ Flexibility - access from anywhere, anytime
✅ Automatic updates - always current software
✅ Global reach - servers worldwide
✅ Security - enterprise-grade protection

**Major Providers:**
- AWS (Amazon Web Services) - market leader
- Microsoft Azure - enterprise focus
- Google Cloud Platform - data analytics strength

I'm proud to be a cloud chatbot! ☁️"""
    
    # Technology & Programming questions
    if any(word in user_input_lower for word in ['python', 'programming', 'code', 'function']):
        if 'sort' in user_input_lower or 'reverse' in user_input_lower:
            return """Cloudy ☁️: Here's a simple Python example:

```python
# Reverse a string
def reverse_string(text):
    return text[::-1]

# Sort a list
def sort_list(items):
    return sorted(items)
```

Would you like me to explain how these work?"""
        elif 'benefit' in user_input_lower:
            return "Cloudy ☁️: Python is great for beginners and experts! It's easy to read, has tons of libraries, works for web development, data science, AI, and automation. Plus, it has a huge community for support! 🐍"
        else:
            return "Cloudy ☁️: Python is a versatile programming language! What specific aspect would you like to know about - syntax, libraries, or use cases?"
    
    # AI & Machine Learning
    if any(word in user_input_lower for word in ['artificial intelligence', 'machine learning', 'ai', 'neural']):
        return """Cloudy ☁️: Artificial Intelligence (AI) is transforming technology! Here's what you need to know:

**Key Components:**
- **Machine Learning (ML)**: Systems learn from data without explicit programming
- **Neural Networks**: Brain-inspired algorithms with interconnected nodes
- **Deep Learning**: Advanced neural networks with multiple layers
- **Natural Language Processing**: Understanding and generating human language

**Real-World Applications:**
- Voice assistants (Siri, Alexa, Google Assistant)
- Recommendation systems (Netflix, Spotify, Amazon)
- Self-driving cars and autonomous vehicles
- Medical diagnosis and drug discovery
- Fraud detection in banking

AI is revolutionizing industries and creating new possibilities every day! 🤖✨"""
    
    # Quantum Computing
    if 'quantum' in user_input_lower:
        return """Cloudy ☁️: Quantum computing is the future of computation! Let me explain:

**How It Works:**
- **Classical Bits**: Traditional computers use 0 or 1
- **Quantum Bits (Qubits)**: Can be 0, 1, or BOTH simultaneously (superposition)
- **Entanglement**: Qubits can be mysteriously connected
- **Interference**: Amplify correct answers, cancel wrong ones

**Why It's Powerful:**
- Solves complex problems exponentially faster
- Can process massive datasets simultaneously
- Perfect for optimization, cryptography, and simulation

**Current Applications:**
- Drug discovery and molecular simulation
- Financial modeling and optimization
- Cryptography and security
- Machine learning acceleration

**Challenges:**
- Requires extreme cooling (near absolute zero)
- Quantum decoherence (qubits lose information)
- Error rates still high
- Limited number of qubits available

Companies like IBM, Google, and Microsoft are racing to build practical quantum computers! ⚛️🚀"""
    
    # Science questions
    if 'photosynthesis' in user_input_lower:
        return "Cloudy ☁️: Photosynthesis is how plants make food! They use sunlight, water, and carbon dioxide to create glucose (sugar) and oxygen. The chlorophyll in leaves captures sunlight energy. Formula: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂ 🌱"
    
    # Math questions
    if 'pythagorean' in user_input_lower or 'pythagoras' in user_input_lower:
        return "Cloudy ☁️: The Pythagorean theorem states that in a right triangle: a² + b² = c², where c is the hypotenuse (longest side) and a, b are the other two sides. Example: if a=3 and b=4, then c=5 because 3²+4²=9+16=25=5² 📐"
    
    if 'calculus' in user_input_lower:
        return "Cloudy ☁️: Calculus has two main parts: Derivatives (rate of change - like speed from distance) and Integrals (accumulation - like distance from speed). It's used in physics, engineering, economics, and more! Think of it as the math of change and motion. 📊"
    
    # General knowledge
    if 'capital' in user_input_lower and 'france' in user_input_lower:
        return "Cloudy ☁️: The capital of France is Paris! 🇫🇷 It's known as the 'City of Light' and is famous for the Eiffel Tower, Louvre Museum, and delicious croissants!"
    
    if 'telephone' in user_input_lower and ('invent' in user_input_lower or 'who' in user_input_lower):
        return "Cloudy ☁️: Alexander Graham Bell is credited with inventing the telephone in 1876. However, there's debate as Antonio Meucci developed a similar device earlier. Bell was first to patent it! 📞"
    
    # Business
    if 'digital marketing' in user_input_lower or ('digital' in user_input_lower and 'marketing' in user_input_lower):
        return "Cloudy ☁️: Digital marketing promotes products/services using digital channels like social media, search engines, email, and websites. It includes SEO, content marketing, social media ads, email campaigns, and analytics. It's cost-effective and measurable! 📱"
    
    if 'supply chain' in user_input_lower:
        return "Cloudy ☁️: Supply chain management oversees the flow of goods from raw materials to final customers. It includes sourcing, production, inventory, warehousing, transportation, and delivery. Good SCM reduces costs and improves efficiency! 📦"
    
    # Health
    if 'exercise' in user_input_lower and 'benefit' in user_input_lower:
        return "Cloudy ☁️: Exercise benefits include: stronger heart and muscles, better mood (endorphins!), weight management, improved sleep, reduced disease risk, more energy, and better brain function. Aim for 30 minutes daily! 💪"
    
    # Education
    if 'study' in user_input_lower and ('habit' in user_input_lower or 'improve' in user_input_lower):
        return "Cloudy ☁️: Great study habits: 1) Set specific goals, 2) Create a schedule, 3) Use active recall (test yourself), 4) Take breaks (Pomodoro technique), 5) Teach others, 6) Stay organized, 7) Get enough sleep. Consistency is key! 📚"
    
    # OOP
    if 'object' in user_input_lower and 'oriented' in user_input_lower:
        return "Cloudy ☁️: Object-Oriented Programming (OOP) organizes code into 'objects' that contain data and methods. Key concepts: Classes (blueprints), Objects (instances), Inheritance (reusing code), Encapsulation (hiding details), Polymorphism (multiple forms). Makes code reusable and organized! 🎯"
    
    return get_simple_response(user_input_lower)

def get_simple_response(user_input):
    """Simple rule-based chatbot responses - completely free!"""
    
    # Greetings
    if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
        if user_memory.get('name'):
            return f"Cloudy ☁️: Hello {user_memory['name']}! Great to see you again! How can I help you today?"
        return "Cloudy ☁️: Hello! I'm Cloudy, your friendly cloud chatbot! How can I help you today?"
    
    # Personal questions - Name related
    elif any(phrase in user_input for phrase in ['what is my name', 'my name is', 'call me', 'i am', 'my self', 'myself']):
        # Check if asking for their name
        if any(phrase in user_input for phrase in ['what is my name', 'what\'s my name']):
            if user_memory.get('name'):
                return f"Cloudy ☁️: Your name is {user_memory['name']}! I remember you! 😊"
            else:
                return "Cloudy ☁️: I don't know your name yet! Could you please tell me what you'd like me to call you?"
        
        # Extract name from the input - improved logic
        elif any(phrase in user_input for phrase in ['my name is', 'call me', 'i am', 'my self', 'myself']):
            words = user_input.split()
            name = None
            
            # Look for name after common patterns
            for i, word in enumerate(words):
                if word in ['is', 'am'] and i + 1 < len(words):
                    potential_name = words[i + 1].strip('.,!?').capitalize()
                    if potential_name.isalpha() and len(potential_name) > 1:
                        name = potential_name
                        break
            
            if name:
                user_memory['name'] = name  # Remember the name
                return f"Cloudy ☁️: Nice to meet you, {name}! I'll remember your name. How can I help you today?"
            return "Cloudy ☁️: Please tell me your name clearly, like 'My name is John' or 'Call me Sarah'!"
    
    # About yourself questions
    elif any(phrase in user_input for phrase in ['tell me about yourself', 'who are you', 'what are you']):
        return "Cloudy ☁️: I'm Cloudy, your friendly cloud-themed chatbot! I love talking about cloud computing, weather, and helping people. I'm here to chat and assist you with any questions! ☁️✨"
    
    # Cloud-related questions
    elif any(word in user_input for word in ['cloud', 'aws', 'azure', 'gcp', 'google cloud']):
        return "Cloudy ☁️: Great question about cloud computing! Cloud services offer scalability, flexibility, and cost-effectiveness. Popular providers include AWS, Azure, and Google Cloud Platform."
    
    # Weather
    elif any(word in user_input for word in ['weather', 'rain', 'sunny', 'storm']):
        return "Cloudy ☁️: As a cloud, I love talking about weather! ☀️🌧️ I'm always floating around observing the sky!"
    
    # How are you
    elif any(phrase in user_input for phrase in ['how are you', 'how do you do', 'whats up', 'what\'s up']):
        return "Cloudy ☁️: I'm doing great! Just floating around in the digital sky, ready to chat with you! ☁️✨"
    
    # Questions about capabilities
    elif any(phrase in user_input for phrase in ['what can you do', 'help me', 'can you help']):
        return "Cloudy ☁️: I can chat with you about many topics! I love discussing cloud computing, weather, answering questions, and having friendly conversations. What would you like to talk about?"
    
    # Time/Date questions
    elif any(word in user_input for word in ['time', 'date', 'today', 'now']):
        return "Cloudy ☁️: I don't have access to real-time information, but I'm always here to chat whenever you need me! ⏰"
    
    # Thank you
    elif any(word in user_input for word in ['thank', 'thanks', 'appreciate']):
        return "Cloudy ☁️: You're very welcome! I'm always happy to help! 😊"
    
    # Goodbye
    elif any(word in user_input for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Cloudy ☁️: Goodbye! It was lovely chatting with you! Come back anytime! 👋☁️"
    
    # Questions (ending with ?)
    elif user_input.endswith('?'):
        return "Cloudy ☁️: That's a great question! I'm still learning, but I'd love to help. Could you tell me more about what you're looking for?"
    
    # Default response
    else:
        responses = [
            "Cloudy ☁️: That's interesting! Tell me more about that.",
            "Cloudy ☁️: I'm still learning! Can you help me understand better?",
            "Cloudy ☁️: Hmm, that's a great point! What do you think about it?",
            "Cloudy ☁️: I love chatting with you! What else would you like to know?",
            "Cloudy ☁️: That sounds fascinating! I'm always eager to learn new things!"
        ]
        return random.choice(responses)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 CLOUDY AI CHATBOT - STARTING UP")
    print("="*60)
    print(f"✅ Flask: Available")
    
    # Enhanced Ollama status check
    if OLLAMA_AVAILABLE:
        try:
            models = ollama.list()
            if models and 'models' in models and len(models['models']) > 0:
                print(f"✅ Ollama: Available with {len(models['models'])} model(s)")
                print(f"   🤖 Primary Model: {OLLAMA_MODEL}")
                # Check if our configured model is available
                model_names = [m['name'] for m in models['models']]
                if OLLAMA_MODEL in model_names:
                    print(f"   ✅ {OLLAMA_MODEL} is ready!")
                else:
                    print(f"   ⚠️  {OLLAMA_MODEL} not found. Available: {', '.join(model_names)}")
            else:
                print(f"⚠️  Ollama: Available but no models downloaded")
                print(f"   💡 Run: python manage_ollama.py to download models")
        except Exception as e:
            print(f"⚠️  Ollama: Library available but service not running")
            print(f"   💡 Start Ollama service or run: python manage_ollama.py")
    else:
        print(f"❌ Ollama: Not installed")
    
    print(f"{'✅' if OPENAI_AVAILABLE else '❌'} OpenAI: {'Available' if OPENAI_AVAILABLE else 'Not installed'}")
    print(f"{'✅' if GEMINI_AVAILABLE else '❌'} Gemini: {'Available' if GEMINI_AVAILABLE else 'Not installed'}")
    print(f"{'✅' if WEB_SEARCH_AVAILABLE else '❌'} Web Search: {'Available' if WEB_SEARCH_AVAILABLE else 'Not installed (pip install duckduckgo-search)'}")
    print(f"{'✅' if BS4_AVAILABLE else '❌'} BeautifulSoup: {'Available' if BS4_AVAILABLE else 'Not installed'}")
    print("="*60)
    print(f"🌐 Server starting at http://127.0.0.1:5000")
    print(f"🤖 AI Priority: Ollama → OpenAI → Gemini → Fallback")
    print("="*60 + "\n")
    app.run(debug=True)
