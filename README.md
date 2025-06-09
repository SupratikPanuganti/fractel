# Fractel Project

A Python project for interacting with the Birdeye API to fetch token data and price history.

## Structure

- `backend/` - Python backend code and tests
  - `src/` - Source code for the backend
    - `birdeye_client.py` - Combined Birdeye API client for token lists and price history
    - `test_birdeye_key.py` - API key testing utility
  - `tests/` - Test files
  - `requirements.txt` - Python dependencies
- `frontend/` - Frontend code (add your framework or static files here)
- `docs/` - Project documentation

## Prerequisites

- Python 3.8 or higher
- Birdeye API key

## Getting Started

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd fractel
   ```

2. Install dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   - Create a `.env` file in the `backend/` directory
   - Add your Birdeye API key:
     ```
     BIRDEYE_API_KEY=your_api_key_here
     ```

4. Test your API key:

   ```bash
   python src/test_birdeye_key.py
   ```

5. Run the Birdeye client:

   ```bash
   python src/birdeye_client.py
   ```

## Features

### Token List

- Fetch top tokens by market cap
- Sort by various metrics (price, volume, etc.)
- Pagination support

### Price History

- Historical price data with 5-minute intervals
- Price analysis including:
  - Price trends (bullish/bearish)
  - Volatility analysis
  - High/low/average prices
  - Price movement statistics

### API Features

- Rate limit handling
- Error management
- Environment variable support
- Detailed logging

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Feel free to expand this README as your project grows!
