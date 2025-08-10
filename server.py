from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dice_roller import DiceRoller

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

"""
Add your own tool here, and then use it through Cursor!
"""
@mcp.tool()
def yfinance_data(symbol: str) -> str:
    """Get real-time stock data from Yahoo Finance. Use this tool to get current stock prices, market data, and financial metrics for any stock symbol."""

    import yfinance as yf
            
    # Clean and validate symbol
    symbol = symbol.upper().strip()
    if not symbol or len(symbol) > 10:
        return f"Invalid stock symbol: {symbol}"
    
    
    ticker = yf.Ticker(symbol)
    
    # Get basic info first
    info = ticker.info
    
    # Check if we got valid data
    if not info or info.get('regularMarketPrice') is None:
        return f"No data found for stock symbol: {symbol}. Please verify the symbol is correct."
    
    # Format the result
    result = f"Stock: {symbol}\n"
    result += f"Price: ${info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))}\n"
    result += f"Previous Close: ${info.get('previousClose', 'N/A')}\n"
    result += f"Change: {info.get('regularMarketChange', 'N/A')}\n"
    result += f"Change %: {info.get('regularMarketChangePercent', 'N/A')}%\n"
    result += f"Volume: {info.get('volume', 'N/A'):,}\n" if info.get('volume') else "Volume: N/A\n"
    result += f"Market Cap: ${info.get('marketCap', 'N/A'):,}\n" if info.get('marketCap') else "Market Cap: N/A\n"
    result += f"P/E Ratio: {info.get('trailingPE', 'N/A')}\n"
    result += f"Dividend Yield: {info.get('dividendYield', 'N/A')}\n"
    result += f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}\n"
    result += f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}\n"
    
    
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")