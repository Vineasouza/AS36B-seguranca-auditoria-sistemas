import sys
if __name__ == '__main__':
    while(1): 
        opt = input()
        if(opt == '0'):
            print("opt 0")
        elif(opt == '1'): 
            print("opt 1")
        elif(opt == "exit"):
            sys.exit()
        else:
            print("default") 