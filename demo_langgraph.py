#!/usr/bin/env python3
"""
Demo script for the LangGraph MCP Agent
This script demonstrates various capabilities of the agent
"""

import os
from dotenv import load_dotenv
from simple_langgraph_app import run_agent
import time

load_dotenv()

def demo_langgraph_agent():
    """Demonstrate the LangGraph agent capabilities"""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        return
    
    print("🎭 LangGraph MCP Agent Demo")
    print("=" * 60)
    print("This demo will showcase the agent's capabilities with various tools")
    print("=" * 60)
    
    # Demo scenarios
    demos = [
        {
            "title": "🎲 Dice Rolling",
            "input": "Roll 3d6 for my character's strength check",
            "description": "Demonstrates the dice rolling functionality"
        },
        {
            "title": "📈 Stock Data",
            "input": "What's the current stock price and market data for TSLA?",
            "description": "Shows real-time stock information retrieval"
        },
        {
            "title": "🔍 Web Search",
            "input": "Search for the latest news about artificial intelligence and machine learning",
            "description": "Demonstrates web search capabilities"
        },
        {
            "title": "🔄 Multi-Tool Usage",
            "input": "Search for information about Apple Inc and then get their current stock price",
            "description": "Shows how the agent can use multiple tools in sequence"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{i}. {demo['title']}")
        print(f"   {demo['description']}")
        print(f"   Input: {demo['input']}")
        print("-" * 60)
        
        try:
            start_time = time.time()
            response = run_agent(demo['input'])
            end_time = time.time()
            
            print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
            print(f"🤖 Agent Response:")
            print(response)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "=" * 60)
        
        # Pause between demos
        if i < len(demos):
            input("Press Enter to continue to the next demo...")
    
    print("\n🎉 Demo completed!")
    print("You can now run 'python simple_langgraph_app.py' to interact with the agent directly.")

def interactive_demo():
    """Interactive demo where user can try their own inputs"""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables")
        return
    
    print("\n🎮 Interactive Demo Mode")
    print("Try your own queries! Type 'quit' to exit.")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Thanks for trying the demo!")
            break
        
        try:
            response = run_agent(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    print("Choose demo mode:")
    print("1. Automated demo (recommended)")
    print("2. Interactive demo")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        demo_langgraph_agent()
    elif choice == "2":
        interactive_demo()
    else:
        print("Invalid choice. Running automated demo...")
        demo_langgraph_agent()
