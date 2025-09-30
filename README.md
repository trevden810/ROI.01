# ROI.01 Sports Betting Analysis Tool

A simple, automated tool for monitoring sports betting odds across multiple bookmakers and identifying arbitrage opportunities. Built for educational and research purposes.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ⚠️ Disclaimer

**This tool is for educational and research purposes only.** Sports betting may be illegal in your jurisdiction. Always gamble responsibly and within your means. The developers are not responsible for any financial losses incurred through the use of this tool.

## Features

- **Multi-Bookmaker Odds Aggregation**: Pull real-time odds from multiple sportsbooks
- **Arbitrage Detection**: Automatically identify guaranteed profit opportunities
- **Multiple Sports Support**: NFL, NBA, MLB, NHL, and more
- **Real-Time Analysis**: Process current odds and upcoming events
- **Simple Setup**: Running in under 5 minutes from git clone
- **Detailed Logging**: Track all analysis and API calls
- **Cost Efficient**: Works with free API tier

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Git
- A free API key from [The Odds API](https://the-odds-api.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/trevden810/ROI.01.git
   cd ROI.01
   ```

2. **Create and activate virtual environment**
   
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**
   ```bash
   # Copy the example environment file
   copy .env.example .env  # Windows
   # OR
   cp .env.example .env    # macOS/Linux
   ```
   
   Edit `.env` and add your API key:
   ```
   ODDS_API_KEY=your_actual_api_key_here
   ```

5. **Run the tool**
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables

Edit the `.env` file to customize behavior:

```bash
# Your API key from https://the-odds-api.com/
ODDS_API_KEY=your_key_here

# Sports to monitor (comma-separated)
ODDS_API_SPORTS=americanfootball_nfl,basketball_nba

# Betting markets to analyze
ODDS_MARKETS=h2h,spreads,totals

# Bookmaker regions
ODDS_REGIONS=us

# Minimum profit percentage to report (2.0 = 2%)
MIN_ARBITRAGE_PROFIT=2.0

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

### Available Sports

Common sport keys you can use in `ODDS_API_SPORTS`:

- `americanfootball_nfl` - NFL
- `basketball_nba` - NBA
- `baseball_mlb` - MLB
- `icehockey_nhl` - NHL
- `soccer_usa_mls` - MLS
- `americanfootball_ncaaf` - NCAA Football
- `basketball_ncaab` - NCAA Basketball

For a complete list, run the tool once and check the console output, or visit [The Odds API Sports List](https://the-odds-api.com/sports-odds-data/sports-apis.html).

## Understanding the Output

### Arbitrage Opportunity Example

```
================================================================================
ARBITRAGE OPPORTUNITY - 3.45% Profit
================================================================================
Event: Kansas City Chiefs vs Buffalo Bills
Sport: americanfootball_nfl
Market: h2h
Start Time: 2025-10-15 20:00:00

BET 1:
  Bookmaker: draftkings
  Outcome: Kansas City Chiefs
  Odds: 2.15
  Stake: $465.12
  Potential Return: $1000.01

BET 2:
  Bookmaker: fanduel
  Outcome: Buffalo Bills
  Odds: 1.92
  Stake: $534.88
  Potential Return: $1026.97

Total Stake: $1000.00
Guaranteed Profit: $26.97
Profit Percentage: 3.45%
================================================================================
```

### Key Metrics Explained

- **Profit Percentage**: The guaranteed return on your total stake
- **Total Stake**: Combined amount to bet across both bookmakers
- **Guaranteed Profit**: Amount you'll profit regardless of outcome
- **Odds**: Decimal odds format (2.00 = even money)

## API Cost Management

The Odds API free tier includes:

- 500 requests per month
- Each call to `get_odds()` counts as 1 request

**Cost-Saving Tips:**

1. Limit the number of sports in `ODDS_API_SPORTS`
2. Run the tool periodically rather than continuously
3. Use the `ODDS_MARKETS` setting to only fetch markets you need
4. Monitor your usage in the console output (shows "requests remaining")

**Estimated Monthly Usage:**

- Running once per day for NFL only: ~30 requests/month
- Running 3x daily for NFL + NBA: ~180 requests/month
- Running hourly during game days: ~400-500 requests/month

## Project Structure

```
ROI.01/
├── src/                     # Source code
│   ├── api/                 # API clients
│   │   ├── base_client.py   # Base API client with retry logic
│   │   └── odds_api.py      # The Odds API client
│   ├── analyzers/           # Analysis modules
│   │   └── arbitrage.py     # Arbitrage detection
│   └── models/              # Data models
│       └── bet.py           # Betting data structures
├── config/                  # Configuration files
│   └── config.yaml          # Application settings
├── data/                    # Data storage (created at runtime)
├── logs/                    # Log files (created at runtime)
├── tests/                   # Unit tests (Phase 2)
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── README.md                # This file
```

## Troubleshooting

### "ERROR: No API key configured!"

**Solution**: 
1. Copy `.env.example` to `.env`
2. Get your free API key from https://the-odds-api.com/
3. Add it to the `.env` file: `ODDS_API_KEY=your_key_here`

### "Rate limit hit"

**Solution**: 
- You've exceeded your API request limit
- Wait 60 seconds, or until the next month if you've used all 500 requests
- Consider upgrading to a paid API plan for higher limits

### "No arbitrage opportunities found"

**Explanation**: 
- This is normal! Arbitrage opportunities are rare
- Bookmakers are efficient and close arbitrage gaps quickly
- Try:
  - Running during major games/events
  - Adding more bookmakers via `ODDS_REGIONS`
  - Lowering `MIN_ARBITRAGE_PROFIT` threshold
  - Checking different sports

### Module Import Errors

**Solution**:
```bash
# Make sure you're in the project directory
cd C:\Projects\ROI.01

# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

## Roadmap

### Phase 1: MVP (Current) ✅
- Basic API integration
- Arbitrage detection
- Console output
- Simple configuration

### Phase 2: Enhanced Features (Planned)
- Database storage for historical tracking
- Value bet detection
- Web dashboard
- Email/Discord alerts
- Unit tests

### Phase 3: Advanced Features (Future)
- Machine learning for probability estimation
- Live betting support
- Multi-currency support
- Mobile app
- Custom strategy builder

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Format code with:

```bash
black src/
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Resources

- [The Odds API Documentation](https://the-odds-api.com/liveapi/guides/v4/)
- [Sports Betting Arbitrage Explained](https://en.wikipedia.org/wiki/Arbitrage_betting)
- [Responsible Gambling Resources](https://www.ncpgambling.org/)

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [The Odds API](https://the-odds-api.com/) for providing sports odds data
- Research document contributors for API recommendations

## Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review The Odds API documentation

---

**Remember**: This tool is for educational purposes. Always gamble responsibly and within your means.
