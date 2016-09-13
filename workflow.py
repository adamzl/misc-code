import glob
import shutil
import os

import apic
import csvTools
import nvCsvTools
import mapMethods

# cyclestats survey to cleaned up folder
def prepCyclestatsSurvey(originalData, outDir):
    # get all the *.xls files from their directories that were named after the APIC folder
    stageOutDir = os.path.join(outDir, "1_renameFiles")
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(originalData, r"**", r"*"))
    a = [mapMethods.moveFileRenameToOriginFolder(inPath, stageOutDir) for inPath in fileList]

    # clean all the xls files into csv files with only event data
    stageOutDir = os.path.join(outDir, "2_cleanAndConvertToCsv")
    os.makedirs(stageOutDir, exist_ok=True)
    fileList = glob.glob(os.path.join(outDir, "1_renameFiles", r"*"))
    a = [nvCsvTools.cyclestatsCleanup(inPath, stageOutDir, True) for inPath in fileList]

    # create multifileSum.csv
    stageOutPath = os.path.join(outDir, "multifileSum.csv")
    csvTools.multifileSum(stageOutDir, 'C', stageOutPath)

#if __name__ == "__main__":
#    prepCyclestatsSurvey(r"C:\Users\aleibel\Desktop\base_driver", r"c:\users\aleibel\desktop\test")