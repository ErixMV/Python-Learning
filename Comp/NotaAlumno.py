# Password validator

def passwordValidator (password):
    passControl = true
    arrVocal = ['A', 'E', 'I', 'O', 'U']

    if len(password) < 8:
        print("Longitud insuficiente")
        passControl = false

    if not password[0] in arrVocal:
        print("El primer carácter no es una vocal consonante")
        passControl = false

    if not isNumeric(string[-1]):
        print("El último carácter no es un número")
        passControl = false

    return passControl

isValidPassword = false

while not isValidPassword:
    strPassword = input("Introduce tu contraseña a comprobar: ")
    if passwordValidator(strPassword):
        print("Tu password ha sido validada exitosamente.")
        isValidPassword == true