import customtkinter as tk
from PIL import Image

tk.set_default_color_theme("green")

def login():
    ventana.withdraw() 
    ventana_login = tk.CTk()
    ventana_login.geometry("700x700")



    Textbox = tk.CTkEntry(ventana_login, width=500)
    Textbox.place(x=200, y=650)

    eventos_pendientes = []

    def cerrar_login():
        for evento in eventos_pendientes:
            ventana_login.after_cancel(evento)
        ventana_login.destroy()
        ventana.deiconify()  

    btn_cerrar = tk.CTkButton(ventana_login, text="Volver", command=cerrar_login)
    btn_cerrar.place(x=0, y=0)

    evento = ventana_login.after(500, lambda: print("Animación o evento en proceso"))
    eventos_pendientes.append(evento)

    ventana_login.protocol("WM_DELETE_WINDOW", cerrar_login)

    ventana_login.mainloop()

def register():
    print("Registrarse presionado")

ventana = tk.CTk()
ventana.geometry("700x700")

ruta_imagen = r"C:\Users\JeanC\OneDrive\Desktop\Proyecto Intro\Queso.png"
dark_image = Image.open(ruta_imagen)
my_image = tk.CTkImage(light_image=dark_image, size=(370, 370))

image_label = tk.CTkLabel(ventana, image=my_image, text="")
image_label.place(x=360, y=380)

titulo = tk.CTkLabel(ventana, text="Bienvenido a la IA Theburger", font=("Fixedsys", 30, "bold"))
titulo.place(x=150, y=60)

titulo2 = tk.CTkLabel(ventana, text="¿En qué puedo ayudarte?", font=("Helvetica", 20, "bold"))
titulo2.place(x=150, y=120)

entry_login = tk.CTkEntry(ventana, width=300)
entry_login.place(x=150, y=220)

btn_login = tk.CTkButton(ventana, text="Iniciar Sesión", command=login, width=300, fg_color="#FD8F31")
btn_login.place(x=150, y=250)

entry_register = tk.CTkEntry(ventana, width=300)
entry_register.place(x=150, y=320)

btn_register = tk.CTkButton(ventana, text="Registrarse", command=register, width=300, fg_color="#FD8F31")
btn_register.place(x=150, y=350)

ventana.mainloop()
