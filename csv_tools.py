#adapted from http://stackoverflow.com/a/34715816

import os
import glob
import csv
from xlsxwriter.workbook import Workbook

def csv_merge(directory, deliminator=','):
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