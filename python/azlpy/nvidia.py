import os
import glob
import csv
import re

def cyclestatsCleanup(inPath, outPath=""):
    if outPath == "":
        outPath = inPath[:-4] + ".csv"
    with open(inPath, 'r') as inFile:
        with open(outPath, 'w') as outFile:
            csvReader = csv.reader(inFile, dialect='excel-tab')
            #throw away header components and write of column headers
            for line in csvReader:
                match = re.match('\[#id\]', line[0])
                if not match:
                    continue
                _writeListToCsvFile(outFile, line)
                break
            #transcribe rows of data, PRESUMED FIVE COLUMNS
            for line in csvReader:
                match = re.match(r'\d+', line[0])
                if not match:
                    break
                _writeListToCsvFile(outFile, line)

#assumed cyclcestatsCleanup was run first
#group(1) of pattern matches are transcribed as the data of each column
#common values for listOfRePatterns: ["pshader.*appHash=(0x[\dA-F`]+)", "compute.*appHash=(0x[\dA-F`]+)"]
def cyclestatsStateBreakout(inPath, listOfRePatterns=[], outPath=""):
    if outPath == "":
        outPath = os.path.join(os.path.split(inPath)[0], "_" + os.path.split(inPath)[1])
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