import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import dotenv
from birdeyepy import BirdEye

# Load environment variables
dotenv.load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'), override=False)
dotenv.load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env.local'), override=True)
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")

class BirdeyeAPI:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Birdeye API client.
        
        Args:
            api_key: Optional API key. If not provided, will use BIRDEYE_API_KEY from environment.
        """
        self.api_key = api_key or BIRDEYE_API_KEY
        if not self.api_key:
            raise ValueError("API key is required. Set BIRDEYE_API_KEY in .env file")
            
        # Initialize the Birdeye client
        self.client = BirdEye(api_key=self.api_key)
    
    def get_historical_price(
        self,
        token_address: str,
        interval: str = "1h",
        days_back: int = 7,
        address_type: str = "token"
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch historical price data for a token using Birdeye API.
        
        Args:
            token_address: The token contract address
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 1d)
            days_back: Number of days of historical data to fetch
            address_type: Type of address ('token' or 'pair')
            
        Returns:
            dict: Historical price data or None if request fails
        """
        if not token_address:
            raise ValueError("Token address is required")
            
        # Calculate time range
        end_time = int(time.time())
        start_time = end_time - (days_back * 24 * 60 * 60)  # Convert days to seconds
        
        print(f"Fetching {interval} data for {token_address} from {start_time} to {end_time}")
        
        try:
            # Use the birdeyepy client to fetch historical data
            result = self.client.defi.history(
                address=token_address,
                time_from=start_time,
                time_to=end_time,
                address_type=address_type,
                type_in_time=interval
            )
            
            # Format the response to match our expected format
            if result and hasattr(result, 'get') and result.get('success', False):
                return {
                    'success': True,
                    'data': {
                        'items': result.get('data', {}).get('items', [])
                    }
                }
            return None
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None

def main():
    # Initialize the API client
    try:
        api = BirdeyeAPI()
        print("API client initialized successfully")
        print(f"Using API Key: {api.api_key[:5]}...{api.api_key[-5:] if api.api_key else 'None'}")
    except Exception as e:
        print(f"Failed to initialize API client: {e}")
        if "BIRDEYE_API_KEY" not in os.environ:
            print("Error: BIRDEYE_API_KEY not found in environment variables")
        return
    
    # Try with different token addresses and intervals
    test_cases = [
        {
            'name': 'Wrapped SOL',
            'address': 'So11111111111111111111111111111111111111112',
            'interval': '1h',
            'days_back': 1
        },
        {
            'name': 'USDC',
            'address': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
            'interval': '1h',
            'days_back': 1
        },
        {
            'name': 'Wrapped SOL - 5min',
            'address': 'So11111111111111111111111111111111111111112',
            'interval': '5m',
            'days_back': 1
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing {test['name']} ({test['address']})")
        print(f"Interval: {test['interval']}, Days back: {test['days_back']}")
        
        try:
            data = api.get_historical_price(
                token_address=test['address'],
                interval=test['interval'],
                days_back=test['days_back']
            )
            
            if data and data.get("success", False):
                items = data.get('data', {}).get('items', [])
                print(f"\n✅ Success! Fetched {len(items)} data points")
                if items:
                    print("\nFirst data point:", items[0])
                    print("Last data point: ", items[-1])
                break  # Stop at first successful test
            else:
                print("❌ Request failed. Trying next test case...")
        except Exception as e:
            print(f"❌ Error during request: {e}")
            print("Trying next test case...")

if __name__ == "__main__":
    main()