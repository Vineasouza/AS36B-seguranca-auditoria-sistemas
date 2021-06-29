import re

# Measure-Command {start-process python rgx.py -Wait -NoNewWindow}
   
if __name__ == '__main__':
    s = "hi my name is ryan, and i am new to python and would like to learn more KEY:=SADNASJBD"
    m = re.search('(?<=KEY:)(.*)', s)
    print(m.groups())

    mystring =  "hi my name is ryan, and i am new to python and would like to learn more KEY:=SADNASJBD"
    keyword = 'KEY:'
    before_keyword, keyword, after_keyword = mystring.partition(keyword)
    print(after_keyword)
