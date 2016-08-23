import glob
import os
import re
import subprocess
import sys

def runApicDir(ApicDirectory, apicParameters, outputPath=""):
    if outputPath == "":
        outputPath = os.path.join(ApicDirectory, "runApicDirResult.csv")
    with open(outputPath, "w") as outputFile:
        outputFile.write("APIC,Averag FPS,Plus Minus,Frames")
        for dirItem in os.listdir(ApicDirectory):
            dirItemPath = os.path.join(ApicDirectory, dirItem);
            if os.path.isdir(dirItemPath):
                executablePath = glob.glob(os.path.join(dirItemPath, "*.exe"))
                commandLine = [executablePath[0], apicParameters]
                thread = subprocess.Popen(commandLine,
                                        cwd=dirItemPath,
                                        stdout=subprocess.PIPE)
                thread.wait()
                output = thread.communicate()[0].decode("utf-8")
                reresult = re.match(r"^total time: (\d+\.\d+) seconds, (\d+) frames, average FPS: (\d+\.\d+) plus or minus (\d+\.\d+)%", output)
                outputFile.write("\n" + dirItem + "," + reresult.groups()[2] + "," + reresult.groups()[3] + "," + reresult.groups()[1])

if __name__ == "__main__":
    runApicDir(sys.argv[1], sys.argv[2])