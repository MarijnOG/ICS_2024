from pyics import Model
from strategies import *
from typing import List, Tuple, Dict
from random import randint
import matplotlib.pyplot as plt
from copy import deepcopy

MUTATION = True


class Gamemaster(Model):

    def __init__(
        self,
        strategies: List[BaseStrategy],
        mutation=False,
    ):
        Model.__init__(self)

        self.tournament_results: Dict[BaseStrategy, List[int]] = {}
        self.payoff_table = {(1, 1): 3, (1, 0): 5, (0, 1): 0, (0, 0): 1}
        self.top_score_per_round = []
        self.mutation = mutation

        self.make_param("random_int", False)
        self.make_param("amount_runs", 100, setter=self.set_amount_runs)

        if mutation:
            self.make_param("mutation_percentage", 0.1)
            self.make_param(
                "amount_strategies", 100, setter=self.set_amount_strategies
            )
            self.make_param(
                "selection_percentage",
                0.1,
                setter=self.set_selection_percentage,
            )
            self.make_param("lookback", 1, setter=self.set_lookback)
            self.strategies = [
                StrategyGenerated(self.lookback)
                for _ in range(self.amount_strategies)
            ]
        else:
            self.strategies = strategies

    def set_lookback(self, value):
        return value if value > 0 else 1

    def set_selection_percentage(self, value):
        return max(0, min(1, value))

    def set_amount_strategies(self, value):
        return value if value > 0 else 1

    def set_amount_runs(self, value):
        value = value if value > 0 else 1
        random_range = 0
        if self.random_int:
            # 10 percent of amount runs
            random_range = int(self.amount_runs * 0.1)
            random_range = randint(0, random_range)
        return value + random_range

    def play_tournament(self):

        strategy_scores = {}

        for strategy1 in self.strategies:
            for strategy2 in self.strategies:
                if strategy1 == strategy2:
                    continue

                if strategy1 not in strategy_scores:
                    strategy_scores[strategy1] = self.play_round(
                        strategy1, strategy2
                    )[0]
                else:
                    strategy_scores[strategy1] += self.play_round(
                        strategy1, strategy2
                    )[0]

        for strat, score in strategy_scores.items():
            if strat in self.tournament_results:
                self.tournament_results[strat].append(score)
            else:
                self.tournament_results[strat] = [score]

        all_scores = strategy_scores.values()
        self.top_score_per_round.append(max(all_scores))
        print(self.top_score_per_round)

        if self.mutation:
            self.evolve(strategy_scores)

    def evolve(self, strategy_scores):

        # select the top self.selection_percentage strategies
        top_strategies = sorted(
            strategy_scores.items(), key=lambda x: x[1], reverse=True
        )[: int(self.amount_strategies * self.selection_percentage)]

        self.strategies = []

        for i in range(self.amount_strategies):
            self.strategies.append(
                deepcopy(top_strategies[i % len(top_strategies)][0])
            )

        # crossover but not with itself
        for i in range(0, len(self.strategies), 2):
            if i + 1 < len(self.strategies):
                self.strategies[i].crossover(
                    self.strategies[i + 1], self.mutation_percentage
                )
                



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
        self.tournament_results = {}
        self.play_tournament()

    def step(self):
        self.play_tournament()

    def top_score_graph(self):
        plt.plot(self.top_score_per_round)
        plt.xlabel("Round")
        plt.ylabel("Top Score")
        plt.title("Top Score per Round")

    def draw(self):
        plt.cla()
        sorted_strategies = sorted(
            self.tournament_results.items(),
            key=lambda x: sum(x[1]),
            reverse=True,
        )

        table = []
        for strategy, scores in sorted_strategies:
            table.append([strategy.__class__.__name__, sum(scores), scores[-1]])

        if not table:
            print("No data to display.")
            plt.text(0.5, 0.5, "No data to display", ha="center")
        else:

            if self.mutation:
                self.top_score_graph()
            else:

                # sub plot 1 of 2
                plt.subplot(2, 1, 1)
                plt.axis("off")
                plt.table(
                    cellText=table,
                    colLabels=["Strategy", "Total Score", "Last Score"],
                    loc="center",
                )
                plt.title("Tournament Results")
                # sub plot 2 of 2
                plt.subplot(2, 1, 2)
                self.top_score_graph()

    def reset(self):
        self.tournament_results = {}


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

    model = Gamemaster(strats, mutation=MUTATION)
    from pyics import GUI

    gui = GUI(model)
    gui.start()
