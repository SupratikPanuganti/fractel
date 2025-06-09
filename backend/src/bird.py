#get all data from birdeye

import pandas as pd
import datetime
import requests
import time, json
import pprint
import re as reggie
from termcolor import cprint
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'), override=False)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env.local'), override=True)

def token_list():
    url = "https://public-api.birdeye.so/defi/tokenlist"
    
    # Get API key from environment variables
    BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
    if not BIRDEYE_API_KEY:
        raise ValueError("BIRDEYE_API_KEY not found in environment variables")
    
    headers = {"x-chain": "solana", "X-API-KEY": BIRDEYE_API_KEY}
    
    offset = 0
    limit = 100  # Using a reasonable limit instead of -1
    
    params = {
        "sort_by": "v24ChangePercent", 
        "sort_type": "desc", 
        "offset": offset, 
        "limit": limit
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    print("Testing Birdeye API key...")
    test_api_key()