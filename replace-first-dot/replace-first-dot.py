#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
input_file = raw_input("Enter the input file to replace first occurance: ")
output_file = raw_input("Enter the name of the output file: ")

find = "."
replace = "#:{{எ.கா}}"

inputs = open(input_file,'r').readlines()

outputs = open(output_file,'w')

for line in inputs:
    if "." in line:
#        print line
        if re.search('{.*\.*}', str(line)):
            bracket = re.search('{.*\.*}', str(line)).group(0)
            word_before_dot = line.split(".")[0].split(' ')[-1]
            if word_before_dot in bracket:
                outputs.write(line)
            elif word_before_dot in bracket:
                #print word_before_dot
                line = line.replace(find, replace, 1)
                #The third parameter is the maximum number of occurrences that you want to replace
                outputs.write(line)
            else:
                outputs.write(line)
    else:
        outputs.write(line)

outputs.close()

print "Find and replace completed"
    
