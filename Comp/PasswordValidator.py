# Password validator

def passwordValidator (password):
    passControl = 1
    arrVocal = ['A', 'E', 'I', 'O', 'U']

    if len(password) < 8:
        print("Longitud insuficiente (7 min)")
        passControl = 0

    if not password[0] in arrVocal:
        print("El primer carácter no es una vocal mayúscula")
        passControl = 0

    if not password[-1].isnumeric():
        print("El último carácter no es un número")
        passControl = 0

    return passControl

isValidPassword = 0

while not isValidPassword:
    strPassword = input("Introduce tu contraseña a comprobar: ")
    if passwordValidator(strPassword):
        print("Tu password ha sido validada exitosamente. Ningún error encontrado")
        isValidPassword == 1
