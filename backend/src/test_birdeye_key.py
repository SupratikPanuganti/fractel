import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env and .env.local if present
env_path = os.path.join(os.path.dirname(__file__), '../.env')
local_env_path = os.path.join(os.path.dirname(__file__), '../.env.local')

print(f"Looking for .env files at:")
print(f"Main .env: {env_path}")
print(f"Local .env: {local_env_path}")

load_dotenv(dotenv_path=env_path, override=False)
load_dotenv(dotenv_path=local_env_path, override=True)

# Print all environment variables (for debugging)
print("\nEnvironment variables:")
print(f"BIRDEYE_API_KEY exists: {'BIRDEYE_API_KEY' in os.environ}")
print(f"BIRDEYE_API_KEY value: {os.getenv('BIRDEYE_API_KEY', 'Not found')}")

def test_api_key():
    """Test if the Birdeye API key is working by making a simple request."""
    url = "https://public-api.birdeye.so/defi/tokenlist"
    
    BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
    if not BIRDEYE_API_KEY:
        print("❌ BIRDEYE_API_KEY not found in environment variables")
        return False
    
    headers = {"x-chain": "solana", "X-API-KEY": BIRDEYE_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("✅ API Key is working!")
        print(f"Response status: {response.status_code}")
        print(f"Number of tokens returned: {len(data.get('data', []))}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ API Key test failed: {e}")
        return False

if __name__ == "__main__":
    print("\nTesting Birdeye API key...")
    test_api_key() 