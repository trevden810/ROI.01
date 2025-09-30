"""
Arbitrage detection and analysis
"""

import logging
from typing import List, Dict, Tuple
from datetime import datetime
from ..models.bet import Event, Odds, ArbitrageOpportunity, calculate_implied_probability

logger = logging.getLogger(__name__)


class ArbitrageAnalyzer:
    """Analyzer for detecting arbitrage opportunities in betting markets"""
    
    def __init__(self, min_profit_percentage: float = 2.0, max_stake: float = 1000):
        """
        Initialize arbitrage analyzer
        
        Args:
            min_profit_percentage: Minimum profit percentage to report (default 2%)
            max_stake: Maximum total stake for calculations (default $1000)
        """
        self.min_profit_percentage = min_profit_percentage
        self.max_stake = max_stake
        
    def find_arbitrage(self, events: List[Event]) -> List[ArbitrageOpportunity]:
        """
        Find all arbitrage opportunities in a list of events
        
        Args:
            events: List of Event objects with odds data
        
        Returns:
            List of ArbitrageOpportunity objects
        """
        opportunities = []
        
        for event in events:
            # Check h2h (moneyline) markets
            h2h_arbs = self._check_two_way_market(event, 'h2h')
            opportunities.extend(h2h_arbs)
            
            # Check totals markets (over/under)
            totals_arbs = self._check_two_way_market(event, 'totals')
            opportunities.extend(totals_arbs)
        
        logger.info(f"Found {len(opportunities)} arbitrage opportunities")
        return opportunities
    
    def _check_two_way_market(self, event: Event, market_type: str) -> List[ArbitrageOpportunity]:
        """
        Check for arbitrage in two-way markets (h2h, totals)
        
        Args:
            event: Event to analyze
            market_type: Type of market ('h2h' or 'totals')
        
        Returns:
            List of arbitrage opportunities found
        """
        opportunities = []
        
        # Get all odds for this market type
        market_odds = [o for o in event.odds_data if o.market == market_type]
        
        if not market_odds:
            return opportunities
        
        # Group odds by outcome
        odds_by_outcome = self._group_odds_by_outcome(market_odds)
        
        # For h2h, we typically have 2 outcomes (home/away)
        # For totals, we have 2 outcomes (over/under)
        if len(odds_by_outcome) != 2:
            return opportunities
        
        outcomes = list(odds_by_outcome.keys())
        
        # Get best odds for each outcome
        best_odds_1 = max(odds_by_outcome[outcomes[0]], key=lambda x: x.price)
        best_odds_2 = max(odds_by_outcome[outcomes[1]], key=lambda x: x.price)
        
        # Calculate if arbitrage exists
        implied_prob_1 = calculate_implied_probability(best_odds_1.price)
        implied_prob_2 = calculate_implied_probability(best_odds_2.price)
        total_implied_prob = implied_prob_1 + implied_prob_2
        
        # Arbitrage exists when total implied probability < 1
        if total_implied_prob < 1:
            profit_percentage = ((1 / total_implied_prob) - 1) * 100
            
            if profit_percentage >= self.min_profit_percentage:
                # Calculate optimal stakes
                stake_1 = self.max_stake * (implied_prob_1 / total_implied_prob)
                stake_2 = self.max_stake * (implied_prob_2 / total_implied_prob)
                
                # Calculate guaranteed profit
                payout_1 = stake_1 * best_odds_1.price
                payout_2 = stake_2 * best_odds_2.price
                guaranteed_profit = min(payout_1, payout_2) - self.max_stake
                
                opportunities.append(ArbitrageOpportunity(
                    event=event,
                    bookmaker_1=best_odds_1.bookmaker,
                    outcome_1=best_odds_1.outcome,
                    odds_1=best_odds_1.price,
                    bookmaker_2=best_odds_2.bookmaker,
                    outcome_2=best_odds_2.outcome,
                    odds_2=best_odds_2.price,
                    profit_percentage=profit_percentage,
                    stake_1=stake_1,
                    stake_2=stake_2,
                    guaranteed_profit=guaranteed_profit,
                    market_type=market_type,
                    timestamp=datetime.now()
                ))
        
        return opportunities
    
    def _group_odds_by_outcome(self, odds: List[Odds]) -> Dict[str, List[Odds]]:
        """
        Group odds by outcome name
        
        Args:
            odds: List of Odds objects
        
        Returns:
            Dictionary mapping outcome names to lists of Odds
        """
        grouped = {}
        for odd in odds:
            outcome = odd.outcome
            if outcome not in grouped:
                grouped[outcome] = []
            grouped[outcome].append(odd)
        return grouped
    
    def format_opportunity(self, opp: ArbitrageOpportunity) -> str:
        """
        Format an arbitrage opportunity for display
        
        Args:
            opp: ArbitrageOpportunity object
        
        Returns:
            Formatted string representation
        """
        output = []
        output.append("=" * 80)
        output.append(f"ARBITRAGE OPPORTUNITY - {opp.profit_percentage:.2f}% Profit")
        output.append("=" * 80)
        output.append(f"Event: {opp.event.home_team} vs {opp.event.away_team}")
        output.append(f"Sport: {opp.event.sport}")
        output.append(f"Market: {opp.market_type}")
        output.append(f"Start Time: {opp.event.commence_time.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        output.append("BET 1:")
        output.append(f"  Bookmaker: {opp.bookmaker_1}")
        output.append(f"  Outcome: {opp.outcome_1}")
        output.append(f"  Odds: {opp.odds_1:.2f}")
        output.append(f"  Stake: ${opp.stake_1:.2f}")
        output.append(f"  Potential Return: ${opp.stake_1 * opp.odds_1:.2f}")
        output.append("")
        output.append("BET 2:")
        output.append(f"  Bookmaker: {opp.bookmaker_2}")
        output.append(f"  Outcome: {opp.outcome_2}")
        output.append(f"  Odds: {opp.odds_2:.2f}")
        output.append(f"  Stake: ${opp.stake_2:.2f}")
        output.append(f"  Potential Return: ${opp.stake_2 * opp.odds_2:.2f}")
        output.append("")
        output.append(f"Total Stake: ${opp.stake_1 + opp.stake_2:.2f}")
        output.append(f"Guaranteed Profit: ${opp.guaranteed_profit:.2f}")
        output.append(f"Profit Percentage: {opp.profit_percentage:.2f}%")
        output.append("=" * 80)
        
        return "\n".join(output)
