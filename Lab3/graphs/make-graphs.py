import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sys import argv

def make_energy_dframe(powers, runtimes, joules=False):
    benchmarkName = powers.caseName.str.rsplit('_').str[0].iloc[0]
    
    time_actual = runtimes

    power_actual = powers.sort_values("caseName")
    power_actual_defaultcase = power_actual.loc[power_actual["caseName"] == benchmarkName]
    power_actual_optcase = power_actual.loc[power_actual["caseName"] == benchmarkName + "_opt"]
    # remove problematic default and optimal case
    power_actual = power_actual.drop(power_actual_defaultcase.index[0]).drop(power_actual_optcase.index[0])

    # sort again by proper numerical order and reintroduce (default first, optimal last)
    power_actual = power_actual.reindex(index=power_actual.caseName.str.rsplit('_').str[-1].astype(int).sort_values().index)
    power_actual = pd.concat([power_actual_defaultcase, power_actual]).reset_index(drop=True)
    power_actual = power_actual.append(power_actual_optcase).reset_index(drop=True)

    if (joules):
        power_temp = power_actual.drop("caseName", axis=1).drop("area", axis=1).multiply(time_actual["sim_seconds"].values, axis="index")
        return power_actual[["caseName", "area"]].join(power_temp)
    else:
        return power_actual


if __name__ == "__main__":
    power = pd.read_csv(argv[1], sep=',')
    runtime = pd.read_csv(argv[2], sep='\t')

    print(make_energy_dframe(power, runtime, joules=True))
    print(make_energy_dframe(power, runtime, joules=False))
    print(runtime)