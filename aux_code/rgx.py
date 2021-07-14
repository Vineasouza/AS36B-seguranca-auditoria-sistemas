import re

# Measure-Command {start-process python rgx.py -Wait -NoNewWindow}
   
if __name__ == '__main__':
    s = "hi my name is ryan, and i am new to python and would like to learn more KEY:=SADNASJBD SIGN:=QADSASJBD"

    # Scan through string looking for the first location where this regular expression produces a match, 
    # and return a corresponding match object.
    m = re.search('(?<=KEY:)(.*?)(?=\s)', s)
    m2 = re.search('(?<=SIGN:)(.*?)(?=$)', s)
    
    # Returns one or more subgroups of the match.
    print(m.group())
    print(m2.group())

    # mystring =  "hi my name is ryan, and i am new to python and would like to learn more KEY:=SADNASJBD"
    # keyword = 'KEY:'
    # before_keyword, keyword, after_keyword = mystring.partition(keyword)
    # print(after_keyword)
