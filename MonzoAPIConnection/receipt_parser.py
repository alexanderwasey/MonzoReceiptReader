import re

def parsereceipt(text_dump):

    #Initializing a list to dump in the lines of the text file into
    list_of_lines = []
    for line in text_dump:
        #Removing spaces in each line because of OCR inconsistency. Will use to check if the line corresponds to price format.
        line_no_space = line.replace(' ', '')
        #In order to avoid entries that are too short (or misread by the OCR) we set a minimum length of 4 for each line to be deemed useful (this holds for the price format)
        if len(line.strip()) > 3:
            #Checking to see if the line contains a dot (decimal point in prices)
            #We want to remove the space between digits that the OCR creates and keep the spaces for the item titles.
            if('.' in line):
                pos = line_no_space.find('.')
                #Note: OCR sometimes reads 0's as an 'O', thus we account for this case in distinguishing whether a line is the price.
                if ((line_no_space[pos-1].isdigit()) or line_no_space[pos-1].upper() == 'O') and (line_no_space[pos+1].isdigit() or line_no_space[pos+1].upper() == 'O'):
                    list_of_lines.append(line_no_space)
                else:
                    list_of_lines.append(line.strip())
            else:
                list_of_lines.append(line.strip())
    #We want to find the first price tag and limit the lines that we store to the start of the individual items (the line before the first price contains the title of the first item)
    flag = -1
    for line in list_of_lines:
        if('.' in line):
            pos = line.find('.')
            if ((line[pos-1].isdigit()) or line[pos-1].upper() == 'O') and (line[pos+1].isdigit()):
                break
        flag = flag + 1
    #We now create the items_list which is the only starts
    items_list = list_of_lines[flag:]
    #We now look for the where the listing of the individual items ends. This will usually be indicated by a TOTAL or BALANCE item.
    #We look for the last occurence of TOTAL or BALANCE (sometimes we can have Subtotals, so we look for the final occurence)
    i = 0
    last_index = 0
    for item in items_list:
        if ('TOTAL' in item.upper()) or ('BALANCE' in item.upper()):
            last_index = i
        i = i + 1
    items_list = items_list[:last_index]
    #Formatting the prices with a pound sign at the beginning.
    #Azure API is severely lacking in international characters and currency and doesn't recognize the £ symbol.
    for i in range(len(items_list)):
        if not(i % 2 == 0):
            items_list[i] = "£" + items_list[i][1:]

    #Uses a regex to get rid of all characters that are not alphanumeric and not spaces.
    for i in range((len(items_list)//2)):
        items_list[i*2] = re.sub(r'([^\s\w]|_)+', '', items_list[i*2])
        temp_array = items_list[i*2].split()
        second_array = []
        #Capitalises the first letter of each word in the description.
        for x in temp_array:
            second_array.append(x[0].upper() + x[1:].lower())
        items_list[i*2] = " ".join(second_array)

    #Replaces the 'O' characters that OCR may have misread with '0'.
    for i in range((len(items_list)//2)):
        items_list[i*2+1] = re.sub(r'O', '0', items_list[i*2+1])

    #Creates the list of tuples that will be outputted to Monzo API.
    output_tuples = []
    for i in range((len(items_list)//2)):
        temp_price_string = items_list.pop()[1:]
        pos = line.find('.')
        pounds = int(temp_price_string[:pos-1])
        pence = int(temp_price_string[pos:])
        #Calculating the price in pence.
        temp_price = 100*pounds + pence
        temp_desc = items_list.pop()
        output_tuples.append((temp_desc, 1, temp_price))
    output_tuples.reverse()
    return output_tuples

#Finds VAT number is one exists
def findVAT(text_dump):
    for line in text_dump:
        if "Vat" in line: 
            pos = line.find(':')
            return line[(pos + 2):]
    return None
