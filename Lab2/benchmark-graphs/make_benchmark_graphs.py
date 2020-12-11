import matplotlib.pyplot as plt
import numpy as np

from sys import argv

SIM_TIME_INDEX = 0
CPI_INDEX = 1
DCACHE_MISSRATE_INDEX = 2
ICACHE_MISSRATE_INDEX = 3
L2_MISSRATE_INDEX = 4

def read_file(file):
    with open(file) as f:
        input_data = f.readlines()[1:]
        raw_data = [i.strip().split() for i in input_data]
        keys, raw_values = [j[0] for j in raw_data], [j[1:] for j in raw_data]
        
        values = [np.array([float(m) for m in k]) for k in raw_values]

        parsed_data = {k:v for k,v in zip(keys, values)}
        f.close()
    return parsed_data


def create_plot(title, y_label, data_dict, data_point_index, file_name):

    labels = ["specbzip", "speclibm", "spechmmer", "specmcf", "specsjeng"]
    
    figure, axes = plt.subplots()
    axes.set_title(title)
    axes.set_ylabel(y_label)
    results = []
    for key in list(data_dict.keys()):
        results.append(data_dict[key][data_point_index])
    
    bar_positions = np.arange(len(results))
    rects = axes.bar(bar_positions, results)
    axes.set_xticks(bar_positions)
    axes.set_xticklabels(labels)

    bound = (max(results) - min(results)) * 0.10
    clamped_min_y = max(0, min(results) - bound)
    axes.set_ylim(clamped_min_y, max(results) + bound)

    for rect in rects:
        height = rect.get_height()
        axes.annotate('{}'.format(height),
                    xy=(rect.get_x() + (rect.get_width() / 2), height + (height * 0.01)),
                    ha='center', va='bottom')

    plt.savefig(file_name, bbox_inches='tight')
    axes.clear()

if __name__ == "__main__":
    data = read_file(argv[1])
    create_plot("run time - " + argv[2], "Seconds", data, SIM_TIME_INDEX, argv[2] + "-simtime.png")
    create_plot("CPI - " + argv[2], "CPI", data, CPI_INDEX, argv[2] + "-cpi.png")
    create_plot("L1 data cache miss rate - " + argv[2], "percent", data, DCACHE_MISSRATE_INDEX, argv[2] + "-dcmiss.png")
    create_plot("L1 instruction cache miss rate - " + argv[2], "percent", data, ICACHE_MISSRATE_INDEX, argv[2] + "-icmiss.png")
    create_plot("L2 cache miss rate - " + argv[2], "percent", data, L2_MISSRATE_INDEX, argv[2] + "-l2miss.png")