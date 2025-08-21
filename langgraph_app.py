import os
import asyncio
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
import subprocess
import json

load_dotenv()

# Define the state structure
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage | ToolMessage], "The messages in the conversation"]
    next: str

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Custom tools that will call the MCP server tools
@tool
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    try:
        # Call the MCP server using subprocess
        result = subprocess.run(
            ["python", "server.py"],
            input=json.dumps({
                "method": "tools/call",
                "params": {
                    "name": "web_search",
                    "arguments": {"query": query}
                }
            }),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"Error calling web search: {str(e)}"

@tool
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation (e.g., '2d6', '1d20')"""
    try:
        result = subprocess.run(
            ["python", "server.py"],
            input=json.dumps({
                "method": "tools/call",
                "params": {
                    "name": "roll_dice",
                    "arguments": {"notation": notation, "num_rolls": num_rolls}
                }
            }),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"Error rolling dice: {str(e)}"

@tool
def get_stock_data(symbol: str) -> str:
    """Get real-time stock data from Yahoo Finance for the given symbol"""
    try:
        result = subprocess.run(
            ["python", "server.py"],
            input=json.dumps({
                "method": "tools/call",
                "params": {
                    "name": "yfinance_data",
                    "arguments": {"symbol": symbol}
                }
            }),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"Error getting stock data: {str(e)}"

# Create the tool node
tools = [web_search, roll_dice, get_stock_data]
tool_node = ToolNode(tools)

# Define the agent function
def agent(state: AgentState) -> AgentState:
    """The main agent that decides what to do next"""
    messages = state["messages"]
    
    # Get the response from the LLM
    response = llm.invoke(messages)
    
    # Check if the response contains tool calls
    if response.tool_calls:
        # If there are tool calls, we need to execute them
        return {"messages": [response], "next": "tools"}
    else:
        # If no tool calls, we're done
        return {"messages": [response], "next": END}

# Define the should_continue function
def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end"""
    last_message = state["messages"][-1]
    
    # If the last message is from a tool, we should continue
    if isinstance(last_message, ToolMessage):
        return "agent"
    else:
        return END

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)

# Add edges
workflow.add_edge("tools", "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

# Set the entry point
workflow.set_entry_point("agent")

# Compile the graph
app = workflow.compile()

# Function to run the application
def run_agent(user_input: str) -> str:
    """Run the agent with the given user input"""
    messages = [HumanMessage(content=user_input)]
    result = app.invoke({"messages": messages})
    
    # Return the last AI message
    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage):
            return message.content
    
    return "No response generated"

# Example usage
if __name__ == "__main__":
    print("🤖 LangGraph MCP Agent")
    print("Available tools: web search, dice rolling, stock data")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        try:
            response = run_agent(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nError: {str(e)}")
