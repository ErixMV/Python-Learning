def askNumber():
    callback = input("Introduce un número: ")
    return callback


f = askNumber()
s = askNumber()
t = askNumber()

if f > s and f > t:
    print("El mayor es " + f)

if s > f and s > t:
    print("El mayor es " + s)

if t > s and t > f:
    print("El mayor es " + t)

if f == s or f == t or s == t:
    print('No hay número mayor que otros')
