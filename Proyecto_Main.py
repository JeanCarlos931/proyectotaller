import json
import customtkinter as tk
from PIL import Image
import os
from datetime import datetime
import API

tk.set_default_color_theme("green") #pone un color al clickar los objetos en verde

def guardar_usuario_actual(user:str)->None:
    """Guarda el usuario actual que se está ejecutando en un documento aparte.

    Args:
        user (_type_): Usuario actual.
    """
    with open("usuario.txt", "w", encoding="utf-8") as archivo: #Crea un archivo con el usuario activo
        archivo.write(user)

def login():
    """Usa la interfaz gráfica de tkinter para solicitar el usuario y verificar si existe el archivo
    """
    user = entry_Login.get().lower()    #Solicita el usuario.
    if not user: #Si no escribe un usuario entonces escribe que lo ingrese
        mensaje.configure(text="Por favor, ingresa un nombre de usuario para iniciar sesión.", text_color="red") 
        return

    try: #Intenta encontrar el archivo asociado al usuario
        with open(f"{user}_conversaciones.txt", "r", encoding="utf-8") as archivo:
            global historial_Guardado  # Hacerlo global para poder usarlo en otras funciones
            historial_Guardado = json.load(archivo)
            mensaje.configure(text=f"Inicio de sesión exitoso. Bienvenido, {user}.", text_color="green")
    except FileNotFoundError: #Si no existe el archivo solicita que se registre
        mensaje.configure(text="El usuario no está registrado.", text_color="red")
        return

    ventana.withdraw() #Crea una ventana
    ventana_Chat = tk.CTk() #Llama al import para crear un tk
    ventana_Chat.geometry("1000x700") #Este es el tamaño de la ventana que se va a crear
    ventana_Chat.title(f"Sesión de {user}") #Muestra la seleccion del usuario seleccionado

    # Panel izquierdo: historial
    marco_Historial = tk.CTkScrollableFrame(ventana_Chat, width=300, height=660) #Crea un marco para moverse en la ventana un scroll basicamente
    marco_Historial.place(x=10, y=20)

    tk.CTkLabel(marco_Historial, text="Historial", font=("Arial", 18, "bold")).pack(pady=10) #Es el apartado donde se escribe arriba "historial"

    # Panel derecho: chat actual
    marco_Chat = tk.CTkScrollableFrame(ventana_Chat, width=650, height=600)
    marco_Chat.place(x=330, y=20)

    def mostrar_mensaje(texto, alineado_izq=True):
        """_mostrar mensaje_

        Args:
            texto (int): lo que se escribe en la caja de texto y se le pregunta a la IA
            alineado_izq (bool, optional): Es para aliniarlo hacia la izquierda. Defaults to True.
        """
        burbuja = tk.CTkLabel(marco_Chat, text=texto, anchor="w" if alineado_izq else "e", justify="left", fg_color="#2a2a2a" if alineado_izq else "#1f6aa5", text_color="white", corner_radius=12, width=500, wraplength=500)
        # Crear una "burbuja" de mensaje dentro del marco del chat.
        # Esta burbuja puede alinearse a la izquierda (usuario) o derecha (chatbot), según el parámetro 'alineado_izq'.
        burbuja.pack(padx=10, pady=(5, 0), anchor="w" if alineado_izq else "e")

    # Función 
    def mostrar_fecha(fecha):
        """Se usa para mostrar la fecha

        Args:
            fecha (_type_): La fecha actual del documento que se calcula fuera de la función
        """
        label_Fecha = tk.CTkLabel(marco_Chat, text=fecha, font=("Arial", 10), text_color="#aaaaaa")
        label_Fecha.pack(pady=(0, 5))

    chat_Actual = tk.StringVar()  # Guardará la pregunta seleccionada
    
    def cargar_chat(chat_seleccionado):
        """Función para cargar el chat cuando se hace clic en una pregunta del historial

        Args:
            chat_seleccionado (_type_): 
        """
        chat_Actual.set(chat_seleccionado)  # Guardamos la selección

        # Limpiar el área de chat antes de cargar nuevos mensajes
        for widget in marco_Chat.winfo_children():
            widget.destroy()

        for entrada in historial_Guardado:
            if isinstance(entrada, dict) and entrada.get("pregunta") == chat_seleccionado:
                mostrar_mensaje(f"Tú: {entrada['pregunta']}", alineado_izq=False)
                mostrar_fecha(entrada["timestamp"])
                mostrar_mensaje(f"ChatBot: {entrada['respuesta']}", alineado_izq=True)
                mostrar_fecha(entrada["timestamp"])
                break
        # Limpiar el área de chat antes de cargar nuevos mensajes
        for widget in marco_Chat.winfo_children():
            widget.destroy()

        # Buscar la pregunta seleccionada en el historial guardado
        for entrada in historial_Guardado:
            if isinstance(entrada, dict):  # Verifica que la entrada sea un diccionario
                if entrada.get("pregunta") == chat_seleccionado:  # Usar .get() para evitar KeyError
                    # Mostrar la pregunta y la respuesta en el chat
                    mostrar_mensaje(f"Tú: {entrada['pregunta']}", alineado_izq=False)
                    mostrar_fecha(entrada["timestamp"])
                    mostrar_mensaje(f"ChatBot: {entrada['respuesta']}", alineado_izq=True)
                    mostrar_fecha(entrada["timestamp"])
                    break
            
    # Mostrar preguntas como botones en el historial
    for entrada in historial_Guardado:
        if isinstance(entrada, dict):  # Asegura que cada entrada sea un diccionario (pregunta/respuesta)
            hora = entrada.get("timestamp", "")[-5:] # Toma solo los últimos 5 caracteres (la hora)
            btn = tk.CTkButton(marco_Historial, text=f"{entrada['pregunta']} ({hora})", anchor="w", width=270, command=lambda p=entrada["pregunta"]: cargar_chat(p))
            # Crea un botón con la pregunta y la hora y cuando se hace clic, se carga el chat de esa pregunta
            btn.pack(padx=10, pady=5, anchor="w") # Muestra el botón en el marco del historial

