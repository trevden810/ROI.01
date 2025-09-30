"""
Client for The Odds API
Documentation: https://the-odds-api.com/liveapi/guides/v4/
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base_client import BaseAPIClient
from ..models.bet import Event, Odds

logger = logging.getLogger(__name__)


class OddsAPIClient(BaseAPIClient):
    """Client for interacting with The Odds API"""
    
    def __init__(self, api_key: str, timeout: int = 30, retry_attempts: int = 3):
        """
        Initialize Odds API client
        
        Args:
            api_key: Your Odds API key from https://the-odds-api.com/
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts
        """
        super().__init__(
            base_url="https://api.the-odds-api.com/v4",
            api_key=api_key,
            timeout=timeout,
            retry_attempts=retry_attempts
        )
        
    def get_sports(self) -> List[Dict[str, Any]]:
        """
        Get list of available sports
        
        Returns:
            List of sports with their keys and details
        """
        logger.info("Fetching available sports...")
        return self._make_request("sports")
    
    def get_odds(self, sport: str, regions: str = 'us', 
                 markets: str = 'h2h', odds_format: str = 'decimal',
                 date_format: str = 'iso') -> List[Event]:
        """
        Get current odds for a specific sport
        
        Args:
            sport: Sport key (e.g., 'americanfootball_nfl', 'basketball_nba')
            regions: Bookmaker regions (us, uk, eu, au) - comma-separated
            markets: Bet markets (h2h, spreads, totals) - comma-separated
            odds_format: Format for odds (decimal or american)
            date_format: Format for dates (iso or unix)
        
        Returns:
            List of Event objects with odds data
        """
        logger.info(f"Fetching odds for {sport}...")
        
        params = {
            'regions': regions,
            'markets': markets,
            'oddsFormat': odds_format,
            'dateFormat': date_format
        }
        
        response = self._make_request(f"sports/{sport}/odds", params=params)
        
        # Parse response into Event objects
        events = []
        for event_data in response:
            events.append(self._parse_event(event_data))
        
        logger.info(f"Retrieved {len(events)} events for {sport}")
        return events
    
    def _parse_event(self, data: Dict[str, Any]) -> Event:
        """
        Parse raw API response into Event object
        
        Args:
            data: Raw event data from API
        
        Returns:
            Event object
        """
        # Parse odds from all bookmakers
        odds_list = []
        bookmakers = []
        
        for bookmaker_data in data.get('bookmakers', []):
            bookmaker_name = bookmaker_data['key']
            bookmakers.append(bookmaker_name)
            
            for market in bookmaker_data.get('markets', []):
                market_type = market['key']
                
                for outcome in market.get('outcomes', []):
                    odds_list.append(Odds(
                        bookmaker=bookmaker_name,
                        market=market_type,
                        outcome=outcome['name'],
                        price=outcome['price'],
                        point=outcome.get('point'),
                        last_update=datetime.fromisoformat(
                            bookmaker_data['last_update'].replace('Z', '+00:00')
                        )
                    ))
        
        # Create Event object
        return Event(
            id=data['id'],
            sport=data['sport_key'],
            commence_time=datetime.fromisoformat(
                data['commence_time'].replace('Z', '+00:00')
            ),
            home_team=data['home_team'],
            away_team=data['away_team'],
            bookmakers=bookmakers,
            odds_data=odds_list
        )
    
    def get_event_odds(self, sport: str, event_id: str, regions: str = 'us',
                       markets: str = 'h2h', odds_format: str = 'decimal') -> Optional[Event]:
        """
        Get odds for a specific event
        
        Args:
            sport: Sport key
            event_id: Unique event identifier
            regions: Bookmaker regions
            markets: Bet markets
            odds_format: Format for odds
        
        Returns:
            Event object or None if not found
        """
        logger.info(f"Fetching odds for event {event_id}...")
        
        params = {
            'regions': regions,
            'markets': markets,
            'oddsFormat': odds_format,
            'dateFormat': 'iso'
        }
        
        try:
            response = self._make_request(
                f"sports/{sport}/odds/{event_id}", 
                params=params
            )
            return self._parse_event(response)
        except Exception as e:
            logger.error(f"Failed to fetch event {event_id}: {str(e)}")
            return None
