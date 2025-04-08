import json # Se importa la librería json para hacer el formato.
import requests  # Se importa la librería requests para hacer solicitudes HTTP.

# URL del servidor PHP que maneja la lógica del chatbot.
URL_PHP  = "https://leoviquez.com/IproyectoIntro/"

# Lista que almacena el historial de la conversación.
conversacion = [
    {"role": "system", "content": "Eres un asistente útil y conversacional."}
]

def chat_con_php(mensaje:str)->str:
    """
    Envía el historial de la conversación a un servidor PHP y recibe la respuesta del asistente.
    
    Args:
        mensaje (str): Entrada del usuario que será enviada al servidor.

    Returns:
        str: Respuesta generada por el asistente en el servidor PHP o mensaje de error.
    """

    with open("usuario.txt", "r", encoding="utf-8") as archivo_usuario: # Se actualiza el usuario.
            user = archivo_usuario.read().strip()

    # Se añade el mensaje del usuario al historial de la conversación.
    conversacion.append({"role": "user", "content": mensaje})

    try: # Se intenta hacer la respuesta de ChatGPT 
        # Se envía una solicitud POST al servidor PHP con el historial de conversación en formato JSON.
        respuesta = requests.post(URL_PHP, json={"messages": conversacion})
        
        # Se intenta convertir la respuesta en formato JSON.
        respuestaJson = respuesta.json()
        
        # Extrae el contenido de la respuesta generada por el asistente.
        mensajeRespuesta = respuestaJson["choices"][0]["message"]["content"]
        
        # Se añade la respuesta del asistente al historial de la conversación.
        conversacion.append({"role": "assistant", "content": mensajeRespuesta})
        
        with open(f"{user}_conversaciones.txt", "r", encoding="utf-8") as archivoUsuario: #Recupero la lista para agregar el chat
            listaArchivo = json.load(archivoUsuario)
            listaArchivo.append([conversacion])

        with open(f"{user}_conversaciones.txt", "w", encoding="utf-8") as archivoUsuario: #Actualiso el archivo de historial
            json.dump(listaArchivo, archivoUsuario, indent=4)

        return mensajeRespuesta  # Se retorna el mensaje de respuesta del asistente.
    
    except Exception as e:
        # En caso de error (por ejemplo, problemas de conexión), se devuelve un mensaje de error.
        return f"Error al conectar con el servidor: {e}"

# Ciclo de conversación donde el usuario puede interactuar con el asistente hasta que escriba 'salir'.
def chat(mensaje:str)->str:
    """Funciona de intermediario para poder verificar problemas durante la rpogramación.

    Args:
        mensaje (str): Mensaje del usuario

    Returns:
        str: Respuesta del chat
    """

    # Se envía el mensaje del usuario al servidor PHP y se recibe la respuesta.
    respuesta = chat_con_php(mensaje)

    # Se muestra la respuesta en la terminal.
    return(respuesta)
