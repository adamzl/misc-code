import sys
import azlpy.nvidia

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            inPathList = sys.argv[1:]
            print("[1/2] inPath:")
            for arg in sys.argv[1:]:
                print("\t{}".format(arg))
        else:
            inPath = input("[1/2] inPath: ")
            inPathList = [inPath] 
        outPath = input("[2/2] outPath: ")
        for inPath in inPathList:
            azlpy.nvidia.cyclestatsCleanup(inPath, outPath)
    except Exception as e:
        print(e)
        input("press any key")