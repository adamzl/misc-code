import os
import sys
import glob
import shutil

def regexMatchToDestination(inDir, outDir, regexFilePattern):
    os.makedirs(outDir, exist_ok=True)
    globPattern = os.path.join(inDir, regexFilePattern)
    fileList = glob.glob(globPattern)
    for file in fileList:
        truncatedFile = file[len(inDir)+1:]
        outPath = os.path.join(outDir, truncatedFile)
        shutil.move(file, outPath)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        inDir = sys.argv[1]
        print("[1/3] inDir: {}".format(inDir))
    else:
        inDir = input("[1/3] inDir: ")
    outDir = input("[2/3] outDir: ")
    regexFilePattern = input("[3/3] regexFilePattern: ")
    regexMatchToDestination(inDir, outDir, regexFilePattern)