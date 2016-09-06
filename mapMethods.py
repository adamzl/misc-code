import os
import shutil

#  inFilePath renamed to the directory that contained it and copied to outDir
def moveFileRenameToOriginFolder(inFilePath, outDir):
    newName = os.path.split(os.path.split(inFilePath)[0])[1]
    extension = os.path.splitext(inFilePath)[1]
    outPath = os.path.join(outDir, newName) + extension
    shutil.copy2(inFilePath, outPath)