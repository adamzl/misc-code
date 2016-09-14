import glob
import shutil
import os

import csvTools
import nvidia
import fileSystem

# cyclestats survey to cleaned up folder
def processCyclestatsSurvey(inDir, outDir):
    # get all the *.xls files from their directories that were named after the APIC folder
    stageInDir = inDir
    stageOutDir = os.path.join(outDir, "1_renameFiles")
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(stageInDir, r"**\*.xls"))
    [fileSystem.moveFileRenameToOriginFolder(inPath, stageOutDir) for inPath in fileList]

    # clean all the xls files into csv files with only event data
    stageInDir = stageOutDir
    stageOutDir = os.path.join(outDir, "2_cleanAndConvertToCsv")
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(stageInDir, r"*"))
    for inPath in fileList:
        outPath = os.path.join(stageOutDir, os.path.split(inPath)[1][:-4] + ".csv")
        nvidia.cyclestatsCleanup(inPath, outPath)

    # create multifileSum.csv
    stageInDir = stageOutDir
    stageOutPath = os.path.join(outDir, "multifileSum.csv")
    csvTools.multifileSum(stageInDir, stageOutPath, 'C')