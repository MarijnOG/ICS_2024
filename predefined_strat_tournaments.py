import gamemaster
from strategies import *
import numpy as np
import matplotlib.pyplot as plt

strats = [
    StrategyAlwaysDefect(),
    StrategyAlwaysCooperate(),
    StrategyTitForThat(),
    StrategyGrudge(),
    StrategyRandom(),
    StrategyAverage(),
    StrategyGamblersTitForThat(),
    StrategyInvertedTat(),
    StrategyDefectAfterTwoDefects(),
    StrategyFunnyLooking(),
    StrategySigmaTFT(),
]

keys_list = [
    "AlwaysDef",
    "AlwaysCoop",
    "TitForThat",
    "Grudge",
    "Random",
    "Average",
    "GamblersTFT",
    "InvertedTFT",
    "DAfter2D",
    "FunnyLooking",
    "SigmaTFT",
]

def experiment_table(payoff_table):
    model = gamemaster.Gamemaster(strats, mutation=False, experimental=False)
    model.amount_runs = 100
    model.payoff_table = payoff_table
    model.reset()

    TOTAL_STEPS = 5
    for i in range(TOTAL_STEPS):
        model.step()

    return model.tournament_results

def experiment_added_coop():

    inc_coop_strats = [StrategyHighlyCooperative_1(),
                       StrategyHighlyCooperative_2(),
                       StrategyHighlyCooperative_3()] + strats
    print(len(inc_coop_strats))

    model = gamemaster.Gamemaster(inc_coop_strats, mutation=False, experimental=False)
    model.amount_runs = 100
    model.reset()

    TOTAL_STEPS = 5
    for i in range(TOTAL_STEPS):
        model.step()

    return model.tournament_results, keys_list + ["HighlyCoop1", "HighlyCoop1", "HighlyCoop1"]

def experiment_added_defect():

    inc_defect_strats = [StrategyHighlyDefective_1(),
                         StrategyHighlyDefective_2(),
                         StrategyHighlyDefective_3()] + strats


    model = gamemaster.Gamemaster(inc_defect_strats, mutation=False, experimental=False)
    model.amount_runs = 100
    model.reset()

    TOTAL_STEPS = 5
    for i in range(TOTAL_STEPS):
        model.step()

    return model.tournament_results, keys_list + ["HighlyDef1", "HighlyDef2", "HighlyDef3"]

def barplot_tournament_results(results, keys, title):
    results = [r for r in results.values()]
    averages = np.mean(results, axis=1)
    plt.bar(keys, averages, color='firebrick')
    plt.xlabel("Strategy")
    plt.ylabel("Reward")
    plt.title(title)
    plt.show()



tables = [{(1, 1): 3, (1, 0): 5, (0, 1): 0, (0, 0): 1},
          {(1, 1): 3, (1, 0): 8, (0, 1): 0, (0, 0): 1}, 
          {(1, 1): 4, (1, 0): 5, (0, 1): 0, (0, 0): 0}]

regular_table = experiment_table(tables[0])
increased_defect_table = experiment_table(tables[1])
increased_coop_table = experiment_table(tables[2])

barplot_tournament_results(regular_table, keys_list, "Average Strategy Performance for Typical Reward Table")
barplot_tournament_results(increased_coop_table, keys_list, "Average Strategy Performance for Increased Cooperation Reward Table")
barplot_tournament_results(increased_defect_table, keys_list, "Average Strategy Performance for Defection Cooperation Reward Table")

increased_coop_strats = experiment_added_coop()
increased_defect_strats = experiment_added_defect()

barplot_tournament_results(*increased_coop_strats, "Average Strategy Performance with More Cooperation Strategies")
barplot_tournament_results(*increased_defect_strats, "Average Strategy Performance with More Defection Strategies")