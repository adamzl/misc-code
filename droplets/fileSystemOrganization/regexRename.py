import os
import sys
import re
import shutil

# will rename files by using only those that match regex.
# new name is the concatination of the regex groups
def regexRename(inPath, regexPattern):

    match = re.match(regexPattern, file)
    if match:
        newFilename = ""
        for group in match.groups():
            newFilename = newFilename + group
        shutil.move(os.path.join(inDir, file), os.path.join(inDir, newFilename))

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            inDir = sys.argv[1]
            print("[1/2] inDir: {}".format(inDir))
        else:
            inDir = input("[1/2] inDir: ")
        regexPattern = input("[2/2] regexPattern: ")
        regexRename(inDir, regexPattern)
    except Exception as e:
        print(e)
        input("press any key")