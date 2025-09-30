"""
Data models for betting opportunities and odds
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Odds:
    """Represents odds from a single bookmaker"""
    bookmaker: str
    market: str  # h2h, spreads, totals
    outcome: str  # home, away, over, under, etc.
    price: float  # American or Decimal odds
    point: Optional[float] = None  # For spreads and totals
    last_update: Optional[datetime] = None


@dataclass
class Event:
    """Represents a sporting event"""
    id: str
    sport: str
    commence_time: datetime
    home_team: str
    away_team: str
    bookmakers: List[str]
    odds_data: List[Odds]


@dataclass
class ArbitrageOpportunity:
    """Represents an identified arbitrage opportunity"""
    event: Event
    bookmaker_1: str
    outcome_1: str
    odds_1: float
    bookmaker_2: str
    outcome_2: str
    odds_2: float
    profit_percentage: float
    stake_1: float
    stake_2: float
    guaranteed_profit: float
    market_type: str
    timestamp: datetime


@dataclass
class ValueBet:
    """Represents an identified value betting opportunity"""
    event: Event
    bookmaker: str
    outcome: str
    offered_odds: float
    true_probability: float
    edge_percentage: float
    recommended_stake: float
    expected_value: float
    market_type: str
    timestamp: datetime


def convert_american_to_decimal(american_odds: float) -> float:
    """
    Convert American odds to decimal format
    
    Args:
        american_odds: Odds in American format (e.g., -110, +150)
    
    Returns:
        Decimal odds (e.g., 1.91, 2.50)
    """
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1


def convert_decimal_to_american(decimal_odds: float) -> float:
    """
    Convert decimal odds to American format
    
    Args:
        decimal_odds: Odds in decimal format (e.g., 1.91, 2.50)
    
    Returns:
        American odds (e.g., -110, +150)
    """
    if decimal_odds >= 2.0:
        return (decimal_odds - 1) * 100
    else:
        return -100 / (decimal_odds - 1)


def calculate_implied_probability(decimal_odds: float) -> float:
    """
    Calculate implied probability from decimal odds
    
    Args:
        decimal_odds: Odds in decimal format
    
    Returns:
        Implied probability as a decimal (0-1)
    """
    return 1 / decimal_odds
