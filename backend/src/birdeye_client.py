"""
Birdeye API Client
=================

A Python client for interacting with the Birdeye API to fetch:
- Token lists and rankings
- Historical price data
- Price analysis and statistics

Features:
    - Token list fetching with sorting and filtering
    - Historical price data with multiple time intervals
    - Price analysis including trends and volatility
    - Detailed error handling and rate limit management
"""

import os
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'), override=False)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env.local'), override=True)
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")

class BirdeyeClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Birdeye API client."""
        self.api_key = api_key or BIRDEYE_API_KEY
        if not self.api_key:
            raise ValueError("API key is required. Set BIRDEYE_API_KEY in .env file")
        
        self.base_url = "https://public-api.birdeye.so"
        self.headers = {
            "accept": "application/json",
            "x-chain": "solana",
            "X-API-KEY": self.api_key
        }
    
    def get_token_list(
        self,
        sort_by: str = "price",
        sort_type: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> Optional[Dict[str, Any]]:
        """Fetch token list with sorting and pagination.
        
        Args:
            sort_by: Field to sort by (e.g., "price", "volume", "marketCap")
            sort_type: Sort direction ("asc" or "desc")
            limit: Number of tokens to fetch
            offset: Starting position for pagination
        """
        url = f"{self.base_url}/defi/tokenlist"
        params = {
            "sort_by": sort_by,
            "sort_type": sort_type,
            "limit": limit,
            "offset": offset
        }
        
        try:
            # Add a small delay to avoid rate limits
            time.sleep(1)
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("❌ Rate limit exceeded. Please wait before trying again.")
            elif e.response.status_code == 400:
                print("❌ Bad request. Check your parameters.")
            else:
                print(f"❌ HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error fetching token list: {e}")
            return None
    
    def get_historical_price(
        self,
        token_address: str,
        interval: str = "5m",
        days_back: int = 1,
        address_type: str = "token"
    ) -> Optional[Dict[str, Any]]:
        """Fetch historical price data for a token.
        
        Args:
            token_address: The token contract address
            interval: Time interval for data points
                - "5m": 5-minute intervals (288 points per day)
                - "1h": 1-hour intervals (24 points per day) - Not currently supported
                - "1d": 1-day intervals (1 point per day) - Not implemented
            days_back: Number of days of historical data to fetch
            address_type: Type of address ('token' or 'pair')
        """
        if not token_address:
            raise ValueError("Token address is required")
        
        # Calculate time range
        end_time = int(time.time())
        start_time = end_time - (days_back * 24 * 60 * 60)
        
        # Format timestamps for display
        start_date = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\nFetching {interval} data for {token_address}")
        print(f"Time range: {start_date} to {end_date}")
        print(f"Expected data points: {days_back * 24 * (60/5 if interval == '5m' else 1)}")
        
        url = f"{self.base_url}/defi/history_price"
        params = {
            "address": token_address,
            "address_type": address_type,
            "type": interval,
            "time_from": start_time,
            "time_to": end_time
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success", False):
                return data
            return None
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("❌ Rate limit exceeded. Please wait before trying again.")
            elif e.response.status_code == 400:
                print("❌ Bad request. Check your parameters.")
            else:
                print(f"❌ HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error fetching historical data: {e}")
            return None

def format_price_data(items: List[Dict[str, Any]], token_name: str) -> None:
    """Format and display price data in a readable way."""
    if not items:
        return
    
    first = items[0]
    last = items[-1]
    
    # Convert timestamps to readable dates
    first_time = datetime.fromtimestamp(first['unixTime']).strftime('%Y-%m-%d %H:%M:%S')
    last_time = datetime.fromtimestamp(last['unixTime']).strftime('%Y-%m-%d %H:%M:%S')
    
    print("\n📊 Price Analysis Summary")
    print(f"Token: {token_name}")
    print(f"Time Period: {first_time} to {last_time}")
    print(f"Number of Data Points: {len(items)}")
    
    # Calculate price statistics
    prices = [item['value'] for item in items]
    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices) / len(prices)
    
    print("\n💰 Price Details:")
    print(f"Starting Price: ${first['value']:.2f}")
    print(f"Current Price:  ${last['value']:.2f}")
    print(f"Highest Price:  ${max_price:.2f}")
    print(f"Lowest Price:   ${min_price:.2f}")
    print(f"Average Price:  ${avg_price:.2f}")
    
    # Calculate price change
    price_change = last['value'] - first['value']
    percent_change = (price_change / first['value']) * 100
    
    print("\n📈 Price Movement:")
    print(f"Total Change: ${price_change:.2f} ({percent_change:+.2f}%)")
    
    # Add trend analysis
    if percent_change > 5:
        trend = "Strongly Bullish 🚀"
    elif percent_change > 0:
        trend = "Slightly Bullish 📈"
    elif percent_change > -5:
        trend = "Slightly Bearish 📉"
    else:
        trend = "Strongly Bearish 🔻"
    
    print(f"Market Trend: {trend}")
    
    # Add volatility analysis
    price_range = max_price - min_price
    volatility = (price_range / avg_price) * 100
    print(f"Price Volatility: {volatility:.1f}%")
    
    if volatility > 10:
        print("⚠️ High volatility detected - significant price swings")
    elif volatility > 5:
        print("ℹ️ Moderate volatility - normal market conditions")
    else:
        print("ℹ️ Low volatility - stable price movement")

def main():
    # Initialize the client
    try:
        client = BirdeyeClient()
        print("API client initialized successfully")
        print(f"Using API Key: {client.api_key[:5]}...{client.api_key[-5:] if client.api_key else 'None'}")
    except Exception as e:
        print(f"Failed to initialize API client: {e}")
        return
    
    # Test token list
    print("\nFetching token list...")
    token_list = client.get_token_list(limit=5)  # Get top 5 tokens
    if token_list and token_list.get("success", False):
        tokens = token_list.get('data', {}).get('items', [])
        print(f"\n✅ Success! Fetched {len(tokens)} tokens")
        for token in tokens:
            print(f"- {token.get('symbol', 'Unknown')}: ${token.get('price', 0):.2f}")
    else:
        print("❌ Token list request failed. Trying price history...")
    
    # Add delay between requests to avoid rate limits
    time.sleep(2)
    
    # Test price history
    print("\nFetching price history...")
    test_case = {
        'name': 'Wrapped SOL (SOL)',
        'address': 'So11111111111111111111111111111111111111112',
        'interval': '5m',
        'days_back': 1
    }
    
    data = client.get_historical_price(
        token_address=test_case['address'],
        interval=test_case['interval'],
        days_back=test_case['days_back']
    )
    
    if data and data.get("success", False):
        items = data.get('data', {}).get('items', [])
        print(f"\n✅ Success! Fetched {len(items)} data points")
        format_price_data(items, test_case['name'])
    else:
        print("❌ Price history request failed. Please check your API key and parameters.")

if __name__ == "__main__":
    main() 
