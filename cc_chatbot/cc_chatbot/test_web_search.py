"""
Test Web Search Functionality
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# Test queries that should trigger web search
test_queries = [
    "What's the latest news about AI?",
    "Tell me about current events",
    "Who is Elon Musk?",
    "What is happening today?",
    "Latest technology news",
    "Current weather",
    "Search for quantum computing",
    "Find information about Python programming"
]

print("="*70)
print("🔍 TESTING WEB SEARCH FUNCTIONALITY")
print("="*70)

for i, query in enumerate(test_queries, 1):
    print(f"\n[Test {i}/{len(test_queries)}]")
    print(f"Query: {query}")
    print("-"*70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/get",
            json={"message": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get('reply', 'No reply')
            
            # Check if it's a web search response
            if "Based on my web search" in reply or "🔗 Source:" in reply:
                print("✅ WEB SEARCH USED")
                print(f"Response preview: {reply[:200]}...")
            else:
                print("❌ WEB SEARCH NOT USED")
                print(f"Response: {reply[:150]}...")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

print("="*70)
print("Test completed!")
print("="*70)
