#!/usr/bin/env python3
"""
Test script for the LangGraph MCP Agent
"""

import os
from dotenv import load_dotenv
from simple_langgraph_app import run_agent

load_dotenv()

def test_langgraph_agent():
    """Test the LangGraph agent with various inputs"""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        return False
    
    print("🧪 Testing LangGraph MCP Agent")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "input": "Roll 2d6 for me",
            "description": "Testing dice rolling functionality"
        },
        {
            "input": "What's the current stock price of AAPL?",
            "description": "Testing stock data functionality"
        },
        {
            "input": "Search for information about Python programming",
            "description": "Testing web search functionality"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"Input: {test_case['input']}")
        
        try:
            response = run_agent(test_case['input'])
            print(f"✅ Response: {response[:200]}...")
            results.append(True)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print(f"Total tests: {len(test_cases)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(test_cases) - sum(results)}")
    
    if all(results):
        print("🎉 All tests passed! The LangGraph agent is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    test_langgraph_agent()
