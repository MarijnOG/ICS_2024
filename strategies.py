from enum import Enum
from random import random, randint

# Lists all strategies

# Mees' strategies

# Marijn's strategies

# Rudimentary strategies
"""
Tit for that
Always cooperate
Always defect
Cooperate until defection, than always defect
"""


class BaseStrategy:

    def __init__(self): ...

    def decide(self, self_previous_actions, opponent_previous_actions):
        """
        Make a decision based previous actions of both players.

        Parameters:
        - opponent_previous_actions: List of opponent's previous actions

        Returns:
        - Next action: Cooperate (1) or Defect (0)
        """
        pass

    def split_last_string(self, string: str):
        return string[:-1], string[-1]

    def generate_lookup_table(self, strategy_code, lookback):
        lookup_table = {}
        table_size = 2 ** (lookback * 2)
        for i in range(table_size):
            key, result = self.split_last_string(strategy_code[i::table_size])
            lookup_table[key] = result

        return lookup_table


class StrategyAlwaysDefect(BaseStrategy):

    def __init__(self):
        pass

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Always defects (0)

        :param self_previous_actions: _description_
        :param opponent_previous_actions: _description_
        :return: _description_
        """
        return 0


class StrategyAlwaysCooperate(BaseStrategy):

    def __init__(self):
        pass

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Always cooperates (1)

        :param self_previous_actions: _description_
        :param opponent_previous_actions: _description_
        :return: _description_
        """
        return 1


class StrategyTitForThat(BaseStrategy):

    def __init__(self):
        pass

    def decide(self, self_previous_actions, opponent_previous_actions):
        """
        Tit for tat rules
        """
        if opponent_previous_actions:
            return opponent_previous_actions[-1]
        return 1


class StrategyGrudge(BaseStrategy):

    def __init__(self):
        self.grudge: bool = False

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Defect if opponent defected once, else cooperate."""
        if self.grudge:
            return 0
        if opponent_previous_actions[-1] == 0:
            self.grudge = True
            return 0
        return 1


class StrategyRandom(BaseStrategy):

    def decide(self, self_previous_actions, opponent_previous_actions):
        return randint(0, 1)


class StrategyAverage(BaseStrategy):

    def __init__(self, decision_sum: float = 0.51):
        self.decision_count: int = 0
        self.decision_sum = decision_sum

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Cooperate or defect based on the average decision by opponent.
        Starts out cooperating by default, but can be set as arg.
        """
        self.decision_count += 1
        if opponent_previous_actions[-1]:
            self.decision_sum += opponent_previous_actions[-1]

        return round(self.decision_sum/self.decision_count)


class StrategyGamblersTitForThat(BaseStrategy):

    def __init__(self, chance_to_invert: float = 0.2):
        self.chance = chance_to_invert

    def decide(self, self_previous_actions, opponent_previous_actions):
        """
        Tit for tat with added chance element. It makes the invverse decision 20%
        of the time by default.
        """
        if opponent_previous_actions:
            return opponent_previous_actions[-1] if random() > self.chance else abs(opponent_previous_actions[-1] - 1)
        
        return 1

