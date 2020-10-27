# Adivina el Número

isMatch = 0

def valNum (intGiven, intHidden):
    
    if intGiven == intHidden:
        print("Has acertado")
        return 1
    
    if intGiven < intHidden:
        print("El número oculto es mayor.")
    else: 
        print("El número oculto es menor.")
    
    return 0
    
print("Adivina el número")
print()
print()

intHidden = int(input("Introduce el número oculto: "))
while not isMatch:
    print()
    intGiven = int(input("Introduce un número: "))
    if valNum(intGiven, intHidden):
        isMatch = 1
