# Pasar de segundos a horas, minutos y segundos

seconds = int(input("Introduce la cantidad de segundos: "))
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print("%d:%02d:%02d" % (h, m, s))
