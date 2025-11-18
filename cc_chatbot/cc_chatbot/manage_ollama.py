#!/usr/bin/env python3
"""
Ollama Management Script for Cloudy AI Chatbot
This script helps you manage Ollama models and check system status.
"""

import subprocess
import sys
import os

OLLAMA_PATH = r"C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.exe"

def run_ollama_command(command):
    """Run an Ollama command and return the result"""
    try:
        cmd = [OLLAMA_PATH] + command.split()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1

def list_models():
    """List all available Ollama models"""
    print("📋 Available Ollama Models:")
    print("=" * 40)
    stdout, stderr, code = run_ollama_command("list")
    if code == 0:
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")
    print()

def check_service():
    """Check if Ollama service is running"""
    print("🔍 Checking Ollama Service Status:")
    print("=" * 40)
    stdout, stderr, code = run_ollama_command("ps")
    if code == 0:
        print("✅ Ollama service is running")
        if stdout.strip():
            print("Running models:")
            print(stdout)
        else:
            print("No models currently loaded")
    else:
        print("❌ Ollama service is not running")
        print(f"Error: {stderr}")
    print()

def download_model(model_name):
    """Download a specific model"""
    print(f"⬇️  Downloading model: {model_name}")
    print("=" * 40)
    print("This may take several minutes depending on model size...")
    
    try:
        # Run the command without capturing output so we can see progress
        cmd = [OLLAMA_PATH, "pull", model_name]
        result = subprocess.run(cmd, timeout=1800)  # 30 minute timeout
        if result.returncode == 0:
            print(f"✅ Successfully downloaded {model_name}")
        else:
            print(f"❌ Failed to download {model_name}")
    except subprocess.TimeoutExpired:
        print("❌ Download timed out")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

def test_model(model_name):
    """Test a model with a simple query"""
    print(f"🧪 Testing model: {model_name}")
    print("=" * 40)
    
    # First check if model exists
    stdout, stderr, code = run_ollama_command("list")
    if model_name not in stdout:
        print(f"❌ Model {model_name} not found. Please download it first.")
        return
    
    # Test the model
    test_prompt = "Hello, please introduce yourself briefly."
    cmd = f'run {model_name} "{test_prompt}"'
    stdout, stderr, code = run_ollama_command(cmd)
    
    if code == 0:
        print("✅ Model test successful!")
        print("Response:")
        print(stdout)
    else:
        print(f"❌ Model test failed: {stderr}")
    print()

def main():
    """Main function"""
    print("🤖 Cloudy AI - Ollama Management Tool")
    print("=" * 50)
    
    if not os.path.exists(OLLAMA_PATH):
        print("❌ Ollama not found at expected location!")
        print(f"Expected: {OLLAMA_PATH}")
        print("Please install Ollama or update the path in this script.")
        return
    
    while True:
        print("\nChoose an option:")
        print("1. List available models")
        print("2. Check Ollama service status")
        print("3. Download recommended model (llama3.2:3b)")
        print("4. Download custom model")
        print("5. Test a model")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            list_models()
        elif choice == "2":
            check_service()
        elif choice == "3":
            download_model("llama3.2:3b")
        elif choice == "4":
            model = input("Enter model name (e.g., llama3.2:1b, codellama:7b): ").strip()
            if model:
                download_model(model)
        elif choice == "5":
            model = input("Enter model name to test: ").strip()
            if model:
                test_model(model)
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
