def numbersInsideRange(limitMin, limitMax):
    lista = []
    for contLoops in range(limitMin+1, limitMax):
        if contLoops %2==1:
            lista.append(contLoops)

    return lista  


limitMin = int(input("Introduce el límite inferior: "))
limitMax = int(input("Introduce el límite superior: "))

lista=numbersInsideRange(limitMin, limitMax)
print(lista)