"""
This strategy can also be found in the main strategies.py file. 
This is here simply to demonstrate how one would generate the binary string
format from a written out strategy.
"""

from strategies import BaseStrategy


class StrategyDefectAfterTwoDefects(BaseStrategy):

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Defects after 2 consecutive defects by the opponent        """

        if len(opponent_previous_actions) >= 2:
            return 0 if opponent_previous_actions[-2:] == [0, 0] else 1
        return 1


strat = StrategyDefectAfterTwoDefects()
strat.strategy_code_table_from_strategy(2)
print(strat.strategy_code)
