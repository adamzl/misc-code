import os
import sys
import re
import csv

#assumed cyclcestatsCleanup was run first
#group(1) of pattern matches are transcribed as the data of each column
#common values for listOfRePatterns: ["pshader.*appHash=(0x[\dA-F`]+)", "compute.*appHash=(0x[\dA-F`]+)"]
def cyclestatsStateBreakout(inPath, listOfRePatterns=[], outDir=""):
    if outDir == "":
        outDir = os.path.split(inPath)[0]
    with open(inPath, 'r') as inFile:
        outPath = os.path.join(outDir, "_" + os.path.split(inPath)[1])
        with open(outPath, 'w') as outFile:
            csvReader = csv.reader(inFile)
            for line in csvReader:
                if line[0] == "[#id]":
                    for pattern in listOfRePatterns:
                        line.append(pattern)
                else:
                    stateString = line[-1]
                    for pattern in listOfRePatterns:
                        match = re.search(pattern, stateString)
                        if match != None:
                            line.append(match.group(1))
                _writeListToCsvFile(outFile, line)

def _writeListToCsvFile(outFile, line):
    for count, cell in enumerate(line):
        if count > 0:
            outFile.write(',')
        outFile.write(cell)
    outFile.write('\n')

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        inPathList = sys.argv[1:]
        print("[1/2] inPath:")
        for arg in sys.argv[1:]:
            print("\t{}".format(arg))
    else:
        inPath = input("[1/2] inPath: ")
        inPathList = [inPath] 
    regexPattern = input("[2/2] regexPattern: ")
    for inPath in inPathList:
        cyclestatsStateBreakout(inPath, [regexPattern])