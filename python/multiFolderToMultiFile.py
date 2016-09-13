import sys
import azlpy.fileSystem

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            inDir = sys.argv[1]
            print("[1/3] inDir: {}".format(inDir))
        else:
            inDir = input("[1/3] inDir: ")
        regexFilePattern = input("[2/3] regexFilePattern: ")
        outDir = input("[3/3] outDir: ")
        azlpy.fileSystem.multiFolderToMultiFile(inDir, regexFilePattern, outDir)
    except Exception as e:
        print(e)
        input("press any key")