def suma (num1,num2):
    return num1+num2

def resta (num1,num2):
    return num1-num2

def mult (num1,num2):
    return num1*num2

def div (num1,num2):
    if not num2==0:
        return num1/num2

def default():
   return "Opcion Inválida"

def switcher(case, num1, num2):
    switch = {
        1: suma(num1, num2),
        2: resta(num1, num2),
        3: mult(num1, num2),
        4: div(num1, num2)
    }

    return switch.get(case,default())

num1=int(input("Introduce el primer valor"))
num2=int(input("Introduce el segundo valor"))

print("CALCULADORA")
print()
print("1: Suma")
print("2: Resta")
print("3: Multiplicación")
print("4: División")
print()
menuOpt = int(input("Elije una opción (1-4): "))

mathResult = switcher(menuOpt, num1, num2)

print(str(mathResult))

