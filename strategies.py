from enum import Enum
from random import random, randint, choice

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

    def _int_to_binary_str(self, number, padding_length):
        """Converts an integer to binary in list format with length padding_length"""
        binary_string = bin(
            number)[2:]  # Convert to binary and remove the '0b' prefix
        return "0"*(padding_length - len(binary_string)) + binary_string

    def lookup_table_from_strategy(self, lookback: int):
        """Takes a compatible, possibly written out strategy and converts it to a table.
        This is implemented to reduce 'ugly' strategies in this file. Note that using this
        method with an incompatible strategy, such as one that uses chance, will produce
        undesirable and perhaps undeterministic behaviour."""
        lookup_table = {}

        for own_decision in range(2**lookback):
            for opponent_decision in range(2**lookback):
                own_str_bin = self._int_to_binary_str(own_decision, lookback)
                opp_str_bin = self._int_to_binary_str(
                    opponent_decision, lookback)

                new_decision = self.decide([own_str_bin], [opp_str_bin])
                new_decision = new_decision if type(
                    new_decision) == int else new_decision[-1]

                lookup_table[own_str_bin + opp_str_bin] = new_decision

        return lookup_table


class StrategyGenerated(BaseStrategy):

    def __init__(self, lookback):
        self.strategy_code = ''.join(choice(['0', '1']) for _ in range(2**(2*lookback)))
        self.lookback = lookback

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Uses the randomly generated table to decide the next step.

        :param self_previous_actions: _description_
        :param opponent_previous_actions: _description_
        :return: _description_
        """
        if len(self_previous_actions) < self.lookback: return 1

        index = self_previous_actions[-self.lookback:] + opponent_previous_actions[-self.lookback:]
        index = int(''.join(map(str, index)), 2)

        return int(self.strategy_code[index])

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
        if not opponent_previous_actions:
            return 1

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


class StrategyInvertedTat(BaseStrategy):

    def __init__(self, chance_to_invert: float = 0.2):
        self.chance = chance_to_invert

    def decide(self, self_previous_actions, opponent_previous_actions):
        """
        Tit for tat with added chance element. It makes the invverse decision 20%
        of the time by default.
        """
        if opponent_previous_actions:
            return abs(opponent_previous_actions[-1] - 1)

        return 1

from enum import Enum
from random import random, randint, choice

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

    # def split_last_string(self, string: str):
    #     return string[:-1], string[-1]

    # def generate_lookup_table(self, strategy_code, lookback):
    #     lookup_table = {}
    #     table_size = 2 ** (lookback * 2)
    #     for i in range(table_size):
    #         key, result = self.split_last_string(strategy_code[i::table_size])
    #         lookup_table[key] = result

    #     return lookup_table

    def _int_to_binary_str(self, number, padding_length):
        """Converts an integer to binary in list format with length padding_length"""
        binary_string = bin(number)[2:]  # Convert to binary and remove the '0b' prefix

        return "0"*(padding_length - len(binary_string)) + binary_string

    def lookup_table_from_strategy(self, lookback: int):
        """Takes a compatible, possibly written out strategy and converts it to a table.
        This is implemented to reduce 'ugly' strategies in this file. Note that using this
        method with an incompatible strategy, such as one that uses chance, will produce
        undesirable and perhaps undeterministic behaviour."""
        strategy_code = ""

        for own_decision in range(2**lookback):
            for opponent_decision in range(2**lookback):
                own_str_bin = self._int_to_binary_str(own_decision, lookback)
                opp_str_bin = self._int_to_binary_str(opponent_decision, lookback)

                new_decision = self.decide([own_str_bin], [opp_str_bin])
                new_decision = new_decision if type(
                    new_decision) == int else new_decision[-1]

                strategy_code += str(new_decision)

        return strategy_code


class StrategyGenerated(BaseStrategy):

    def __init__(self, lookback):
        self.strategy_code = ''.join(choice(['0', '1']) for _ in range(2**(2*lookback)))
        self.lookback = lookback

    def decide(self, self_previous_actions, opponent_previous_actions):
        """Uses the randomly generated table to decide the next step.

        :param self_previous_actions: _description_
        :param opponent_previous_actions: _description_
        :return: _description_
        """
        if len(self_previous_actions) < self.lookback: return 1

        index = self_previous_actions[-self.lookback:] + opponent_previous_actions[-self.lookback:]
        index = int(''.join(map(str, index)), 2)

        return int(self.strategy_code[index])

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


class StrategyInvertedTat(BaseStrategy):

    def __init__(self, chance_to_invert: float = 0.2):
        self.chance = chance_to_invert

    def decide(self, self_previous_actions, opponent_previous_actions):
        """
        Tit for tat with added chance element. It makes the invverse decision 20%
        of the time by default.
        """
        if opponent_previous_actions:
            return abs(opponent_previous_actions[-1] - 1)

        return 1
