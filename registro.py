import json


with open("registro.txt", "r", encoding="utf-8") as registro:
    datos = json.load(registro)

def login():
    print("Iniciar sesión presionado")

def register():
    user=input("Usurario: ").lower
    print(user)
    with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as registro:
        registro.close()
    return(True)

register()



