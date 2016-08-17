import os
import glob
import csv
import re

#convert CycleStats outputted xls to a csv
#expand the vshader, pshader, and compute subfields to their own columns
def tabXls_to_csv_shader_expand(inFilepath):
    outFilepath = inFilepath[:-3] + 'csv'
    with open(outFilepath, 'w') as outFileObject:
        with open(inFilepath, 'r') as inFileObject:
            csvReader = csv.reader(inFileObject, dialect='excel-tab')
            for line in csvReader:
                #regex patterns for lines to throw away
                if re.match('version=', line[0]):
                    continue
                #throw away everything from "-- CycleState: config --"
                if re.match('-- CycleStat: config --', line[0]):
                    break
                for count, cell in enumerate(line):
                    if count > 0:
                        outFileObject.write(',')
                    outFileObject.write(cell)
                outFileObject.write('\n')

def return_csv_string_list_for_state_pairs(columnPairs, text):
    outputText = ''
    for category, subCategory in columnPairs:
        matchObjectCategory = re.search(category + r'{(.*)}', text)
        if matchObjectCategory:
            matchObjectSubCategory = re.search(subCategory + r'=([\S]+)')
            if matchObjectSubCategory:
                outputText = outputText + matchObjectSubCategory.group(1) + ','
            else:
                outputText = outputText + ','

tabXls_to_csv(r'C:\data\binary_const_folding\3dmark gt1\cycleStats001.xls')