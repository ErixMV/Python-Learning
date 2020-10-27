# Triangle

h = int(input("Introduce la altura: "))
cont = 1
str = "* "

while cont <= h:
    print(cont * str)
    cont = cont + 1

cont = h - 1 

while cont > 0:
    print(cont * str)
    cont = cont - 1
