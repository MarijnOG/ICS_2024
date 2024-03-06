import gamemaster
from strategies import *
import numpy as np

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

model = gamemaster.Gamemaster(strats, mutation=False, experimental=False)
model.play_tournament()