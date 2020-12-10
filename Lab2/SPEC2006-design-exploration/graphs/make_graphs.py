import matplotlib.pyplot as plt
import numpy as np

from sys import argv

CPI_INDEX = 0
DCACHE_MISSRATE_INDEX = 1
ICACHE_MISSRATE_INDEX = 2
L2_MISSRATE_INDEX = 3

def read_file(file):
    with open(file) as f:
        input_data = f.readlines()[1:]
        raw_data = [i.strip().split() for i in input_data]
        keys, raw_values = [j[0] for j in raw_data], [j[1:] for j in raw_data]
        
        values = [np.array([float(m) for m in k]) for k in raw_values]

        parsed_data = {k:v for k,v in zip(keys, values)}
        f.close()
    return parsed_data


def create_plot(title, x_label, data_dict, data_point_index, boundary_line, file_name):

    labels = ["64k L1i size", "4-way L1i assoc.", "8-way L1i assoc.", "32k L1d size", \
    "128k L1d size", "4-way L1d assoc.", "8-way L1d assoc.", "1MB L2 size", "4MB L2 size", \
    "2-way L2 assoc.", "4-way L2 assoc.", "32b line size", "128b line size", "256b line size",
    "256k L1d size", "Optimal CPI case"]
    
    figure, axes = plt.subplots()
    axes.axvline(boundary_line, color='r')
    axes.set_title(title)

    axes.spines["right"].set_visible(False)
    axes.spines["top"].set_visible(False)
    
    axes.set_xlabel(x_label)
    results = []
    for key in list(data_dict.keys())[1:]:
        results.append(data_dict[key][data_point_index])

    
    bar_positions = np.arange(len(results))
    rects = axes.barh(bar_positions, results)
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

if __name__ == "__main__":
    data = read_file(argv[1])
    create_plot(argv[2].capitalize() + " CPI", "CPI (lower is better)", data, CPI_INDEX, data[argv[2]][CPI_INDEX], argv[2] + "-cpi.png")
    create_plot(argv[2].capitalize() + " L1 data cache overall miss rate", "Miss rate (lower is better)",data, DCACHE_MISSRATE_INDEX, data[argv[2]][DCACHE_MISSRATE_INDEX], argv[2] + "-dcmiss.png")
    create_plot(argv[2].capitalize() + " L1 instr. cache overall miss rate", "Miss rate (lower is better)", data, ICACHE_MISSRATE_INDEX, data[argv[2]][ICACHE_MISSRATE_INDEX], argv[2] + "-icmiss.png")
    create_plot(argv[2].capitalize() + " L2 cache overall miss rate", "Miss rate (lower is better)", data, L2_MISSRATE_INDEX, data[argv[2]][L2_MISSRATE_INDEX], argv[2] + "-l2miss.png")
    