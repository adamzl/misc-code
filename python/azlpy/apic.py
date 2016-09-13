import glob
import os
import re
import subprocess
import sys

def runApicDir(ApicDirectory, apicParameters, logsPath=""):
    outputDir = os.path.join(ApicDirectory, "logs")
    os.makedirs(outputDir, exist_ok=True)
    print("Writing output to " + outputDir)
    if logsPath != "":
        outLogsPath = os.path.join(ApicDirectory, "logs")
        print("Copying per-run logs from " + logsPath + " to " + outLogsPath)
    with open(os.path.join(outputDir, "results.csv"), "w") as outputFile:
        outputFile.write("APIC,Average FPS,Plus Minus,Frames")
        for dirItem in os.scandir(ApicDirectory):
            if dirItem.path == outputDir:
                continue
            if dirItem.is_dir():
                executablePath = glob.glob(os.path.join(dirItem.path, "x64", "*.exe"))
                commandLine = [executablePath[0]] + apicParameters.split(" ")
                print(commandLine[0])
                thread = subprocess.Popen(commandLine,
                                        cwd=dirItem.path,
                                        stdout=subprocess.PIPE)
                thread.wait()
                output = thread.communicate()[0].decode("utf-8")
                reresult = re.search(r"total time: (\d+\.\d+) seconds, (\d+) frames, average FPS: (\d+\.\d+) plus or minus (\d+\.\d+)%", output)
                if reresult:
                    outputFile.write("\n" + dirItem.name + "," + reresult.groups()[2] + "," + reresult.groups()[3] + "," + reresult.groups()[1])
                else:
                    outputFile.write("\n" + dirItem.name)
                if logsPath != "":
                    logList = glob.glob(os.path.join(logsPath, "*"))
                    os.makedirs(os.path.join(outLogsPath, dirItem.name), exist_ok=True)
                    for logItem in logList:
                        os.rename(logItem, os.path.join(outLogsPath, dirItem.name, os.path.basename(logItem)))

if __name__ == "__main__":
    runApicDir(r"C:\Users\adam\Desktop\test", "100 100", logsPath=r"c:\users\adam\desktop\logging")