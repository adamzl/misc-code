import sys
import azlpy.csvTools

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 3:
            inPathList = sys.argv[1:]
            print("[1/1] inPath:")
            for arg in sys.argv[1:]:
                print("\t{}".format(arg))
        else:
            inPathList = []
            while True:
                print("[1/1] inPath: (terminate with blank line)")
                inPath = input("\t")
                if inPath == "":
                    break
                inPathList.append(inPath) 
        azlpy.csvTools.csvMergeToXlsx(inPathList)
    except Exception as e:
        print(e)
        input("press any key")