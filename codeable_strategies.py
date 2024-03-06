"""
This file is strictly to write out strategies better captured with our binary string format.
"""

from strategies import *

class StrategyDefectAfterTwoDefects(BaseStrategy):
    
    def __init__(self):
        pass

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Defects after 2 consecutive defects by the opponent

        :param self_previous_actions: _description_
        :param opponent_previous_actions: _description_
        :return: _description_
        """

        if len(opponent_previous_actions) >= 2:
            return 0 if opponent_previous_actions[-2:] == [0, 0] else 1
        return 1
    
strat = StrategyDefectAfterTwoDefects()
strat.strategy_code_table_from_strategy(2)
strat2 = StrategyGenerated(2)

print(strat.strategy_code)
print(strat2.strategy_code, "\n")

strat2.mutate(1)

print(strat.strategy_code)
print(strat2.strategy_code)
#TODO Fix dat previous actions niet als lijst maar als ['00'] <- dit worden doorgegeven door de method in strategies.