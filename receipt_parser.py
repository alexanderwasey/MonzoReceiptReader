"""
TO DO:
1. Fix the labels for each item and it's spacing.
"""

text_dump = open("sample_texts/sample1.txt", "r")

""" 
Taking the bulk text file outputted by Azure and seperating each line
and removing the spaces in each line. 
"""

#Initializing a list to dump in the lines of the text file into
list_of_lines = []
for line in text_dump:
    #Removing spaces in each line because of OCR inconsistency
    line_no_space = line.replace(' ', '')
    if not len(line.strip()) == 0:
        #Removing newline at the end of each line and adding it to list of lines
        list_of_lines.append(line_no_space[:-1])

flag = -1

for line in list_of_lines:
    
    if('.' in line):
        pos = line.find('.')
        if (line[pos-1].isdigit()) and (line[pos+1].isdigit()):
            break
    flag = flag + 1

items_list = list_of_lines[flag:]
i = 0
last_index = 0
for item in items_list:
    if ('TOTAL' in item.upper()) or ('BALANCE' in item.upper()):
        last_index = i
    i = i + 1
items_list = items_list[:last_index+2]
print(items_list)

