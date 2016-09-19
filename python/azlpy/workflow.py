import glob
import shutil
import os

import csvTools
import nvidia
import fileSystem

# cyclestats survey to cleaned up folder
def processCyclestatsSurvey(inDir, outDir, removeIdle=False):
    stepNumber = 0

    # get all the *.xls files from their directories that were named after the APIC folder
    stepNumber = stepNumber + 1
    stageInDir = inDir
    stageOutDir = os.path.join(outDir, "{}_renameFiles".format(stepNumber))
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(stageInDir, r"**\*.xls"))
    [fileSystem.moveFileRenameToOriginFolder(inPath, stageOutDir) for inPath in fileList]

    # clean all the xls files into csv files with only event data
    stepNumber = stepNumber + 1
    stageInDir = stageOutDir
    stageOutDir = os.path.join(outDir, "{}_cleanAndConvertToCsv".format(stepNumber))
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(stageInDir, r"*"))
    for inPath in fileList:
        outPath = os.path.join(stageOutDir, os.path.split(inPath)[1][:-4] + ".csv")
        nvidia.cyclestatsCleanup(inPath, outPath)

    # clear remove idle time, optional
    if removeIdle:
        stepNumber = stepNumber + 1
        stageInDir = stageOutDir
        stageOutDir = os.path.join(outDir, "{}_removeGPUIdle".format(stepNumber))
        os.makedirs(stageOutDir, exist_ok=True)
        fileList = glob.glob(os.path.join(stageInDir, r"*.csv"))
        for inPath in fileList:
            outPath = os.path.join(stageOutDir, os.path.split(inPath)[1])
            csvTools.removeRowsWithColumnValue(inPath, outPath, r"GPUIDLE.*{}$", "D")

    # create multifileSum.csv
    stageInDir = stageOutDir
    stageOutPath = os.path.join(outDir, "multifileSum.csv")
    csvTools.multifileSum(stageInDir, stageOutPath, 'C')

def processCyclestatsFile(inPath):
    nvidia.cyclestatsCleanup(inPath)
    os.remove(inPath)
    inPath = inPath[:-4] + ".csv"
    nvidia.cyclestatsStateBreakout(inPath,
                                   nvidia.stateBreakoutPatterns["tags"] + nvidia.stateBreakoutPatterns["allshaders"])
    nvidia.cyclestatsInsertFormulaHeaders(inPath)