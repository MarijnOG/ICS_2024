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
        self.payoff_table = {(1, 1): 3, (1, 0): 5, (0, 1): 0, (0, 0): 0}

        self.amount_runs = n_runs + random_int

    def play_round(self):

        player1_reward = 0
        player2_reward = 0

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

            # Calculate rewards
            result_key = (self.player1_results[-1], self.player2_results[-1])
            player1_reward += self.payoff_table[result_key]
            player2_reward += self.payoff_table[result_key[::-1]]

        print(self.player1_results, "\n")
        print(self.player2_results, "\n")

        print(player1_reward, player2_reward)

    def reset(self):
        self.player1_results = []
        self.player2_results = []


if __name__ == "__main__":
    strategy1 = StrategyAlwaysCooperate()
    strategy2 = StrategyTitForThat()

    print(strategy2.lookup_table_from_strategy(2))
    # strategy1 = StrategyTitForThat()
    # strategy2 = StrategyRandom()
    game = Gamemaster(strategy1, strategy2, 100)
    game.play_round()
