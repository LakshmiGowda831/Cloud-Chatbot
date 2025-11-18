#!/usr/bin/env python3
"""
Setup script for Ollama integration with the Cloud Chatbot
This script helps you install Ollama and download the required model
"""

import subprocess
import sys
import os
import requests
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n[*] {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completed successfully!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"[ERROR] {description} failed!")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] {description} failed with exception: {e}")
        return False

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("Cloud Chatbot - Ollama Setup Script")
    print("=" * 50)
    
    # Check if Ollama is installed
    if check_ollama_installed():
        print("[SUCCESS] Ollama is already installed!")
    else:
        print("[ERROR] Ollama is not installed.")
        print("\n[INFO] Please install Ollama manually:")
        print("1. Go to https://ollama.ai/")
        print("2. Download Ollama for Windows")
        print("3. Install and run the application")
        print("4. Come back and run this script again")
        return
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("\n[*] Starting Ollama service...")
        # Try to start Ollama (it should auto-start on Windows)
        subprocess.Popen("ollama serve", shell=True)
        time.sleep(3)
        
        if not check_ollama_running():
            print("[ERROR] Ollama service is not running.")
            print("Please start Ollama manually and try again.")
            return
    
    print("[SUCCESS] Ollama service is running!")
    
    # Download the model
    model_name = "llama3.2:1b"
    print(f"\n[*] Downloading model: {model_name}")
    print("This may take a few minutes...")
    
    if run_command(f"ollama pull {model_name}", f"Downloading {model_name}"):
        print(f"\n[SUCCESS] Setup completed successfully!")
        print(f"[SUCCESS] Model '{model_name}' is ready to use")
        print("\n[INFO] You can now run your chatbot with:")
        print("   python app/chatbot.py")
        print("\n[INFO] The chatbot will now use AI-powered responses!")
    else:
        print(f"\n[ERROR] Failed to download model '{model_name}'")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
