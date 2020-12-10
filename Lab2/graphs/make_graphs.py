import matplotlib.pyplot as plt
import numpy as np

from sys import argv

CPI_INDEX = 0
DCACHE_MISSRATE = 1
ICACHE_MISSRATE = 2
L2_MISSRATE = 3

def read_file(file):
    with open(file) as f:
        input_data = f.readlines()[1:]
        raw_data = [i.strip().split() for i in input_data]
        keys, raw_values = [j[0] for j in raw_data], [j[1:] for j in raw_data]
        
        values = [np.array([float(m) for m in k]) for k in raw_values]

        parsed_data = {k:v for k,v in zip(keys, values)}
        f.close()
    return parsed_data


def create_plot(title, x_label, data_dict, data_point_index, boundary_line, lower_xlim, upper_xlim, file_name):

    labels = ["64k L1i size", "4-way L1i assoc.", "8-way L1i assoc.", "32k L1d size", \
    "128k L1d size", "4-way L1d assoc.", "8-way L1d assoc.", "1MB L2 size", "4MB L2 size", \
    "2-way L2 assoc.", "4-way L2 assoc.", "32b line size", "128b line size", "256b line size",
    "256k L1d size"]
    
    figure, axes = plt.subplots()
    axes.axvline(boundary_line, color='r')
    axes.set_title(title)

    axes.spines["right"].set_visible(False)
    axes.spines["top"].set_visible(False)
    
    axes.set_xlim(lower_xlim, upper_xlim)
    axes.set_xlabel(x_label)
    results = []
    for key in list(data_dict.keys())[1:]:
        results.append(data_dict[key][data_point_index])

    
    bar_positions = np.arange(len(results))
    rects = axes.barh(bar_positions, results)
    axes.set_yticks(bar_positions)
    axes.set_yticklabels(labels)

    for rect in rects:
        length = rect.get_width()
        axes.annotate('{}'.format(length),
                    xy=(length + 0.002, rect.get_y() + (rect.get_height() / 2)),
                    va='center')

    plt.savefig(file_name, bbox_inches='tight')
    axes.clear()

if __name__ == "__main__":
    t = read_file(argv[1])
    create_plot("lol", "CPI (lower is better)", t, CPI_INDEX, t["spechmmer"][CPI_INDEX], 1, 1.4, "test1.png")
    create_plot("lol", "CPI (lower is better)", t, CPI_INDEX, t["spechmmer"][CPI_INDEX], 1, 1.4, "test2.png")
    