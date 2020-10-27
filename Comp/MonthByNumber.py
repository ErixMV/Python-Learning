import sys

def month_number(numberMonth):
    arrMonthName = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    if 1 <= numberMonth <= 12:
        return arrMonthName[numberMonth - 1]
    else:
        sys.exit()

numMonth = int(input("Introduce el número del mes: (1-12)"))
print(month_number(numMonth))
