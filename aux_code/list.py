

if __name__ == '__main__':
    list = [
        {"name": "Tom", "age": 10},
        {"name": "Mark", "age": 5},
        {"name": "Pam", "age": 7}
    ]
    list_aux = []

    print("LISTA INICIAL: " + str(list))
    
    
    idx = input("idx 0 a "+ str(len(list) - 1)+" >> ")
    if(int(idx) < len(list)):
        for i in range(int(idx), len(list)):
            list_aux.append(list.pop((int(idx))))
    else:
        raise IndexError

    x = []
    for i in range(len(list_aux)):
        if(i ==int(idx)-1):
            list_aux[i]["name"] = "Jhon"
        
        x.append(list_aux[i]["name"])

    print("LISTA FINAL >> " + str(list))
    print("LISTA AUX >> " + str(list_aux))
    print("RESULTADO >> "+ str(x))
    