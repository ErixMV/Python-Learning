# Precio real y descuento

real = float(input("Introduce el precio original: "))
paid = float(input("Introduce el precio pagado: "))
disc = (paid*100)/real

discountQ = real - paid
discountP = 100 - disc
print("Descuento: " + str(discountQ) + "(" + str(discountP) + "%)")
