import glob
import os
import re
import subprocess
import sys

def runApicDir(ApicDirectory, outDir, logsDir, apicParameters):
    os.makedirs(outDir, exist_ok=True)
    with open(os.path.join(outDir, "apic_fps.csv"), "w") as outputFile:
        outputFile.write("APIC,Average FPS,Plus Minus,Frames")
        for dirItem in os.scandir(ApicDirectory):
            if dirItem.path == outDir:
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
                os.makedirs(os.path.join(outDir, dirItem.name), exist_ok=True)
                logList = glob.glob(os.path.join(logsDir, "*"))
                for logItem in logList:
                    os.rename(logItem, os.path.join(outDir, dirItem.name, os.path.basename(logItem)))

def multiRunApicDir(ApicDirectory, outDir, perRunScriptDir, logsDir, apicParameters):
    runScriptList = glob.glob(os.path.join(perRunScriptDir, r"*"))
    for runScript in runScriptList:
        runOutDir = os.path.join(outDir, os.path.splitext(os.path.split(runScript)[1])[0])
        os.makedirs(outDir, exist_ok=True)
        thread = subprocess.Popen(runScript, stdout=subprocess.PIPE)
        thread.wait()
        output = thread.communicate()[0].decode("utf-8")
        runApicDir(ApicDirectory, runOutDir, logsDir, apicParameters)