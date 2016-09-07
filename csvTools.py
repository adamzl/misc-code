import os
import glob
import csv
from xlsxwriter.workbook import Workbook

#for a directory of csv files, create single xlsx file with each csv as a worksheet
#adapted from http://stackoverflow.com/a/34715816
def csvMergeToXlsx(directory, deliminator=','):
    workbook = Workbook(os.path.join(directory, os.path.basename(directory)) + ".xlsx", {'strings_to_numbers': True})
    for csvfile in glob.glob(os.path.join(directory, '*.csv')):
        worksheet = workbook.add_worksheet(os.path.splitext(os.path.basename(csvfile))[0])
        with open(csvfile, 'r') as file:
            reader = csv.reader(file)
            for rowNum, rowText in enumerate(reader):
                splitLine = rowText[0].split(deliminator)
                for colNum, colText in enumerate(splitLine):
                    worksheet.write(rowNum, colNum, colText)
    workbook.close()

# dataColumn is zero indexed (column A = 0)
def createVlookupDelta(leftCsvPath, rightCsvPath, outputPath, matchColumn, dataColumn):

    xlsxOutputMode = False
    if os.path.splitext(outputPath)[1] == ".xlsx":
        xlsxOutputMode = True
    lineCount = 0
    lineCountRight = 0
    with open(leftCsvPath, 'r') as leftFile:
        for lineNumber, text in enumerate(leftFile):
            pass
        lineCount = lineNumber + 1
    with open(rightCsvPath, 'r') as rightFile:
        for lineNumber, text in enumerate(rightFile):
            pass
        lineCountRight = lineNumber + 1
    if lineCount != lineCountRight:
        print("Files differ in line count, abort")
        return
    with open(leftCsvPath, 'r') as leftFile:
        with open(rightCsvPath, 'r') as rightFile:
            if xlsxOutputMode == False:
                outputFile = open(outputPath, 'w')
            else:
                outputFile = Workbook(outputPath, {'strings_to_numbers': True})
                worksheet = outputFile.add_worksheet("delta")
            leftReader = csv.reader(leftFile)
            rightReader = csv.reader(rightFile)
            for leftLine,rightLine,lineNumber in zip(leftReader,rightReader,range(1, lineCount)):
                if lineNumber == 1:
                    firstRow = False
                    if xlsxOutputMode == False:
                        outputFile.write("ID,Left,Right,%,Abs Diff,,Right ID,Right Data\n")
                    else:
                        worksheet.write(lineNumber-1, 0, "ID")
                        worksheet.write(lineNumber-1, 1, "Left")
                        worksheet.write(lineNumber-1, 2, "Right")
                        worksheet.write(lineNumber-1, 3, "%")
                        worksheet.write(lineNumber-1, 4, "Abs Diff")
                        worksheet.write(lineNumber-1, 5, "")
                        worksheet.write(lineNumber-1, 6, "Right ID")
                        worksheet.write(lineNumber-1, 7, "Right Data")
                    continue
                if xlsxOutputMode == False:
                    outputList = []
                    outputList.append(leftLine[_convertColumnToZeroOffset(matchColumn)])
                    outputList.append(leftLine[_convertColumnToZeroOffset(dataColumn)])
                    outputList.append("\"=VLOOKUP(A{0},G$2:H${1},2,FALSE)\"".format(lineNumber, lineCount))
                    outputList.append("\"=C{0}/B{0}\"".format(lineNumber))
                    outputList.append("\"=C{0}-B{0}\"".format(lineNumber))
                    outputList.append("")
                    outputList.append(rightLine[_convertColumnToZeroOffset(matchColumn)])
                    outputList.append(rightLine[_convertColumnToZeroOffset(dataColumn)])
                    _writeListToCsvFile(outputFile, outputList)
                else:
                    worksheet.write(lineNumber-1, 0, leftLine[_convertColumnToZeroOffset(matchColumn)])
                    worksheet.write(lineNumber-1, 1, leftLine[_convertColumnToZeroOffset(dataColumn)])
                    worksheet.write(lineNumber-1, 2, "=VLOOKUP(A{0},G$2:H${1},2,FALSE)".format(lineNumber, lineCount))
                    worksheet.write(lineNumber-1, 3, "=C{0}/B{0}".format(lineNumber))
                    worksheet.write(lineNumber-1, 4, "=C{0}-B{0}".format(lineNumber))
                    worksheet.write(lineNumber-1, 5, "")
                    worksheet.write(lineNumber-1, 6, rightLine[_convertColumnToZeroOffset(matchColumn)])
                    worksheet.write(lineNumber-1, 7, rightLine[_convertColumnToZeroOffset(dataColumn)])
            outputFile.close()

# inDir directory of csv files, sum the values in dataColumn from each csv into
# a single row. this forms an output csv file that has the sum of values for
# each csv.
# dataColumn is zero indexed (column A = 0)
def multifileSum(inDir, dataColumn, outPath):
    with open(outPath, 'w') as outFile:
        outFile.write("filename,sum\n")
        for csvFile in glob.glob(os.path.join(inDir, '*.csv')):
            with open(csvFile, 'r') as inFile:
                reader = csv.reader(inFile)
                firstRow = True
                sum = 0.0
                for lineList in reader:
                    if firstRow:
                        firstRow = False
                        continue
                    sum = sum + float(lineList[_convertColumnToZeroOffset(dataColumn)])
                testName = os.path.splitext(os.path.split(csvFile)[1])[0]
                sumString = "{}".format(sum)
                outFile.write(testName + ',' + sumString + '\n')

def _writeListToCsvFile(outFile, line):
    for count, cell in enumerate(line):
        if count > 0:
            outFile.write(',')
        outFile.write(cell)
    outFile.write('\n')

def _convertColumnToZeroOffset(input):
    ordValue = ord(input)
    if ordValue >= 48 and ordValue <= 57: # 0-9
        return ordValue - 48
    if ordValue >= 97 and ordValue <= 122: # a-z
        return ordValue - 97
    if ordValue >= 65 and ordValue <= 90: # A-Z
        return ordValue - 65
    return None

if __name__ == "__main__":
    createVlookupDelta(r"C:\users\aleibel\desktop\left.csv", r"C:\users\aleibel\desktop\right.csv", r"C:\users\aleibel\desktop\vlookup.xlsx", 4, 2)