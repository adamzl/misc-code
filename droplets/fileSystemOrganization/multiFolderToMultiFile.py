import os
import sys
import glob
import shutil

#  inFilePath renamed to the directory that contained it and copied to outDir
def _moveFileRenameToOriginFolder(inFilePath, outDir):
    newName = os.path.split(os.path.split(inFilePath)[0])[1]
    extension = os.path.splitext(inFilePath)[1]
    outPath = os.path.join(outDir, newName) + extension
    shutil.copy2(inFilePath, outPath)

def multiFolderToMultiFile(inDir, regexFilePattern, outDir=""):
    if outDir == "":
        outDir = inDir
    os.makedirs(outDir, exist_ok=True)
    fileList = glob.glob(os.path.join(inDir, regexFilePattern))
    for file in fileList:
        _moveFileRenameToOriginFolder(file, outDir)

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            inDir = sys.argv[1]
            print("[1/3] inDir: {}".format(inDir))
        else:
            inDir = input("[1/3] inDir: ")
        regexFilePattern = input("[2/3] regexFilePattern: ")
        outDir = input("[3/3] outDir: ")
        multiFolderToMultiFile(inDir, regexFilePattern, outDir)
    except Exception as e:
        print(e)
        input("press any key")