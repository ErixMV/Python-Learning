# Suma y media

num = 1
acc = 0
cont = 0

while num != 0:
    num = int(input("Introduce un número (0 para salir): "))
    acc = acc + num
    cont = cont + 1

print("Suma: " + str(acc))
print("Media: " + str(acc/cont))
