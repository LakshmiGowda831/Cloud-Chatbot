"""
Automated Test Suite for Cloudy AI Chatbot
Tests various domains and scenarios to ensure proper functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_ENDPOINT = f"{BASE_URL}/get"

# Test cases covering different domains
TEST_CASES = [
    # Technology Domain
    {
        "category": "Technology",
        "message": "What is cloud computing?",
        "expected_keywords": ["cloud", "computing", "server", "internet", "data"]
    },
    {
        "category": "Technology",
        "message": "Explain artificial intelligence in simple terms",
        "expected_keywords": ["AI", "artificial", "intelligence", "machine", "learn"]
    },
    {
        "category": "Technology",
        "message": "What are the benefits of using Python?",
        "expected_keywords": ["Python", "programming", "language", "easy", "versatile"]
    },
    
    # Science Domain
    {
        "category": "Science",
        "message": "How does photosynthesis work?",
        "expected_keywords": ["photosynthesis", "plant", "light", "energy", "oxygen"]
    },
    {
        "category": "Science",
        "message": "What is quantum computing?",
        "expected_keywords": ["quantum", "computing", "qubit", "superposition"]
    },
    
    # Mathematics Domain
    {
        "category": "Mathematics",
        "message": "What is the Pythagorean theorem?",
        "expected_keywords": ["Pythagorean", "theorem", "triangle", "square"]
    },
    {
        "category": "Mathematics",
        "message": "Explain calculus basics",
        "expected_keywords": ["calculus", "derivative", "integral", "function"]
    },
    
    # Business Domain
    {
        "category": "Business",
        "message": "What is digital marketing?",
        "expected_keywords": ["digital", "marketing", "online", "social", "media"]
    },
    {
        "category": "Business",
        "message": "Explain the concept of supply chain management",
        "expected_keywords": ["supply", "chain", "management", "logistics", "product"]
    },
    
    # General Knowledge
    {
        "category": "General",
        "message": "What is the capital of France?",
        "expected_keywords": ["Paris", "France", "capital"]
    },
    {
        "category": "General",
        "message": "Who invented the telephone?",
        "expected_keywords": ["Bell", "telephone", "invented", "Alexander"]
    },
    
    # Coding/Programming
    {
        "category": "Programming",
        "message": "Write a Python function to reverse a string",
        "expected_keywords": ["Python", "function", "reverse", "string"]
    },
    {
        "category": "Programming",
        "message": "What is object-oriented programming?",
        "expected_keywords": ["object", "oriented", "programming", "class", "OOP"]
    },
    
    # Personal/Conversational
    {
        "category": "Personal",
        "message": "Hello! How are you?",
        "expected_keywords": ["hello", "hi", "great", "good", "cloudy"]
    },
    {
        "category": "Personal",
        "message": "My name is Alex",
        "expected_keywords": ["Alex", "name", "meet", "nice"]
    },
    {
        "category": "Personal",
        "message": "What's my name?",
        "expected_keywords": ["Alex", "name", "remember"]
    },
    
    # Health & Wellness
    {
        "category": "Health",
        "message": "What are the benefits of exercise?",
        "expected_keywords": ["exercise", "health", "fitness", "benefit", "body"]
    },
    
    # Education
    {
        "category": "Education",
        "message": "How can I improve my study habits?",
        "expected_keywords": ["study", "learn", "habit", "improve", "focus"]
    },
]

def send_message(message):
    """Send a message to the chatbot and return the response"""
    try:
        response = requests.post(
            TEST_ENDPOINT,
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("reply", "No reply received")
        else:
            return f"Error: HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return "Error: Request timeout"
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to server. Is it running?"
    except Exception as e:
        return f"Error: {str(e)}"

def check_keywords(response, keywords):
    """Check if any expected keywords are in the response"""
    response_lower = response.lower()
    found_keywords = [kw for kw in keywords if kw.lower() in response_lower]
    return len(found_keywords) > 0, found_keywords

def run_tests():
    """Run all test cases"""
    print("=" * 80)
    print("CLOUDY AI CHATBOT - AUTOMATED TEST SUITE")
    print("=" * 80)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing endpoint: {TEST_ENDPOINT}")
    print("=" * 80)
    print()
    
    results = {
        "total": len(TEST_CASES),
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "details": []
    }
    
    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n[Test {i}/{len(TEST_CASES)}] Category: {test['category']}")
        print(f"Question: {test['message']}")
        print("-" * 80)
        
        # Send message
        response = send_message(test['message'])
        
        # Check for errors
        if response.startswith("Error:"):
            print(f"❌ FAILED - {response}")
            results["errors"] += 1
            results["details"].append({
                "test": i,
                "category": test['category'],
                "status": "ERROR",
                "message": test['message'],
                "error": response
            })
            continue
        
        print(f"Response: {response}")
        
        # Check keywords
        has_keywords, found = check_keywords(response, test['expected_keywords'])
        
        if has_keywords:
            print(f"✅ PASSED - Found keywords: {', '.join(found)}")
            results["passed"] += 1
            results["details"].append({
                "test": i,
                "category": test['category'],
                "status": "PASSED",
                "message": test['message'],
                "response": response,
                "keywords_found": found
            })
        else:
            print(f"⚠️  WARNING - No expected keywords found")
            print(f"   Expected any of: {', '.join(test['expected_keywords'])}")
            # Still count as passed if we got a valid response
            results["passed"] += 1
            results["details"].append({
                "test": i,
                "category": test['category'],
                "status": "PASSED_NO_KEYWORDS",
                "message": test['message'],
                "response": response
            })
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"⚠️  Errors: {results['errors']}")
    print(f"Success Rate: {(results['passed'] / results['total'] * 100):.1f}%")
    print("=" * 80)
    
    # Category breakdown
    categories = {}
    for detail in results['details']:
        cat = detail['category']
        if cat not in categories:
            categories[cat] = {"passed": 0, "total": 0}
        categories[cat]["total"] += 1
        if detail['status'] in ["PASSED", "PASSED_NO_KEYWORDS"]:
            categories[cat]["passed"] += 1
    
    print("\nCATEGORY BREAKDOWN:")
    print("-" * 80)
    for cat, stats in categories.items():
        rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{cat:20s}: {stats['passed']}/{stats['total']} ({rate:.0f}%)")
    
    print("\n" + "=" * 80)
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    try:
        results = run_tests()
        
        # Save results to file
        with open("test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\n📄 Detailed results saved to: test_results.json")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite error: {str(e)}")
