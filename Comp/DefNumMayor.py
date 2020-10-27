def num_mayor (num1,num2,num3):
    if num1 > num2 and num1> num3:
        print("El mayor es " + num1)

    if num2 > num1 and num2 > num3:
        print("El mayor es " + num2)

    if num3 > num2 and num3 > num1:
        print("El mayor es " + num3)

    if num1== num2 or num1== num3 or num2 == num3:
        print('No hay número mayor que otro')

num1=input("Introduce el primer numero")
num2=input("Introduce el segundo numero")
num3=input("Introduce el tercer numero")

num_mayor(num1,num2,num3)