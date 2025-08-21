# LangGraph MCP Agent

This is a simple LangGraph application that interacts with your MCP (Model Context Protocol) Server. The application uses LangGraph to create an intelligent agent that can use the tools provided by your MCP server.

## Features

The LangGraph agent can use the following tools from your MCP server:

1. **Web Search** - Search the web for information using Tavily
2. **Dice Rolling** - Roll dice with various notations (e.g., '2d6', '1d20')
3. **Stock Data** - Get real-time stock information from Yahoo Finance

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # or if using uv
   uv sync
   ```

2. **Environment Variables**
   Create a `.env` file with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

3. **Run the Application**
   ```bash
   python simple_langgraph_app.py
   ```

## Available Applications

### 1. Simple LangGraph App (`simple_langgraph_app.py`)
This is the recommended version that directly imports the MCP server functions. It's simpler and more reliable.

**Features:**
- Direct integration with MCP server functions
- Synchronous execution
- Easy to understand and modify

### 2. LangGraph with MCP Client (`langgraph_mcp_client.py`)
This version uses the MCP client library for more sophisticated integration.

**Features:**
- Uses MCP client library
- Asynchronous execution
- More complex but potentially more flexible

### 3. Basic LangGraph App (`langgraph_app.py`)
This version uses subprocess calls to interact with the MCP server.

**Features:**
- Subprocess-based communication
- Good for learning purposes
- Less efficient than direct imports

## Usage Examples

Once you run the application, you can interact with it using natural language:

```
You: Search for information about artificial intelligence
Agent: [Will use web search tool to find AI information]

You: Roll 3d6 for my character's strength
Agent: [Will use dice rolling tool to roll 3 six-sided dice]

You: What's the current stock price of AAPL?
Agent: [Will use stock data tool to get Apple's stock information]

You: Search for the latest news about Tesla and then get their stock price
Agent: [Will use both web search and stock data tools]
```

## How It Works

1. **State Management**: The application uses a `StateGraph` to manage conversation state
2. **Tool Integration**: MCP server functions are wrapped as LangChain tools
3. **Agent Logic**: The LLM decides which tools to use based on user input
4. **Tool Execution**: Tools are executed and results are returned to the user

## Architecture

```
User Input → LangGraph Agent → LLM Decision → Tool Execution → Response
```

The LangGraph workflow:
1. User provides input
2. Agent processes input with LLM
3. LLM decides if tools are needed
4. If tools are needed, they are executed
5. Results are processed and response is generated
6. Process continues until no more tools are needed

## Customization

You can easily extend this application by:

1. **Adding New Tools**: Import new functions from your MCP server and wrap them as tools
2. **Modifying Agent Logic**: Change the agent function to implement different decision-making logic
3. **Adding Memory**: Implement conversation memory using LangGraph's memory features
4. **Multi-Agent Systems**: Create multiple agents that can collaborate

## Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is set in the `.env` file
- **Import Errors**: Ensure all dependencies are installed
- **Tool Execution Errors**: Check that your MCP server is working correctly
- **Network Issues**: Some tools require internet connectivity

## Next Steps

To enhance this application, consider:

1. Adding conversation memory
2. Implementing multi-turn conversations
3. Adding more sophisticated error handling
4. Creating a web interface
5. Adding authentication and user management
6. Implementing streaming responses
