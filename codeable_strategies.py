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
            print(opponent_previous_actions[-2:])
            return 0 if opponent_previous_actions[-1:] == [0] else 1
        return 1
    
strat = StrategyDefectAfterTwoDefects()
print(strat.lookup_table_from_strategy(2))

#TODO Fix dat previous actions niet als lijst maar als ['00'] <- dit worden doorgegeven door de method in strategies.