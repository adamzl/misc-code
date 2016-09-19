import sys
import azlpy.workflow

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            inPathList = sys.argv[1:]
            print("[1/1] inPath:")
            for arg in sys.argv[1:]:
                print("\t{}".format(arg))
        else:
            inPath = input("[1/1] inPath: ")
            inPathList = [inPath]
        for inPath in inPathList:
            azlpy.workflow.processCyclestatsFile(inPath)
    except Exception as e:
        print(e)
        input("press any key")