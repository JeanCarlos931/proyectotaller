import json


def login():
    user=input("Usurario: ").lower()
    try:    #Si existe el archivo con el usuario entonces funciona y retorna false
        with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as registro:
            registro.close()
        return(True)
    except: #Si no existe da error el try y en el except crea el archivo retornando ademas un true
        return(False)


def register()->bool:
    """Registra el usuario, si existe retorna un False indicando que ya está registrado ese usuario, si no existe retorna un True indicando que se registro correctamente

    Returns:
        bool: Retorna False si el usuario ya existe, si no un True de que se registró correctamente
    """
    
    user=input("Usurario: ").lower()
    with open("usuario.txt", "w", encoding="utf-8") as archivo_usuario: #Guarda el usuario en un archivo temporal
        archivo_usuario.write(user)

    list_user= [user]
    try:    #Si existe el archivo con el usuario entonces funciona y retorna false
        with open(f"{user}_conversaciones.txt", "r", encoding="utf-8") as registro:
            pass
        return(False)
    except: #Si no existe da error el try, en el except crea el archivo retornando ademas un true
        with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as registro:
            json.dump(list_user, registro, indent=4)
            registro.close()
        return(True)