# --- CAJA PARA ESCRIBIR MENSAJES AL CHATBOT ---
    caja_Mensaje = tk.CTkEntry(ventana_Chat, width=500)
    caja_Mensaje.place(x=330, y=630) # Posición en la ventana del chat


    def enviar():
        """Función para enviar mensaje y obtener respuesta de la IA
        """
        texto = caja_Mensaje.get().strip()# Toma el texto y elimina espacios
        if texto:
            mostrar_mensaje(f"Tú: {texto}", alineado_izq=False)# Muestra tu mensaje en pantalla
            caja_Mensaje.delete(0, "end")# Limpia la caja

            Mensaje_respuesta = API.chat(texto) # Envía el texto a la IA y recibe respuesta
            if Mensaje_respuesta:
                mostrar_mensaje(f"ChatBot: {Mensaje_respuesta}", alineado_izq=True) # Muestra respuesta

                # Guarda esta nueva pregunta/respuesta en historial
                nueva_Entrada = {
                    "pregunta": texto,
                    "respuesta": Mensaje_respuesta,
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M") # Fecha y hora actual
                }

                # Agregar la nueva entrada al historial_guardado
                historial_Guardado.append(nueva_Entrada)

                # Guarda el historial en archivo (nombre del archivo depende del usuario)
                with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as archivo:
                    json.dump(historial_Guardado, archivo, indent=4)

                # Crea botón nuevo con esa pregunta
                hora = nueva_Entrada["timestamp"][-5:]
                btn = tk.CTkButton(marco_Historial, text=f"{texto} ({hora})", anchor="w", width=270,command=lambda p=texto: cargar_chat(p))
                btn.pack(padx=10, pady=5, anchor="w")

            caja_Mensaje.delete(0, "end") # Borra lo escrito

# Botón para enviar el mensaje
    boton_enviar = tk.CTkButton(ventana_Chat, text="Enviar", command=enviar, width=100)
    boton_enviar.place(x=840, y=630)

# Botón para cerrar el chat y volver al menú principal 
    def cerrar_chat():
        ventana_Chat.destroy() # Cierra la ventana del chat
        ventana.deiconify() # Muestra la ventana principal

    boton_volver = tk.CTkButton(ventana_Chat, text="Volver", command=cerrar_chat)
    boton_volver.place(x=10, y=10)

# Función para abrir una ventana y buscar palabras en el historial
    def abrir_ventana_busqueda():
        ventana_Busqueda = tk.CTkToplevel(ventana_Chat) # Nueva ventana encima de la principal
        ventana_Busqueda.title("Buscar en historial")
        ventana_Busqueda.geometry("500x400")
        ventana_Busqueda.configure(fg_color="#666666")

# Entrada de texto para escribir la palabra que se quiere buscar
        entrada_Busqueda = tk.CTkEntry(ventana_Busqueda, width=300, placeholder_text="Escribe una palabra clave")
        entrada_Busqueda.pack(pady=10)

