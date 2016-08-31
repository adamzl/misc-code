import os
import glob
import csv
import re

def cyclestatsCleanup(inPath):
    outPath = inPath[:-3] + 'csv'
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
def cyclestatsStateBreakout(inPath, outPath, listOfRePatterns):
    with open(inPath, 'r') as inFile:
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