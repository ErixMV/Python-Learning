# Tabla de multiplicar
def createTable (numberForTable):
    cont = 1
    while cont <= 10 :
        print(str(numTable) + " x " + str(cont) + " = " + str(numTable * cont) )
        cont = cont +1

numTable = int(input("Introduce el número de la tabla de multiplicar: "))

createTable(numTable)

