import sys
import re
import azlpy.nvidia

predefinedRegexPatterns = [
    ("[tags, pshader, compute]", ["^([A-Z_<>]+)", "pshader{[^}]*?appHash=(0x[\dA-F`]+)", "compute{[^}]*?appHash=(0x[\dA-F`]+)"]),
    ("[tags, pshader.apphash, pshader.ucodehash, compute.apphash, compute.ucodehash]", ["^([A-Z_<>]+)",
                                                                                        "pshader{[^}]*?appHash=(0x[\dA-F`]+)", "pshader{[^}]*?ucodeHash=(0x[\dA-F`]+)",
                                                                                        "compute{[^}]*?appHash=(0x[\dA-F`]+)", "compute{[^}]*?ucodeHash=(0x[\dA-F`]+)"]),
    ("[tags, pshader/compute/vshader/gshader/hullshader/domainshader.appHash/ucodeHash]", ["^([A-Z_<>]+)",
                                                                                           "pshader{[^}]*?appHash=(0x[\dA-F`]+)", "pshader{[^}]*?ucodeHash=(0x[\dA-F`]+)",
                                                                                           "compute{[^}]*?appHash=(0x[\dA-F`]+)", "compute{[^}]*?ucodeHash=(0x[\dA-F`]+)",
                                                                                           "vshader{[^}]*?appHash=(0x[\dA-F`]+)", "vshader{[^}]*?ucodeHash=(0x[\dA-F`]+)",
                                                                                           "gshader{[^}]*?appHash=(0x[\dA-F`]+)", "gshader{[^}]*?ucodeHash=(0x[\dA-F`]+)",
                                                                                           "hullshader{[^}]*?appHash=(0x[\dA-F`]+)", "hullshader{[^}]*?ucodeHash=(0x[\dA-F`]+)",
                                                                                           "domainshader{[^}]*?appHash=(0x[\dA-F`]+)", "domainshader{[^}]*?ucodeHash=(0x[\dA-F`]+)"]),
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
            print("\t{0}: {1}".format(count, pattern[0]))
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