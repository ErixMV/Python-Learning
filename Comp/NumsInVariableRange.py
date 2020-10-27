def numbersInsideRange(limitMin, limitMax):

    for contLoops in range(limitMin+1, limitMax):
        print(contLoops)

limitMin = int(input("Introduce el límite inferior: "))
limitMax = int(input("Introduce el límite superior: "))

numbersInsideRange(limitMin, limitMax)