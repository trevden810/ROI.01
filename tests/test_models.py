"""
Unit tests for data models
"""

import pytest
from datetime import datetime
from src.models.bet import (
    Odds, Event, ArbitrageOpportunity,
    convert_american_to_decimal,
    convert_decimal_to_american,
    calculate_implied_probability
)


class TestOddsConversion:
    """Test odds conversion functions"""
    
    def test_american_to_decimal_positive(self):
        """Test conversion of positive American odds"""
        assert convert_american_to_decimal(150) == pytest.approx(2.5, 0.01)
        assert convert_american_to_decimal(200) == pytest.approx(3.0, 0.01)
    
    def test_american_to_decimal_negative(self):
        """Test conversion of negative American odds"""
        assert convert_american_to_decimal(-110) == pytest.approx(1.91, 0.01)
        assert convert_american_to_decimal(-200) == pytest.approx(1.5, 0.01)
    
    def test_decimal_to_american_favorites(self):
        """Test conversion of decimal odds for favorites"""
        assert convert_decimal_to_american(1.5) == pytest.approx(-200, 0.1)
        assert convert_decimal_to_american(1.91) == pytest.approx(-110, 1)
    
    def test_decimal_to_american_underdogs(self):
        """Test conversion of decimal odds for underdogs"""
        assert convert_decimal_to_american(2.5) == pytest.approx(150, 0.1)
        assert convert_decimal_to_american(3.0) == pytest.approx(200, 0.1)
    
    def test_implied_probability(self):
        """Test implied probability calculation"""
        assert calculate_implied_probability(2.0) == pytest.approx(0.5, 0.01)
        assert calculate_implied_probability(4.0) == pytest.approx(0.25, 0.01)
        assert calculate_implied_probability(1.5) == pytest.approx(0.6667, 0.01)


class TestDataModels:
    """Test data model creation"""
    
    def test_odds_creation(self):
        """Test Odds dataclass creation"""
        odds = Odds(
            bookmaker="draftkings",
            market="h2h",
            outcome="Kansas City Chiefs",
            price=2.15,
            last_update=datetime.now()
        )
        assert odds.bookmaker == "draftkings"
        assert odds.price == 2.15
        assert odds.point is None
    
    def test_event_creation(self):
        """Test Event dataclass creation"""
        event = Event(
            id="test123",
            sport="americanfootball_nfl",
            commence_time=datetime.now(),
            home_team="Chiefs",
            away_team="Bills",
            bookmakers=["draftkings", "fanduel"],
            odds_data=[]
        )
        assert event.sport == "americanfootball_nfl"
        assert len(event.bookmakers) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
