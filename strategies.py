from enum import Enum

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
        from random import randint

        return randint(0, 1)
