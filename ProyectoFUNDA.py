import json
import customtkinter as tk
from PIL import Image
import os
from datetime import datetime
import API

tk.set_default_color_theme("green")

def guardar_usuario_actual(user):
    """Guarda el nombre del usuario en un archivo txt."""
    with open("usuario.txt", "w", encoding="utf-8") as archivo:
        archivo.write(user)

def login():
    user = entry_login.get().lower()
    if not user:
        mensaje.configure(text="Por favor, ingresa un nombre de usuario para iniciar sesión.", text_color="red")
        return

    try:
        with open(f"{user}_conversaciones.txt", "r", encoding="utf-8") as archivo:
            global historial_guardado  # Hacerlo global para poder usarlo en otras funciones
            historial_guardado = json.load(archivo)
            mensaje.configure(text=f"Inicio de sesión exitoso. Bienvenido, {user}.", text_color="green")
    except FileNotFoundError:
        mensaje.configure(text="El usuario no está registrado.", text_color="red")
        return

    ventana.withdraw()
    ventana_chat = tk.CTk()
    ventana_chat.geometry("1000x700")
    ventana_chat.title(f"Sesión de {user}")

    # Panel izquierdo: historial
    marco_historial = tk.CTkScrollableFrame(ventana_chat, width=300, height=660)
    marco_historial.place(x=10, y=20)

    tk.CTkLabel(marco_historial, text="Historial", font=("Arial", 18, "bold")).pack(pady=10)

    # Panel derecho: chat actual
    marco_chat = tk.CTkScrollableFrame(ventana_chat, width=650, height=600)
    marco_chat.place(x=330, y=20)

    # Función para mostrar mensajes
    def mostrar_mensaje(texto, alineado_izq=True):
        burbuja = tk.CTkLabel(marco_chat, text=texto, anchor="w" if alineado_izq else "e", justify="left", fg_color="#2a2a2a" if alineado_izq else "#1f6aa5", text_color="white", corner_radius=12, width=500, wraplength=500)
        burbuja.pack(padx=10, pady=(5, 0), anchor="w" if alineado_izq else "e")

    # Función para mostrar la fecha
    def mostrar_fecha(fecha):
        label_fecha = tk.CTkLabel(marco_chat, text=fecha, font=("Arial", 10), text_color="#aaaaaa")
        label_fecha.pack(pady=(0, 5))

    pregunta_actual = tk.StringVar()  # Guardará la pregunta seleccionada
    
    # Función para cargar el chat cuando se hace clic en una pregunta del historial
    def cargar_chat(pregunta_seleccionada):
        pregunta_actual.set(pregunta_seleccionada)  # Guardamos la selección

        # Limpiar el área de chat antes de cargar nuevos mensajes
        for widget in marco_chat.winfo_children():
            widget.destroy()

        for entrada in historial_guardado:
            if isinstance(entrada, dict) and entrada.get("pregunta") == pregunta_seleccionada:
                mostrar_mensaje(f"Tú: {entrada['pregunta']}", alineado_izq=False)
                mostrar_fecha(entrada["timestamp"])
                mostrar_mensaje(f"ChatBot: {entrada['respuesta']}", alineado_izq=True)
                mostrar_fecha(entrada["timestamp"])
                break
        # Limpiar el área de chat antes de cargar nuevos mensajes
        for widget in marco_chat.winfo_children():
            widget.destroy()

        # Buscar la pregunta seleccionada en el historial guardado
        for entrada in historial_guardado:
            if isinstance(entrada, dict):  # Verifica que la entrada sea un diccionario
                if entrada.get("pregunta") == pregunta_seleccionada:  # Usar .get() para evitar KeyError
                    # Mostrar la pregunta y la respuesta en el chat
                    mostrar_mensaje(f"Tú: {entrada['pregunta']}", alineado_izq=False)
                    mostrar_fecha(entrada["timestamp"])
                    mostrar_mensaje(f"ChatBot: {entrada['respuesta']}", alineado_izq=True)
                    mostrar_fecha(entrada["timestamp"])
                    break
            else:
                print(f"Entrada no válida: {entrada}")  # Agrega un mensaje para depurar el tipo de entrada

    # Mostrar preguntas como botones en el historial
    for entrada in historial_guardado:
        if isinstance(entrada, dict):  # Solo si es un diccionario válido
            hora = entrada.get("timestamp", "")[-5:]
            btn = tk.CTkButton(marco_historial, text=f"{entrada['pregunta']} ({hora})", anchor="w", width=270, command=lambda p=entrada["pregunta"]: cargar_chat(p))
            btn.pack(padx=10, pady=5, anchor="w")

    # Campo de texto y botón de enviar
    caja_mensaje = tk.CTkEntry(ventana_chat, width=500)
    caja_mensaje.place(x=330, y=630)

    def enviar():
        texto = caja_mensaje.get().strip()
        if texto:
            mostrar_mensaje(f"Tú: {texto}", alineado_izq=False)
            caja_mensaje.delete(0, "end")

            Mensajerespuesta = API.chat(texto)
            if Mensajerespuesta:
                mostrar_mensaje(f"ChatBot: {Mensajerespuesta}", alineado_izq=True)

                nueva_entrada = {
                    "pregunta": texto,
                    "respuesta": Mensajerespuesta,
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
                }

                # Agregar la nueva entrada al historial_guardado
                historial_guardado.append(nueva_entrada)

                with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as archivo:
                    json.dump(historial_guardado, archivo, indent=4)

                hora = nueva_entrada["timestamp"][-5:]
                btn = tk.CTkButton(marco_historial, text=f"{texto} ({hora})", anchor="w", width=270,command=lambda p=texto: cargar_chat(p))
                btn.pack(padx=10, pady=5, anchor="w")

            caja_mensaje.delete(0, "end")

    boton_enviar = tk.CTkButton(ventana_chat, text="Enviar", command=enviar, width=100)
    boton_enviar.place(x=840, y=630)

    # Botón de cerrar chat
    def cerrar_chat():
        ventana_chat.destroy()
        ventana.deiconify()

    boton_volver = tk.CTkButton(ventana_chat, text="Volver", command=cerrar_chat)
    boton_volver.place(x=10, y=10)

    # --- BOTÓN PARA BUSCAR PALABRAS RELACIONADAS ---
    def abrir_ventana_busqueda():
        ventana_busqueda = tk.CTkToplevel(ventana_chat)
        ventana_busqueda.title("Buscar en historial")
        ventana_busqueda.geometry("500x400")
        ventana_busqueda.configure(fg_color="#666666")

        entrada_busqueda = tk.CTkEntry(ventana_busqueda, width=300, placeholder_text="Escribe una palabra clave")
        entrada_busqueda.pack(pady=10)

        resultado_box = tk.CTkTextbox(ventana_busqueda, width=460, height=280)
        resultado_box.pack(pady=10)

        def buscar_palabra():
            palabra = entrada_busqueda.get().strip().lower()
            resultado_box.delete("0.0", "end")
            if palabra:
                for entrada in historial_guardado:
                    if isinstance(entrada, dict):
                        if palabra in entrada["pregunta"].lower() or palabra in entrada["respuesta"].lower():
                            resultado_box.insert("end", f"🟢 {entrada['pregunta']}\n{entrada['respuesta']}\n\n")

        boton_realizar_busqueda = tk.CTkButton(ventana_busqueda, text="Buscar", command=buscar_palabra)
        boton_realizar_busqueda.pack(pady=5)

    # --- BOTÓN PARA RESUMIR EL CHAT ---
    def resumir_conversacion():
        seleccion = pregunta_actual.get()
        if not seleccion:
            mostrar_mensaje("Selecciona una pregunta del historial para resumirla.", alineado_izq=True)
            return

        for entrada in historial_guardado:
            if isinstance(entrada, dict) and entrada.get("pregunta") == seleccion:
                texto = f"Tú: {entrada['pregunta']}\nChatBot: {entrada['respuesta']}\n"
                resumen = API.chat("Resume esta conversación:\n" + texto)
                mostrar_mensaje("Resumen de la conversación:", alineado_izq=True)
                mostrar_mensaje(resumen, alineado_izq=True)
                break

    # --- AGREGAR BOTONES AL FINAL ---
    boton_buscar = tk.CTkButton(ventana_chat, text="🔍 Buscar en historial", fg_color="#35b46d", command=abrir_ventana_busqueda, width=200)
    boton_buscar.place(x=330, y=670)

    boton_resumen = tk.CTkButton(ventana_chat, text="📝 Resumir", fg_color="#35b46d", command=resumir_conversacion, width=200)
    boton_resumen.place(x=550, y=670)

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
