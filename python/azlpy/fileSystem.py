import os
import shutil
import glob

def moveFileRenameToOriginFolder(inFilePath, outDir):
    newName = os.path.split(os.path.split(inFilePath)[0])[1]
    extension = os.path.splitext(inFilePath)[1]
    outPath = os.path.join(outDir, newName) + extension
    shutil.copy2(inFilePath, outPath)

def regexMatchToDestination(inDir, outDir, regexFilePattern):
    os.makedirs(outDir, exist_ok=True)
    globPattern = os.path.join(inDir, regexFilePattern)
    fileList = glob.glob(globPattern)
    for file in fileList:
        truncatedFile = file[len(inDir)+1:]
        outPath = os.path.join(outDir, truncatedFile)
        shutil.move(file, outPath)