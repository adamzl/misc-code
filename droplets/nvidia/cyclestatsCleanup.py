import os
import sys
import re
import csv

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

def _writeListToCsvFile(outFile, line):
    for count, cell in enumerate(line):
        if count > 0:
            outFile.write(',')
        outFile.write(cell)
    outFile.write('\n')

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            inPathList = sys.argv[1:]
            print("[1/2] inPath:")
            for arg in sys.argv[1:]:
                print("\t{}".format(arg))
        else:
            inPath = input("[1/2] inPath: ")
            inPathList = [inPath] 
        outPath = input("[2/2] outPath: ")
        for inPath in inPathList:
            cyclestatsCleanup(inPath, outPath)
    except Exception as e:
        print(e)
        input("press any key")