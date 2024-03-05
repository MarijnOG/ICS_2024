import numpy as np


COOPERATE = 1
DEFECT = 0

class PrisonersDilemmaStrategy:
    def __init__(self, name, decision_table_integer):
        self.name = name
        self.previous_actions = []
        self.decision_table = 0

    def set_decision_table(self, table_int):
        """
        Takes the decision_table from the input and converts it to the proper syntax.
        """
        


    def decide(self, opponent_previous_actions):
        """
        Make a decision based previous actions of both players.

        Parameters:
        - opponent_previous_actions: List of opponent's previous actions

        Returns:
        - Next action: Cooperate (1) or Defect (0)
        """
        pass


# Example of strategy format (tit for that):
# +-------------------------------+---+---+---+---+
# | Opponent previous decision(s) | 1 | 1 | 0 | 0 |
# | Player prvious decision(s)    | 0 | 1 | 0 | 1 |
# +-------------------------------+---+---+---+---+
# | Player next decision          | 1 | 1 | 0 | 0 |
# +-------------------------------+---+---+---+---+
#
# Input as joined integer: 1100 0101 1100

# Tit for that:
tit_for_tat = "110001011100"
# tit_for_that_dic = {'10': 1, '11': 1, '00': 0, '01': 0}


def split_last_string(string: str):
    return string[:-1], string[-1]


def generate_lookup_table(strategy_code, lookback):
    lookup_table = {}
    table_size = 2 ** (lookback*2)
    for i in range(table_size):
        key, result = split_last_string(strategy_code[i::table_size])
        lookup_table[key] = result

    return lookup_table




lb = 1
tit_for_that_dic = generate_lookup_table(tit_for_tat, lb)

print(tit_for_that_dic)
# Now tit_for_that_dic is {('1', '0'): 1, ('1', '1'): 1, ('0', '0'): 0, ('0', '1'): 0}


# For a full table:
# For lookback 1, we require 2^(2*1) sets of 2^1 cells + 2^2 result cells. For 2 lookback, 
# we require 2^(2*2) sets of 2^2 cells + 2^4 result cells. For n lookback, we require 2^(2n) sets of 2^n cells + 2^(2n) cells.