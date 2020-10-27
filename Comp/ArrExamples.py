# Listas

# Buscar en una lista
arrPeople = ['Erix', 'Alexander', 'Julia', 'Illya']
person1 = "Illya"

for (index, person) in enumerate(arrPeople):
    if person == person1:
        print("Index: " + str(index) + ". Persona encontrada: " + person)
        break
else:
    print("El valor no se encuentra.")

# Max and Min

arrIntegers = [4, 3, 8, 5, 18, 54, 23, 28, 6,-700,100]
maxNumber = arrIntegers[0]
minNumber = arrIntegers[0]
for number in arrIntegers:
    if number > maxNumber:
        maxNumber = number

    if number < minNumber:
        minNumber = number

print("Número máximo: " + str(maxNumber))
print("Número mínimmo: " + str(minNumber))

# Ordenar lista

arrOrdered = [arrIntegers[0]]
maximum = arrIntegers[0]

for i in range(0, len(arrIntegers)-1):
    for j in range(i + 1, len(arrIntegers)):
        if arrIntegers[i] > arrIntegers[j]:
            tempNum = arrIntegers[i]
            arrIntegers[i] = arrIntegers[j]
            arrIntegers[j] = tempNum

print()
print()
print()
print("Array ordenada: " + str(arrIntegers))
