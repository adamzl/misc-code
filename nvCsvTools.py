import os
import glob
import csv
import re

def cyclestatsCleanup(inPath, outDir=""):
    if outDir == "":
        outDir = inPath[:-4] + ".csv"
    else:
        nameNoExt = os.path.split(os.path.splitext(inPath)[0])[1]
        outDir = os.path.join(outDir, nameNoExt) + ".csv"
    with open(inPath, 'r') as inFile:
        with open(outDir, 'w') as outFile:
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
def cyclestatsStateBreakout(inPath, outDir="", listOfRePatterns=[]):
    if outDir == "":
        outDir = os.path.joint(os.path.split(inPath)[0], "_output_cyclestatsStateBreakout")
    with open(inPath, 'r') as inFile:
        outPath = os.path.join(outDir, os.path.split(inPath)[1])
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

# if __name__ == '__main__':
#     cyclestatsStateBreakout(r'C:\data\binary_const_folding\sniper elite\adam_cyclestats.csv', r'C:\data\binary_const_folding\sniper elite\adam_cyclestats_breakout.csv', ['pshader.*appHash=(0x[\dA-F`]+)'])