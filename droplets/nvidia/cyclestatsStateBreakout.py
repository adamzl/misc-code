import os
import sys
import re
import csv

#assumed cyclcestatsCleanup was run first
#group(1) of pattern matches are transcribed as the data of each column
#common values for listOfRePatterns: ["pshader.*appHash=(0x[\dA-F`]+)", "compute.*appHash=(0x[\dA-F`]+)"]
def cyclestatsStateBreakout(inPath, listOfRePatterns=[], outPath=""):
    if outPath == "":
        outPath = "_" + inPath
    with open(inPath, 'r') as inFile:
        with open(outPath, 'w') as outFile:
            csvReader = csv.reader(inFile)
            for line in csvReader:
                if line[0] == "[#id]":
                    patternsInsertIndex = len(line) - 1
                    line = line[:patternsInsertIndex] + listOfRePatterns + line[patternsInsertIndex:]
                else:
                    patternMatches = []
                    for pattern in listOfRePatterns:
                        match = re.search(pattern, line[-1])
                        if match != None:
                            patternMatches.append(match.group(1))
                        else:
                            patternMatches.append("")
                    line = line[:patternsInsertIndex] + patternMatches + line[patternsInsertIndex:]
                _writeListToCsvFile(outFile, line)

def _writeListToCsvFile(outFile, line):
    for count, cell in enumerate(line):
        if count > 0:
            outFile.write(',')
        outFile.write(cell)
    outFile.write('\n')

predefinedRegexPatterns = [
    ("[tags, pshader, compute]", ["^([A-Z_<>]+)", "pshader.*appHash=(0x[\dA-F`]+)", "compute.*appHash=(0x[\dA-F`]+)"]),
    ("[tags, pshader.apphash, pshader.ucodehash, compute.apphash, compute.ucodehash]", ["^([A-Z_<>]+)", "pshader.*appHash=(0x[\dA-F`]+)", "pshader.*ucodeHash=(0x[\dA-F`]+)", "compute.*appHash=(0x[\dA-F`]+)", "compute.*ucodeHash=(0x[\dA-F`]+)"]),
]

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        inPathList = sys.argv[1:]
        print("[1/2] inPath:")
        for arg in sys.argv[1:]:
            print("\t{}".format(arg))
    else:
        inPath = input("[1/2] inPath: ")
        inPathList = [inPath]
    print("[2/2] regexPattern: enter a single expression or ^^#")
    for count,pattern in enumerate(predefinedRegexPatterns):
        print("\t{0}: {1}".format(count, pattern[0]))
    inputPatternText = input("      regexPattern: ")
    match = re.fullmatch("\^\^(\d+)", inputPatternText)
    if match:
        regexPattern = predefinedRegexPatterns[int(match.group(1))][1]
    else:
        regexPattern = [inputPatternText]
    for inPath in inPathList:
        cyclestatsStateBreakout(inPath, regexPattern)