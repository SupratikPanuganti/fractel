# Fractel Project

A Python project for interacting with the Birdeye API to fetch token data and price history.

## Structure

- `backend/` - Python backend code and tests
  - `src/` - Source code for the backend
    - `bird.py` - Core Birdeye API interactions
    - `pricehistory.py` - Historical price data fetching
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

5. Run other scripts from `backend/src/`:
   ```bash
   python src/bird.py
   python src/pricehistory.py
   ```

## Features

- Token list fetching
- Historical price data retrieval
- API key validation
- Environment variable management

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
