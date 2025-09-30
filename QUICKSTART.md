# ROI.01 Quick Start Guide

## Get Running in 5 Minutes

### Step 1: Get Your API Key (2 minutes)
1. Go to https://the-odds-api.com/
2. Click "Sign Up" or "Get API Key"
3. Create a free account
4. Copy your API key (it looks like: `a1b2c3d4e5f6g7h8i9j0`)

### Step 2: Run Setup Script (2 minutes)

**On Windows:**
```bash
cd C:\Projects\ROI.01
setup.bat
```

**On macOS/Linux:**
```bash
cd /path/to/ROI.01
chmod +x setup.sh
./setup.sh
```

### Step 3: Add Your API Key (30 seconds)

Open the `.env` file in a text editor and replace `your_api_key_here` with your actual API key:

```
ODDS_API_KEY=a1b2c3d4e5f6g7h8i9j0
```

### Step 4: Run the Tool (30 seconds)

```bash
python main.py
```

## That's It!

You should see output like:

```
================================================================================
                 ROI.01 SPORTS BETTING ANALYSIS TOOL                
================================================================================

Fetching available sports...
✓ Successfully connected! 40 sports available

================================================================================
Analyzing: AMERICANFOOTBALL_NFL
================================================================================
Retrieved 15 events

Sample Event:
  Kansas City Chiefs vs Buffalo Bills
  Start: 2025-10-15 20:00:00
  Bookmakers: 8
  Total odds entries: 48

Searching for arbitrage opportunities...
🎯 Found 1 arbitrage opportunity(ies)!
...
```

## Customization

Edit the `.env` file to customize:

```bash
# Monitor multiple sports
ODDS_API_SPORTS=americanfootball_nfl,basketball_nba,baseball_mlb

# Change minimum profit threshold
MIN_ARBITRAGE_PROFIT=3.0

# Add more bookmaker regions
ODDS_REGIONS=us,uk,eu
```

## Troubleshooting

**"ERROR: No API key configured!"**
- Make sure you copied `.env.example` to `.env`
- Make sure you replaced `your_api_key_here` with your actual key

**"Module not found" errors**
- Make sure your virtual environment is activated
- Run: `pip install -r requirements.txt`

**No arbitrage opportunities found**
- This is normal - they're rare!
- Try during major game days
- Lower the `MIN_ARBITRAGE_PROFIT` threshold
- Add more regions to `ODDS_REGIONS`

## What's Next?

- Check the full [README.md](README.md) for detailed documentation
- Explore the configuration options in `.env`
- Review logs in `logs/` directory
- Star the repo if you find it useful!

## Need Help?

- Check the main README.md
- Review The Odds API docs: https://the-odds-api.com/liveapi/guides/v4/
- Open an issue on GitHub
