from pyics import Model
from strategies import *
from typing import List, Tuple, Dict
from random import randint
import matplotlib.pyplot as plt
from copy import deepcopy

MUTATION = True

ALL_STRATS = [
        StrategyAlwaysDefect(),
        StrategyAlwaysCooperate(),
        StrategyTitForThat(),
        StrategyGrudge(),
        StrategyRandom(),
        StrategyAverage(),
        StrategyGamblersTitForThat(),
        StrategyInvertedTat(),
        StrategyFunnyLooking(),
        StrategySigmaTFT(),
        StrategyDefectAfterTwoDefects(),
    ]


class Gamemaster(Model):

    def __init__(
        self,
        strategies: List[BaseStrategy],
        mutation=False,
        experimental=False,
    ):
        Model.__init__(self)

        assert not (
            mutation and experimental
        ), "Can't be both mutation and experimental"

        self.payoff_table = {(1, 1): 3, (1, 0): 5, (0, 1): 0, (0, 0): 1}
        self.mutation = mutation
        self.base_strategies = strategies
        self.experimental = experimental

        self.make_param("random_int", False)
        self.make_param("amount_runs", 100, setter=self.set_amount_runs)

        if mutation or experimental:
            self.make_param("mutation_chance", 0.01)
            self.make_param(
                "amount_strategies", 20, setter=self.set_amount_strategies
            )
            self.make_param(
                "selection_fraction",
                0.2,
                setter=self.set_selection_fraction,
            )
            self.make_param(
                "crossover_fraction", 0.2, setter=self.set_selection_fraction
            )
            self.make_param("lookback", 4, setter=self.set_lookback)

        else:
            self.strategies = strategies

        self.reset()

    def set_lookback(self, value):
        return value if value > 0 else 1

    def set_selection_fraction(self, value):
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
        self.scores_per_round.append(list(all_scores))
        self.top_score_per_round.append(max(all_scores))

        if self.mutation:
            self.evolve(strategy_scores)

    def experimental_play_tournament(self):

        strategy_scores = {}

        for strategy1 in self.strategies:
            for strategy2 in self.strategies:
                if strategy1 == strategy2:
                    continue
                if isinstance(strategy1, StrategyGenerated) and isinstance(
                    strategy2, StrategyGenerated
                ):
                    continue

                if not isinstance(strategy1, StrategyGenerated):
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
            if not isinstance(strat, StrategyGenerated):
                continue

            if strat in self.tournament_results:
                self.tournament_results[strat].append(score)
            else:
                self.tournament_results[strat] = [score]

        all_scores = strategy_scores.values()
        self.scores_per_round.append(list(all_scores))
        self.top_score_per_round.append(max(all_scores))

        for strat in strategy_scores:
            print(strat.__class__.__name__, strategy_scores[strat])


        # remove base strategies
        strategy_scores = {
            k: v for k, v in strategy_scores.items() if isinstance(k, StrategyGenerated)
        }
        self.evolve(strategy_scores)
        # add them back in
        self.strategies = self.base_strategies + self.strategies

    def evolve(self, strategy_scores):

        # select the top self.selection_fraction strategies
        top_strategies = sorted(
            strategy_scores.items(), key=lambda x: x[1], reverse=True
        )[: int(self.amount_strategies * self.selection_fraction)]

        self.strategies = []

        for i in range(self.amount_strategies):
            self.strategies.append(
                deepcopy(top_strategies[i % len(top_strategies)][0])
            )

        # crossover but not with itself
        for i in range(0, len(self.strategies), 2):
            if i + 1 < len(self.strategies):
                self.strategies[i].crossover(
                    self.strategies[i + 1], self.crossover_fraction
                )

        # mutate
        for strategy in self.strategies:
            strategy.mutate(self.mutation_chance)

    def play_round(
        self, strategy1: BaseStrategy, strategy2: BaseStrategy
    ) -> Tuple[int, int]:

        player1_reward = 0
        player2_reward = 0

        player1_results = []
        player2_results = []

        for _ in range(self.amount_runs):
            tmp1 = player1_results.copy()
            player1_results.append(
                strategy1.decide(player1_results, player2_results)
            )
            player2_results.append(
                strategy2.decide(player2_results, tmp1)
            )

            # Calculate rewards
            result_key = (player1_results[-1], player2_results[-1])

            player1_reward += self.payoff_table[result_key]
            player2_reward += self.payoff_table[result_key[::-1]]

        return player1_reward, player2_reward

    def reset(self):
        self.tournament_results: Dict[BaseStrategy, List[int]] = {}
        self.top_score_per_round = []
        self.scores_per_round = []

        if self.mutation:
            self.strategies = [
                StrategyGenerated(self.lookback)
                for _ in range(self.amount_strategies)
            ]

        # if self.experimental then base strategies plus generated strategies
        if self.experimental:
            self.strategies = self.base_strategies + [
                StrategyGenerated(self.lookback)
                for _ in range(self.amount_strategies)
            ]



    def step(self):
        if self.experimental:
            self.experimental_play_tournament()
        else:
            self.play_tournament()

    def top_score_graph(self):
        plt.plot(self.top_score_per_round)
        plt.xlabel("Round")
        plt.ylabel("Top Score")

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
            plt.title(
                f"Top score. parameters: {self.amount_strategies=}, {self.selection_fraction=}, {self.crossover_fraction=}, {self.mutation_chance=}"
            )

        if not table:
            print("No data to display.")
            plt.text(0.5, 0.5, "No data to display", ha="center")
            return

        if self.mutation:
            self.top_score_graph()
            return

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


