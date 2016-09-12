import os
import sys
import csv
from xlsxwriter.workbook import Workbook

def csvMergeToXlsx(fileList):
    workbookPath = os.path.join(os.path.split(fileList[0])[0], os.path.split(os.path.split(fileList[0])[0])[1] + ".xlsx")
    workbook = Workbook(workbookPath, {'strings_to_numbers': True})
    for csvfile in fileList:
        worksheet = workbook.add_worksheet(os.path.splitext(os.path.basename(csvfile))[0])
        with open(csvfile, 'r') as file:
            reader = csv.reader(file)
            for rowNum, rowText in enumerate(reader):
                for colNum, colText in enumerate(rowText):
                    worksheet.write(rowNum, colNum, colText)
    workbook.close()

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
        csvMergeToXlsx(inPathList)
    except Exception as e:
        print(e)
        input("press any key")