from enum import Enum
from random import random, randint, choice
from numpy import exp

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

    def __init__(self):
        self.strategy_code = ""

    def decide(self, self_previous_actions, opponent_previous_actions):
        """
        Make a decision based previous actions of both players.

        Parameters:
        - opponent_previous_actions: List of opponent's previous actions

        Returns:
        - Next action: Cooperate (1) or Defect (0)
        """
        pass

    def _int_to_binary_str(self, number, padding_length):
        """Converts an integer to binary in list format with length padding_length"""
        binary_string = bin(
            number)[2:]  # Convert to binary and remove the '0b' prefix
        return "0"*(padding_length - len(binary_string)) + binary_string

    def strategy_code_from_strategy(self, lookback: int):
        """Takes a compatible, possibly written out strategy and converts it to a strategy code.
        This is implemented to reduce 'ugly' strategies in this file, as well as making it possible
        to have manually defined strategies as mutable objects. Note that using this
        method with an incompatible strategy, such as one that uses chance, will produce
        undesirable and perhaps undeterministic behaviour."""
        strategy_code = ""

        for own_decision in range(2**lookback):
            for opponent_decision in range(2**lookback):
                own_str_bin = self._int_to_binary_str(own_decision, lookback)
                opp_str_bin = self._int_to_binary_str(
                    opponent_decision, lookback)

                new_decision = self.decide([int(c) for c in own_str_bin],
                                           [int(c) for c in opp_str_bin])
                new_decision = new_decision if type(
                    new_decision) == int else new_decision[-1]

                strategy_code += str(new_decision)

        self.strategy_code = strategy_code
        return strategy_code


class CodeBasedStrategy(BaseStrategy):
    def decide(self, self_previous_actions, opponent_previous_actions):
        """Uses the randomly generated table to decide the next step.

        :param self_previous_actions: _description_
        :param opponent_previous_actions: _description_
        :return: _description_
        """
        if len(self_previous_actions) < self.lookback:
            return 1

        index = self_previous_actions[-self.lookback:] + \
            opponent_previous_actions[-self.lookback:]
        index = int(''.join(map(str, index)), 2)

        return int(self.strategy_code[index])

    def mutate(self, chance):
        if not self.strategy_code:
            raise AttributeError("Instance must have stratey_code attribute.")

        for i in range(len(self.strategy_code)):
            if random() <= chance:
                bit = self.strategy_code[i]
                flipped_bit = '0' if bit == '1' else '1'
                self.strategy_code = (
                    self.strategy_code[:i] + flipped_bit +
                    self.strategy_code[i + 1:]
                )

    def crossover(self, other_strategy, chance):
        if not isinstance(other_strategy, BaseStrategy):
            raise ValueError(
                "Input must be an instance of BaseStrategy or its subclass.")

        if not self.strategy_code or not other_strategy.strategy_code:
            raise AttributeError(
                "Input and class instance must have stratey_code attribute.")

        list_self = list(self.strategy_code)
        list_other = list(other_strategy.strategy_code)

        for i, _ in enumerate(list_self):
            if random() <= chance:
                list_self[i], list_other[i] = list_other[i], list_self[i]

        self.strategy_code = "".join(list_self)
        other_strategy.strategy_code = "".join(list_other)


class StrategyGenerated(CodeBasedStrategy):
    """Generates a strategy code for itself"""

    def __init__(self, lookback):
        self.strategy_code = ''.join(
            choice(['0', '1']) for _ in range(2**(2*lookback)))
        self.lookback = lookback


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
        if not opponent_previous_actions: 
            return 1
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
        Tit for tat with added chance element. It makes the inverse decision 20%
        of the time by default.
        """
        if opponent_previous_actions:
            return abs(opponent_previous_actions[-1] - 1)

        return 1


class StrategySigmaTFT(BaseStrategy):

    def __init__(self):
        # -1 for defect, +1 for cooperate
        self.defect_coop_count = 0

    def sigmoid(self, z):
        return 1/(1 + exp(-z))

    def decide(self, self_previous_actions, opponent_previous_actions):
        """TFT except when there is a large discrepancy in cooperation and defection"""
        if not opponent_previous_actions:
            return 1

        self.defect_coop_count += 1 if opponent_previous_actions[-1] == 1 else -1

        # DON'T tit for that
        if abs(self.sigmoid(self.defect_coop_count)**2) > 0.75:
            return int(not opponent_previous_actions[-1])

        return opponent_previous_actions[-1]

# Note that this strategy is in binary string format. For the written out version,
# see codeable_strategies.py


class StrategyDefectAfterTwoDefects(CodeBasedStrategy):
    """Defects after 2 consecutive defects by the opponent"""

    def __init__(self):
        self.strategy_code = "0111011101110111"
        self.lookback = 2


class StrategyFunnyLooking(CodeBasedStrategy):
    """Interesting looking code. Added to introduce a bit more """

    def __init__(self):
        self.strategy_code = "1110001110001110"
        self.lookback = 2

class StrategyHighlyCooperative_1(CodeBasedStrategy):
    """Cooperates except for very specific sequences"""

    def __init__(self):
        self.strategy_code = "1111011111111110"
        self.lookback = 2

class StrategyHighlyCooperative_2(CodeBasedStrategy):
    """Cooperates except for very specific sequences"""

    def __init__(self):
        self.strategy_code = "0111101110111111"
        self.lookback = 2

class StrategyHighlyCooperative_3(CodeBasedStrategy):
    """Cooperates except for very specific sequences"""

    def __init__(self):
        self.strategy_code = "1011111111011111"
        self.lookback = 2

class StrategyHighlyDefective_1(CodeBasedStrategy):
    """Defects except for very specific sequences"""

    def __init__(self):
        self.strategy_code = "0001000000100000"
        self.lookback = 2

class StrategyHighlyDefective_2(CodeBasedStrategy):
    """Defects except for very specific sequences"""

    def __init__(self):
        self.strategy_code = "1001000000000010"
        self.lookback = 2

class StrategyHighlyDefective_3(CodeBasedStrategy):
    """Defects except for very specific sequences"""

    def __init__(self):
        self.strategy_code = "0000000100000100"
        self.lookback = 2