def experiment_full_genetic():
    model = Gamemaster([], mutation=True)
    model.amount_runs = 100
    model.amount_strategies = 60
    model.selection_fraction = 0.2
    model.crossover_fraction = 0.4
    model.mutation_chance = 0.05
    model.lookback = 6
    model.reset()

    TOTAL_STEPS = 20
    for i in range(TOTAL_STEPS):
        model.step()
        print(f"Step {i+1}/{TOTAL_STEPS}")

    with open("full_genetic.txt", "w") as file:
        file.write(f"amount_strategies: {model.amount_strategies}\n")
        file.write(f"selection_fraction: {model.selection_fraction}\n")
        file.write(f"crossover_fraction: {model.crossover_fraction}\n")
        file.write(f"mutation_chance: {model.mutation_chance}\n")
        file.write(f"lookback: {model.lookback}\n")
        file.write(f"amount_runs: {model.amount_runs}\n")
        file.write(f"top_score_per_round: {model.top_score_per_round}\n")
        file.write(f"scores_per_round: {model.scores_per_round}\n")
        file.write(f"total_steps: {TOTAL_STEPS}\n\n")

        # genetic parameters
        for strategy in model.strategies:
            file.write(
                f"{strategy.__class__.__name__}: {strategy.strategy_code}\n"
            )

def experiment_mixed():
    model = Gamemaster(ALL_STRATS, mutation=False, experimental=True)
    model.amount_runs = 100
    model.amount_strategies = 20
    model.selection_fraction = 0.2
    model.crossover_fraction = 0.4
    model.mutation_chance = 0.05
    model.lookback = 6
    model.reset()

    TOTAL_STEPS = 20
    for i in range(TOTAL_STEPS):
        model.step()
        print(f"Step {i+1}/{TOTAL_STEPS}")

    with open("experiment_mixed.txt", "w") as file:
        file.write(f"amount_strategies: {model.amount_strategies}\n")
        file.write(f"selection_fraction: {model.selection_fraction}\n")
        file.write(f"crossover_fraction: {model.crossover_fraction}\n")
        file.write(f"mutation_chance: {model.mutation_chance}\n")
        file.write(f"lookback: {model.lookback}\n")
        file.write(f"amount_runs: {model.amount_runs}\n")
        file.write(f"top_score_per_round: {model.top_score_per_round}\n")
        file.write(f"scores_per_round: {model.scores_per_round}\n")
        file.write(f"total_steps: {TOTAL_STEPS}\n\n")

        # genetic parameters

        for strategy in model.strategies:
            if isinstance(strategy, StrategyGenerated):
                file.write(
                    f"{strategy.__class__.__name__}: {strategy.strategy_code}\n"
                )
            else:
                file.write(f"{strategy.__class__.__name__}\n")


def main():
    experiment_mixed()
    return



    model = Gamemaster(strats, mutation=False, experimental=True)
    from pyics import GUI

    gui = GUI(model)
    gui.start()


if __name__ == "__main__":
    main()
