import sys
import os
import shutil

import nvidia.cyclestatsCleanup
import nvidia.cyclestatsStateBreakout

def cyclestatsPrep(inPath):
    nvidia.cyclestatsCleanup(inPath)
    os.remove(inPath)
    shutil.move("_" + inPath, inPath)
    nvidia.cyclestatsStateBreakout(inPath,
                                   ["^([A-Z_<>]+)", #tag
                                   "pshader.*appHash=(0x[\dA-F`]+)",
                                   "pshader.*ucodeHash=(0x[\dA-F`]+)",
                                   "compute.*appHash=(0x[\dA-F`]+)",
                                   "compute.*ucodeHash=(0x[\dA-F`]+)"])
    os.remove(inPath)
    shutil.move("_" + inPath, inPath)
    _insertSumRow(inPath)
    os.remove(inPath)
    shutil.move("_" + inPath, inPath)

def _insertSumRow(inPath):
    with open(inPath, "w") as inFile:
        with open("_" + inPath) as outFile:
            isFirstLine = True
            for line in inFile:
                if isFirstLine:
                    isFirstLine = False
                    sumRowListText = ["=subtotal(109,{0}1:{0}1000000)".format(chr(charCode)) for charCode in range(65, 65 + len(line))]
                    _writeListToCsvFile(outFile, sumRowListText)
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
        print("[1/1] inPath:")
        for arg in sys.argv[1:]:
            print("\t{}".format(arg))
    else:
        inPath = input("[1/1] inPath: ")
        inPathList = [inPath]
    for inPath in inPathList:
        cyclestatsPrep(inPath)