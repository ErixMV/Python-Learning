from math import pi

def circleArea(r):
    area=pi*(r*r)
    return area
radio=float(input("Introduce el radio del círculo"))
print(circleArea(radio))
