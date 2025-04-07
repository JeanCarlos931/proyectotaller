import json
import customtkinter as tk
from PIL import Image
import os

tk.set_default_color_theme("green")

def guardar_usuario_actual(user):
    """_summary_

    Args:
        user (_persona_): guarda la persona en un documento txt.
    """
    with open("usuario.txt", "w", encoding="utf-8") as archivo:
        archivo.write(user)


def login():
    user = entry_login.get().lower()
    if not user:
        mensaje.configure(text="Por favor, ingresa un nombre de usuario para iniciar sesión.", text_color="red")
        return

    try:
        with open(f"{user}_conversaciones.txt", "r", encoding="utf-8") as archivo:
            historial_guardado = json.load(archivo)
            mensaje.configure(text=f"Inicio de sesión exitoso. Bienvenido, {user}.", text_color="green")
    except FileNotFoundError:
        mensaje.configure(text="El usuario no está registrado.", text_color="red")
        return

    ventana.withdraw()
    ventana_chat = tk.CTk()
    ventana_chat.geometry("1000x700")
    ventana_chat.title(f"Sesión de {user}")

    # ─────────── PANEL IZQUIERDO: HISTORIAL ───────────
    marco_historial = tk.CTkScrollableFrame(ventana_chat, width=300, height=660)
    marco_historial.place(x=10, y=20)

    tk.CTkLabel(marco_historial, text="Historial", font=("Arial", 18, "bold")).pack(pady=10)

    for msg in historial_guardado[1:]:
        mensaje_hist = tk.CTkLabel(marco_historial,text=msg,anchor="w",justify="left",wraplength=270,fg_color="#333333",text_color="white",corner_radius=10)
        mensaje_hist.pack(padx=10, pady=5, anchor="w")

    # ─────────── PANEL DERECHO: CHAT ACTUAL ───────────
    marco_chat = tk.CTkScrollableFrame(ventana_chat, width=650, height=600)
    marco_chat.place(x=330, y=20)

    def mostrar_mensaje(texto, alineado_izq=True):
        burbuja = tk.CTkLabel(marco_chat,text=texto,anchor="w" if alineado_izq else "e",justify="left",fg_color="#2a2a2a" if alineado_izq else "#1f6aa5",text_color="white",corner_radius=12,width=500,wraplength=500)
        burbuja.pack(padx=10, pady=5, anchor="w" if alineado_izq else "e")

    # Campo de texto y botón de enviar
    caja_mensaje = tk.CTkEntry(ventana_chat, width=500)
    caja_mensaje.place(x=330, y=630)

    def enviar():
        texto = caja_mensaje.get().strip()
        if texto:
            mostrar_mensaje(f"Tú: {texto}", alineado_izq=False)
            historial_guardado.append(f"Tú: {texto}")
            caja_mensaje.delete(0, "end")

            with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as archivo:
                json.dump(historial_guardado, archivo, indent=4)

            # También mostrar en historial (izquierda)
            mensaje_hist = tk.CTkLabel(marco_historial,text=f"Tú: {texto}",anchor="w",justify="left",wraplength=270,fg_color="#333333",text_color="white",corner_radius=10)
            mensaje_hist.pack(padx=10, pady=5, anchor="w")

    boton_enviar = tk.CTkButton(ventana_chat, text="Enviar", command=enviar, width=100)
    boton_enviar.place(x=840, y=630)

    # Botón volver
    def cerrar_chat():
        ventana_chat.destroy()
        ventana.deiconify()

    boton_volver = tk.CTkButton(ventana_chat, text="Volver", command=cerrar_chat)
    boton_volver.place(x=10, y=10)

    ventana_chat.mainloop()

def register():
    user = entry_register.get().lower()
    if not user:
        mensaje.configure(text="Por favor, ingresa un nombre de usuario para registrarte.", text_color="red")
        return

    if os.path.exists(f"{user}_conversaciones.txt"):
        mensaje.configure(text="El usuario ya está registrado.", text_color="orange")
        return

    with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as archivo:
        json.dump([user], archivo, indent=4)

    guardar_usuario_actual(user)
    mensaje.configure(text="Usuario registrado correctamente.", text_color="green")


# Interfaz principal
ventana = tk.CTk()
ventana.geometry("700x700")

ruta_imagen = "Queso.png"
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

# Mensaje informativo
mensaje = tk.CTkLabel(ventana, text="", font=("Helvetica", 16))
mensaje.place(x=150, y=400)

ventana.mainloop()
