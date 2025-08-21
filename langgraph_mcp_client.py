import os
import asyncio
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from mcp.client.stdio import stdio_client
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

# MCP Client setup
async def get_mcp_client():
    """Get an MCP client connected to our server"""
    client = await stdio_client(["python", "server.py"])
    return client

# Custom tools that will call the MCP server
@tool
async def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    try:
        client = await get_mcp_client()
        result = await client.call_tool("web_search", {"query": query})
        await client.aclose()
        return result.content[0].text if result.content else "No results found"
    except Exception as e:
        return f"Error calling web search: {str(e)}"

@tool
async def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation (e.g., '2d6', '1d20')"""
    try:
        client = await get_mcp_client()
        result = await client.call_tool("roll_dice", {"notation": notation, "num_rolls": num_rolls})
        await client.aclose()
        return result.content[0].text if result.content else "Error rolling dice"
    except Exception as e:
        return f"Error rolling dice: {str(e)}"

@tool
async def get_stock_data(symbol: str) -> str:
    """Get real-time stock data from Yahoo Finance for the given symbol"""
    try:
        client = await get_mcp_client()
        result = await client.call_tool("yfinance_data", {"symbol": symbol})
        await client.aclose()
        return result.content[0].text if result.content else "No stock data found"
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
async def run_agent(user_input: str) -> str:
    """Run the agent with the given user input"""
    messages = [HumanMessage(content=user_input)]
    result = await app.ainvoke({"messages": messages})
    
    # Return the last AI message
    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage):
            return message.content
    
    return "No response generated"

# Example usage
async def main():
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
            response = await run_agent(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
