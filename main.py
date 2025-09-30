"""
ROI.01 Sports Betting Analysis Tool - Main Entry Point
A simple tool for monitoring sports betting odds and identifying opportunities
"""

import os
import sys
import logging
import yaml
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.api.odds_api import OddsAPIClient
from src.analyzers.arbitrage import ArbitrageAnalyzer


def setup_logging(log_level: str = 'INFO', log_to_file: bool = True):
    """
    Configure logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_to_file: Whether to log to file in addition to console
    """
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Set up handlers
    handlers = [logging.StreamHandler()]
    
    if log_to_file:
        log_file = log_dir / f'roi_{datetime.now().strftime("%Y%m%d")}.log'
        handlers.append(logging.FileHandler(log_file))
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )


def load_config():
    """
    Load configuration from config.yaml and environment variables
    
    Returns:
        Dictionary with configuration settings
    """
    # Load .env file
    load_dotenv()
    
    # Load yaml config
    config_path = Path('config/config.yaml')
    if config_path.exists():
        with open(config_path, 'r') as f:
            yaml_config = yaml.safe_load(f)
    else:
        yaml_config = {}
    
    # Build configuration with environment variables taking precedence
    config = {
        'api_key': os.getenv('ODDS_API_KEY'),
        'sports': os.getenv('ODDS_API_SPORTS', 'americanfootball_nfl').split(','),
        'markets': os.getenv('ODDS_MARKETS', 'h2h,spreads,totals'),
        'regions': os.getenv('ODDS_REGIONS', 'us'),
        'min_arbitrage_profit': float(os.getenv('MIN_ARBITRAGE_PROFIT', '2.0')),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'log_to_file': os.getenv('LOG_TO_FILE', 'true').lower() == 'true'
    }
    
    return config


def validate_config(config):
    """
    Validate configuration and check for required settings
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, False otherwise
    """
    if not config['api_key'] or config['api_key'] == 'your_api_key_here':
        print("\n" + "=" * 80)
        print("ERROR: No API key configured!")
        print("=" * 80)
        print("\nPlease follow these steps:")
        print("1. Get a free API key at: https://the-odds-api.com/")
        print("2. Copy .env.example to .env")
        print("3. Add your API key to the .env file")
        print("\nExample:")
        print("  ODDS_API_KEY=1234567890abcdef")
        print("=" * 80)
        return False
    
    return True


def display_welcome():
    """Display welcome message and tool information"""
    print("\n" + "=" * 80)
    print(" ROI.01 SPORTS BETTING ANALYSIS TOOL ".center(80))
    print("=" * 80)
    print("\nVersion: 0.1.0 (MVP)")
    print("Purpose: Monitor odds and identify arbitrage opportunities")
    print("\nDISCLAIMER: This tool is for educational and research purposes only.")
    print("Sports betting may be illegal in your jurisdiction. Always gamble responsibly.")
    print("=" * 80 + "\n")


def main():
    """Main application entry point"""
    
    # Display welcome message
    display_welcome()
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Setup logging
    setup_logging(config['log_level'], config['log_to_file'])
    logger = logging.getLogger(__name__)
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    logger.info("Starting ROI.01 Sports Betting Analyzer")
    logger.info(f"Monitoring sports: {', '.join(config['sports'])}")
    logger.info(f"Markets: {config['markets']}")
    logger.info(f"Regions: {config['regions']}")
    
    try:
        # Initialize API client
        logger.info("Connecting to The Odds API...")
        client = OddsAPIClient(api_key=config['api_key'])
        
        # Test API connection by getting available sports
        print("\nFetching available sports...")
        sports = client.get_sports()
        print(f"[OK] Successfully connected! {len(sports)} sports available")
        
        # Initialize analyzer
        analyzer = ArbitrageAnalyzer(
            min_profit_percentage=config['min_arbitrage_profit']
        )
        
        # Process each sport
        all_opportunities = []
        
        for sport in config['sports']:
            sport = sport.strip()
            print(f"\n{'=' * 80}")
            print(f"Analyzing: {sport.upper()}")
            print(f"{'=' * 80}")
            
            try:
                # Fetch odds
                events = client.get_odds(
                    sport=sport,
                    regions=config['regions'],
                    markets=config['markets']
                )
                
                print(f"Retrieved {len(events)} events")
                
                if not events:
                    print("No events currently available for this sport")
                    continue
                
                # Display sample event info
                print("\nSample Event:")
                sample = events[0]
                print(f"  {sample.home_team} vs {sample.away_team}")
                print(f"  Start: {sample.commence_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Bookmakers: {len(sample.bookmakers)}")
                print(f"  Total odds entries: {len(sample.odds_data)}")
                
                # Find arbitrage opportunities
                print("\nSearching for arbitrage opportunities...")
                opportunities = analyzer.find_arbitrage(events)
                
                if opportunities:
                    print(f"\n[TARGET] Found {len(opportunities)} arbitrage opportunity(ies)!\n")
                    for opp in opportunities:
                        print(analyzer.format_opportunity(opp))
                        print()
                    all_opportunities.extend(opportunities)
                else:
                    print("No arbitrage opportunities found at this time")
                
            except Exception as e:
                logger.error(f"Error processing {sport}: {str(e)}")
                print(f"[WARNING] Error processing {sport}: {str(e)}")
        
        # Summary
        print("\n" + "=" * 80)
        print(" ANALYSIS COMPLETE ".center(80))
        print("=" * 80)
        print(f"\nTotal arbitrage opportunities found: {len(all_opportunities)}")
        
        if all_opportunities:
            print("\nBest opportunity:")
            best = max(all_opportunities, key=lambda x: x.profit_percentage)
            print(f"  {best.event.home_team} vs {best.event.away_team}")
            print(f"  Profit: {best.profit_percentage:.2f}%")
            print(f"  Guaranteed return: ${best.guaranteed_profit:.2f}")
        
        print("\n" + "=" * 80)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"\n[ERROR] Fatal error: {str(e)}")
        print("Check logs/roi_*.log for details")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()
    
    logger.info("ROI.01 analyzer finished")
    print("\nThank you for using ROI.01!")


if __name__ == "__main__":
    main()
