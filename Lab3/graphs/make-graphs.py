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


def create_plot(title, x_label, dframe_core, dframe_l2, parameter_under_test, file_name, peak=False):

    labels = ["64k L1i size", "4-way L1i assoc.", "8-way L1i assoc.", "32k L1d size", \
    "128k L1d size", "4-way L1d assoc.", "8-way L1d assoc.", "1MB L2 size", "4MB L2 size", \
    "2-way L2 assoc.", "4-way L2 assoc.", "32b line size", "128b line size", "256b line size",
    "256k L1d size", "Optimal CPI case"]

    if (peak):
        dframe_l2["cpuPeakPower"] = np.zeros(len(dframe_l2))
    
    boundary_line = dframe_core[parameter_under_test][0].astype(float).round(decimals=4) + dframe_l2[parameter_under_test][0].astype(float).round(decimals=4)
    figure, axes = plt.subplots()
    axes.axvline(boundary_line, color='r')
    axes.set_title(title)

    axes.spines["right"].set_visible(False)
    axes.spines["top"].set_visible(False)
    
    axes.set_xlabel(x_label)
    results = dframe_core[parameter_under_test][1:].astype(float).round(decimals=4) + dframe_l2[parameter_under_test][1:].astype(float).round(decimals=4)
    
    bar_positions = np.arange(len(results))
    rects = axes.barh(bar_positions, results) #default case (red line) is the 0th element
    axes.set_yticks(bar_positions)
    axes.set_yticklabels(labels)

    bound = (max(results) - min(results)) * 0.05
    clamped_min_x = max(0, min(results) - bound)
    axes.set_xlim(clamped_min_x, max(results) + bound)

    for rect in rects:
        length = rect.get_width()
        axes.annotate('{}'.format(length),
                    xy=(length, rect.get_y() + (rect.get_height() / 2)),
                    va='center')
    
    plt.savefig(file_name, bbox_inches='tight')
    axes.clear()

def get_edp(core_joules, l2_joules, benchmarkname):
    result = pd.DataFrame()
    result["caseName"] = core_joules["caseName"] # same at both
    result["edp"] = core_joules["runtimeDynamicPower"] + l2_joules["runtimeDynamicPower"] + \
        core_joules["gateLeakage"] + l2_joules["gateLeakage"] + core_joules["subthresholdLeakage"] + \
        l2_joules["subthresholdLeakage"]

    result.to_csv(benchmarkname + "-edp.csv")
    


if __name__ == "__main__":
    power_core = pd.read_csv(argv[1], sep=',')
    power_l2 = pd.read_csv(argv[2], sep=',')
    runtime = pd.read_csv(argv[3], sep='\t')

    core_dframe_watts = make_energy_dframe(power_core, runtime, joules=False)
    l2_dframe_watts = make_energy_dframe(power_l2, runtime, joules=False)
    core_dframe_joules = make_energy_dframe(power_core, runtime, joules=True)
    l2_dframe_joules = make_energy_dframe(power_l2, runtime, joules=True)

    create_plot("Runtime dynamic power - " + argv[4].capitalize(), "Watts", core_dframe_watts, l2_dframe_watts, "runtimeDynamicPower", argv[4] + "-rdp.png")
    create_plot("Active processor area - " + argv[4].capitalize(), "mm^2", core_dframe_watts, l2_dframe_watts, "area", argv[4] + "-area.png")
    create_plot("Subthreshold Leakage Power - " + argv[4].capitalize(), "Watts", core_dframe_watts, l2_dframe_watts, "subthresholdLeakage", argv[4] + "-stlp.png")
    create_plot("Gate Leakage Power - " + argv[4].capitalize(), "Watts", core_dframe_watts, l2_dframe_watts, "gateLeakage", argv[4] + "-glp.png") 
    create_plot("Peak Power - " + argv[4].capitalize(), "Watts", core_dframe_watts, l2_dframe_watts, "cpuPeakPower", argv[4] + "-peak.png", True)
    get_edp(core_dframe_joules, l2_dframe_joules, argv[4])    