# Área donde se mostrarán los resultados encontrados
        resultado_Box = tk.CTkTextbox(ventana_Busqueda, width=460, height=280)
        resultado_Box.pack(pady=10)

# Función interna para buscar la palabra escrita en el historial
        def buscar_palabra():
            palabra = entrada_Busqueda.get().strip().lower()
            resultado_Box.delete("0.0", "end") # Limpia los resultados anteriores
            if palabra:
                for entrada in historial_Guardado:
                    if isinstance(entrada, dict):
                        if palabra in entrada["pregunta"].lower() or palabra in entrada["respuesta"].lower():
                            resultado_Box.insert("end", f"{entrada['pregunta']}\n{entrada['respuesta']}\n\n")

        # Botón que ejecuta la búsqueda
        boton_Realizar_busqueda = tk.CTkButton(ventana_Busqueda, text="Buscar", command=buscar_palabra)
        boton_Realizar_busqueda.pack(pady=5)

    
    def resumir_conversacion():
        """Función para resumir una conversación específica del historial
        """
        seleccion = chat_Actual.get() # Obtiene la pregunta seleccionada en el historial
        if not seleccion:
            mostrar_mensaje("Selecciona una pregunta del historial para resumirla.", alineado_izq=True)
            return

        # Busca la entrada correspondiente y la resume
        for entrada in historial_Guardado:
            if isinstance(entrada, dict) and entrada.get("pregunta") == seleccion:
                texto = f"Tú: {entrada['pregunta']}\nChatBot: {entrada['respuesta']}\n"
                resumen = API.chat("Resume esta conversación en 50 palabras:\n" + texto)
                mostrar_mensaje("Resumen de la conversación en 50 palabras:", alineado_izq=True)
                mostrar_mensaje(resumen, alineado_izq=True)
                break

# Botones de la parte inferior: buscar y resumir
    boton_buscar = tk.CTkButton(ventana_Chat, text="Buscar en historial", fg_color="#35b46d", command=abrir_ventana_busqueda, width=200)
    boton_buscar.place(x=330, y=670)

    boton_Resumen = tk.CTkButton(ventana_Chat, text="Resumir", fg_color="#35b46d", command=resumir_conversacion, width=200)
    boton_Resumen.place(x=550, y=670)

    ventana_Chat.mainloop()

# Registro de usuario nuevo
def register():
    user = entry_Register.get().lower()  # Toma el nombre ingresado en minúsculas
    if not user:
        mensaje.configure(text="Por favor, ingresa un nombre de usuario para registrarte.", text_color="red")
        return

    if os.path.exists(f"{user}_conversaciones.txt"):
        mensaje.configure(text="El usuario ya está registrado.", text_color="orange")
        return

# Crea un archivo vacío con el nombre del usuario
    with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as archivo:
        json.dump([user], archivo, indent=4)

    guardar_usuario_actual(user) # Guarda el nombre como usuario actual
    mensaje.configure(text="Usuario registrado correctamente.", text_color="green")

# Interfaz principal
ventana = tk.CTk()
ventana.geometry("700x700") # Tamaño de la ventana

# Cargar y mostrar imagen
ruta_Imagen = "TheBurger_IA.png"
dark_Image = Image.open(ruta_Imagen)
my_Image = tk.CTkImage(light_image=dark_Image, size=(370, 370))

# Títulos de bienvenida
image_Label = tk.CTkLabel(ventana, image=my_Image, text="")
image_Label.place(x=360, y=380)

titulo = tk.CTkLabel(ventana, text="Bienvenido a la IA Theburger", font=("Fixedsys", 30, "bold"))
titulo.place(x=150, y=60)

titulo2 = tk.CTkLabel(ventana, text="¿En qué puedo ayudarte?", font=("Helvetica", 20, "bold"))
titulo2.place(x=150, y=120)

# Campo para iniciar sesión
entry_Login = tk.CTkEntry(ventana, width=300)
entry_Login.place(x=150, y=220)

btn_Login = tk.CTkButton(ventana, text="Iniciar Sesión", command=login, width=300, fg_color="#FD8F31")
btn_Login.place(x=150, y=250)

# Campo para registrarse
entry_Register = tk.CTkEntry(ventana, width=300)
entry_Register.place(x=150, y=320)

btn_Register = tk.CTkButton(ventana, text="Registrarse", command=register, width=300, fg_color="#FD8F31")
btn_Register.place(x=150, y=350)

# Mensaje informativo para errores o avisos
mensaje = tk.CTkLabel(ventana, text="", font=("Helvetica", 16))
mensaje.place(x=150, y=400)

ventana.mainloop() #Bucle de la ventana
