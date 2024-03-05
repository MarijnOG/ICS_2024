from pyics import Model
import numpy as np
from strategies import *


class Gamemaster:

    def __init__(
        self,
        strategy1: BaseStrategy,
        strategy2: BaseStrategy,
        n_runs: int,
        random_int: int = 0,
    ):
        super().__init__()

        self.player1_results: list[int] = []
        self.player2_results: list[int] = []

        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.payoff_table = [(3, 3), (0, 5), (5, 0), (1, 1)]

        self.amount_runs = n_runs + random_int

    def play_round(self):

        for _ in range(self.amount_runs):
            self.player1_results.append(
                self.strategy1.decide(
                    self.player1_results, self.player2_results
                )
            )
            self.player2_results.append(
                self.strategy2.decide(
                    self.player2_results, self.player1_results
                )
            )

        print(self.player1_results)
        print()
        print(self.player2_results)

    def reset(self):
        self.player1_results = []
        self.player2_results = []


if __name__ == "__main__":
    # strategy1 = StrategyAlwaysCooperate()
    # strategy2 = StrategyAlwaysDefect()
    strategy1 = StrategyTitForThat()
    strategy2 = StrategyRandom()
    game = Gamemaster(strategy1, strategy2, 10)
    game.play_round()
