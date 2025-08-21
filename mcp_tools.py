"""
MCP Tools Module
This module provides the tools from the MCP server without triggering initialization issues
"""

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from dice_roller import DiceRoller
import yfinance as yf

load_dotenv()

def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    try:
        client = TavilyClient(os.getenv("TAVILY_API_KEY"))
        search_results = client.get_search_context(query=query)
        return search_results
    except Exception as e:
        return f"Error searching the web: {str(e)}"

def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    try:
        roller = DiceRoller(notation, num_rolls)
        return str(roller)
    except Exception as e:
        return f"Error rolling dice: {str(e)}"

def yfinance_data(symbol: str) -> str:
    """Get real-time stock data from Yahoo Finance. Use this tool to get current stock prices, market data, and financial metrics for any stock symbol."""
    try:
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
    except Exception as e:
        return f"Error getting stock data: {str(e)}"
