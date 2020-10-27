# Suma de 100 impares
cont = 100
acumuladorImpar = 0
# De 100 a 1 según cont
while cont >= 1 :
    # Si impar, mostrar por pantalla
    if cont % 2 == 1:
        print(str(cont))
        acumuladorImpar = acumuladorImpar + cont

    # Resta del contador
    cont = cont -1

print("Suma de impares: ", str(acumuladorImpar))
