import sys
import re
import azlpy.nvidia

predefinedRegexPatterns = [
    ("tags", azlpy.nvidia.stateBreakoutPatterns["tags"]),
    ("pshader + compute", azlpy.nvidia.stateBreakoutPatterns["pshader"] + azlpy.nvidia.stateBreakoutPatterns["compute"]),
    ("all shaders", azlpy.nvidia.stateBreakoutPatterns["allshaders"]),
]

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
        print("[2/2] regexPattern: enter a single expression or ^^#")
        for count,pattern in enumerate(predefinedRegexPatterns):
            print("\t^^{0}: {1}".format(count, pattern[0]))
        inputPatternText = input("      regexPattern: ")
        match = re.fullmatch("\^\^(\d+)", inputPatternText)
        if match:
            regexPattern = predefinedRegexPatterns[int(match.group(1))][1]
        else:
            regexPattern = [inputPatternText]
        for inPath in inPathList:
            azlpy.nvidia.cyclestatsStateBreakout(inPath, regexPattern)
    except Exception as e:
        print(e)
        input("press any key")