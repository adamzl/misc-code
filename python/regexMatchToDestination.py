import sys
import azlpy.fileSystem

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            inDir = sys.argv[1]
            print("[1/3] inDir: {}".format(inDir))
        else:
            inDir = input("[1/3] inDir: ")
        outDir = input("[2/3] outDir: ")
        regexFilePattern = input("[3/3] regexFilePattern: ")
        azlpy.fileSystem.regexMatchToDestination(inDir, outDir, regexFilePattern)
    except Exception as e:
        print(e)
        input("press any key")