# Juego Preguntas
import sys

print("QUIZ")
print()
answer = input("¿Colón descubrió América? (s/n)")
if answer != "s" and answer != "n":
    print("Valor no válido")
    sys.exit()

if answer == "s":
    print("Correcto")
else:
    print("Incorrecto")
    sys.exit()

print()
answer = input("¿La capital de Inglaterra es Cambrige? (s/n)")
if answer != "s" and answer != "n":
    print("Valor no válido")
    sys.exit()

if answer == "n":
    print("Correcto")
else:
    print("Incorrecto")
    sys.exit()

print()
answer = input("¿El Sol, es una estrella? (s/n)")
if answer != "s" and answer != "n":
    print("Valor no válido")
    sys.exit()

if answer == "s":
    print("Correcto")
else:
    print("Incorrecto")
    sys.exit()
print()
print()
print("Has respondido todas las preguntas correctamente")
