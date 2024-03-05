from pyics import Model
import numpy as np
from strategies import *
from typing import List, Tuple


class Gamemaster:

    def __init__(
        self,
        strategies: List[BaseStrategy],
        n_runs: int,
        random_int: int = 0,
    ):
        super().__init__()

        self.strategies = strategies
        self.tournament_results = []
        self.payoff_table = {(1, 1): 3, (1, 0): 5, (0, 1): 0, (0, 0): 1}

        self.amount_runs = n_runs + random_int

    def play_tournament(self):

        strategy_scores = {}

        for strategy1 in self.strategies:
            for strategy2 in self.strategies:
                if strategy1 == strategy2:
                    print("self")
                    continue

                if strategy1 not in strategy_scores:
                    strategy_scores[strategy1] = self.play_round(
                        strategy1, strategy2
                    )[0]
                else:
                    strategy_scores[strategy1] += self.play_round(
                        strategy1, strategy2
                    )[0]

        for key, value in strategy_scores.items():
            key: BaseStrategy
            print(f"{key.__class__.__name__}: {value}")

    def play_round(
        self, strategy1: BaseStrategy, strategy2: BaseStrategy
    ) -> Tuple[int, int]:

        player1_reward = 0
        player2_reward = 0

        player1_results = []
        player2_results = []

        for _ in range(self.amount_runs):
            player1_results.append(
                strategy1.decide(player1_results, player2_results)
            )
            player2_results.append(
                strategy2.decide(player2_results, player1_results)
            )

            # Calculate rewards
            result_key = (player1_results[-1], player2_results[-1])
            player1_reward += self.payoff_table[result_key]
            player2_reward += self.payoff_table[result_key[::-1]]

        return player1_reward, player2_reward

    def reset(self):
        self.player1_results = []
        self.player2_results = []


if __name__ == "__main__":
    strats = [
        StrategyAlwaysDefect(),
        StrategyAlwaysCooperate(),
        StrategyTitForThat(),
        StrategyGrudge(),
        StrategyRandom(),
        StrategyAverage(),
        StrategyGamblersTitForThat(),
        StrategyInvertedTat(),
    ]

    game = Gamemaster(strats, 100)
    game.play_tournament()
