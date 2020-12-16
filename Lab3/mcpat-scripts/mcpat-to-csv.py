from sys import argv
from csv import DictWriter
from os import listdir, path

def find_sections(fileLines: list):
    coreStartIndex, coreEndIndex, L2StartIndex, L2EndIndex = 0, 0, 0, 0
    peakPowerIndex = 0
    
    for lineNumber in range(0, len(fileLines)):
        if "Core:" in fileLines[lineNumber]:
            coreStartIndex = lineNumber
        elif "Instruction Fetch Unit" in fileLines[lineNumber]:
            coreEndIndex = lineNumber
        elif "L2" in fileLines[lineNumber]:
            L2StartIndex = lineNumber
        elif "Memory Controller:" in fileLines[lineNumber]:
            L2EndIndex = lineNumber
        elif "Peak Power" in fileLines[lineNumber]:
            peakPowerIndex = lineNumber

    return (coreStartIndex, coreEndIndex, L2StartIndex, L2EndIndex, peakPowerIndex)


def parse_file(file):
    with open(file) as f:
        lines = f.readlines()

    fileName = path.splitext(path.splitext(path.basename(file))[0])[0]
    section_indices = find_sections(lines)

    rawCoreSection = list(map(lambda l: l.strip(), lines[section_indices[0]:section_indices[1]]))
    rawL2Section = list(map(lambda l: l.strip(), lines[section_indices[2]:section_indices[3]]))

    coreSection = list(filter(lambda x: len(x) != 0, rawCoreSection))[1:]
    l2Section = list(filter(lambda x: len(x) != 0, rawL2Section))[1:]

    cleanResults = lambda z: float(z.split('=')[1].split()[0])

    core = {
        "caseName": fileName,
        "area": cleanResults(coreSection[0]),
        "peakDynamicPower": cleanResults(coreSection[1]),
        "runtimeDynamicPower": cleanResults(coreSection[5]),
        "subthresholdLeakage": cleanResults(coreSection[2]),
        "gateLeakage": cleanResults(coreSection[4]),
        "cpuPeakPower": cleanResults(lines[section_indices[4]])
    }
    l2 = {
        "caseName": fileName,
        "area": cleanResults(l2Section[0]),
        "peakDynamicPower": cleanResults(l2Section[1]),
        "runtimeDynamicPower": cleanResults(l2Section[5]),
        "subthresholdLeakage": cleanResults(l2Section[2]),
        "gateLeakage": cleanResults(l2Section[4])
    }
    
    return core, l2


if __name__ == "__main__":
    contents = [j for j in listdir(argv[1]) if "time" not in j]
    coreFields = ["caseName", "area", "peakDynamicPower", "runtimeDynamicPower", "subthresholdLeakage", "gateLeakage","cpuPeakPower"]
    l2Fields = ["caseName", "area", "peakDynamicPower", "runtimeDynamicPower", "subthresholdLeakage", "gateLeakage"]
        
    with open("results_core.csv", "w", newline='') as corecsv, \
        open("results_l2.csv", 'w', newline='') as l2csv:
            coreWriter = DictWriter(corecsv, fieldnames=coreFields)
            l2Writer = DictWriter(l2csv, fieldnames=l2Fields)

            coreWriter.writeheader()
            l2Writer.writeheader()

            for file in contents:
                core, l2 = parse_file(argv[1] + file)
                coreWriter.writerow(core)
                l2Writer.writerow(l2)

            corecsv.close()
            l2csv.close()