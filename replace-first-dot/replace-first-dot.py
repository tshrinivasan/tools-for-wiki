#!/usr/bin/python
# -*- coding: utf-8 -*-


#Based on https://gist.github.com/bravegnu/03acfa2473c97911d252
#Thanks to Vijayakumar vijaykumar@zilogic.com  of ChennaiPy Group.


STATE_SEARCH_DOT = 0
STATE_SEARCH_CLOSE_FLOWER = 1
STATE_SEARCH_CLOSE_PAREN = 2

matching = {
    '{': '}',
    '(': ')'
}

input_file = raw_input("Enter the input file to replace first occurance: ")
output_file = raw_input("Enter the name of the output file: ")

outputs = open(output_file,'w')

find_string = "."
replace_string = "#:{{எ.கா}}"



def find_first_dot(line):
    paren_stack = []

    for pos, ch in enumerate(line):
        if ch in matching:
            paren_stack.append(ch)

        else:
            if paren_stack: 
                if ch == matching[paren_stack[-1]]:
                    paren_stack.pop()
            else:
                if ch == find_string:
                    return pos

    return -1

            
for line in open(input_file):
#    print line
#    outputs.write(line)
    
    pos = find_first_dot(line)
    if pos != -1:
        line = list(line)
        line[pos] = replace_string
        line = "".join(line)

#    print line
    outputs.write(line)


print "The output is written to : " + output_file
outputs.close()

