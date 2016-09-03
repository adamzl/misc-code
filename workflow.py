import apic
import csvTools
import nvCsvTools
import glob
import shutil
import os

# bunch of simple functions for use with map()/list comprehensions

#  inFilePath renamed to the directory that contained it and copied to outDir
def moveFileRenameToOriginFolder(inFilePath, outDir):
    newName = os.path.split(os.path.split(inFilePath)[0])[1]
    extension = os.path.splitext(inFilePath)[1]
    outPath = os.path.join(outDir, newName) + extension
    shutil.copy2(inFilePath, outPath)

# cyclestats survey to cleaned up folder
def prepCyclestatsSurvey(originalData, outDir):
    # get all the *.xls files from their directories that were named after the APIC folder
    stageOutDir = os.path.join(outDir, "1_renameFiles")
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(originalData, r"**", r"*"))
    a = [moveFileRenameToOriginFolder(inPath, stageOutDir) for inPath in fileList]

    # clean all the xls files into csv files with only event data
    stageOutDir = os.path.join(outDir, "2_cleanAndConvertToCsv")
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(outDir, "1_renameFiles", r"*"))
    a = [nvCsvTools.cyclestatsCleanup(inPath, stageOutDir) for inPath in fileList]

    # breakout pshader state
    stageOutDir = os.path.join(outDir, "3_stateBreakouts")
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(outDir, "2_cleanAndConvertToCsv", r"*"))
    stateRePatterns = ['pshader.*appHash=(0x[\dA-F`]+)']
    a = [nvCsvTools.cyclestatsStateBreakout(inPath, stageOutDir, stateRePatterns) for inPath in fileList]

#if __name__ == "__main__":
#    prepCyclestatsSurvey(r"C:\Users\aleibel\Desktop\base_driver", r"c:\users\aleibel\desktop\test")