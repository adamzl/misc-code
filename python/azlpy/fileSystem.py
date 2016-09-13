import os
import shutil
import glob

def multiFolderToMultiFile(inDir, regexFilePattern, outDir=""):
    if outDir == "":
        outDir = inDir
    os.makedirs(outDir, exist_ok=True)
    fileList = glob.glob(os.path.join(inDir, regexFilePattern))
    for file in fileList:
        newName = os.path.split(os.path.split(file)[0])[1]
        extension = os.path.splitext(file)[1]
        outPath = os.path.join(outDir, newName) + extension
        shutil.copy2(file, outPath)

def regexMatchToDestination(inDir, outDir, regexFilePattern):
    os.makedirs(outDir, exist_ok=True)
    globPattern = os.path.join(inDir, regexFilePattern)
    fileList = glob.glob(globPattern)
    for file in fileList:
        truncatedFile = file[len(inDir)+1:]
        outPath = os.path.join(outDir, truncatedFile)
        shutil.move(file, outPath)