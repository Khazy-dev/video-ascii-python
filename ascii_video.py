import cv2 
import sys 
import time 
import shutil


# Cadena de caracteres ASCII que se usarán para representar los píxeles / ASCII character string that will be used to represent the pixels.
# Los caracteres más simples representan tonos más oscuros o suaves, / Simpler characters represent darker or softer tones.
# y los más densos representan tonos más intensos / and denser characters represent more intense tones.
ASCII_CHARS = " .,:-=+*#%@"


# Define el ancho / defines the width
WIDTH = 80

# Define el alto / defines the height
HEIGHT = 150


# Esta función convierte un frame del video en una versión ASCII 
# Recibe el frame original y opcionalmente un ancho y alto
def frame_to_ascii_fixed(frame, width=WIDTH, height=HEIGHT):

    # Convierte el frame de color a escala de grises
    # Esto simplifica la imagen a valores de brillo solamente
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Redimensiona la imagen al tamaño definido para mostrarla en la terminal
    resized = cv2.resize(gray, (width, height))

    # Calcula una escala para convertir los valores de píxel (0 a 255)
    # en posiciones dentro de la cadena ASCII_CHARS
    scale = len(ASCII_CHARS) / 256

    # Lista vacía donde se guardarán las líneas ASCII ya convertidas
    lines = []

    # Recorre cada fila de la imagen redimensionada
    for row in resized:

        # Convierte cada píxel de la fila en un carácter ASCII
        line = "".join(ASCII_CHARS[min(int(p * scale), len(ASCII_CHARS) - 1)] for p in row)

        # Agrega espacios al final si hace falta para que todas las líneas
        # tengan el mismo ancho y no se deforme la imagen en la terminal
        lines.append(line.ljust(width))  
    # Devuelve la lista completa de líneas en formato ASCII
    return lines


# Esta función abre un video y lo reproduce como animación ASCII en la terminal
def play_ascii_video(video_path):

    # Intenta abrir el archivo de video usando la ruta recibida
    cap = cv2.VideoCapture(video_path)

    # Verifica si el video se abrió correctamente
    if not cap.isOpened():

        # en caso que no
        print("No se pudo abrir el video.")

        # Sale de la función para evitar errores posteriores
        return

    # Obtiene los FPS (frames por segundo) del video original
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calcula cuánto tiempo debe esperar entre frames
    # Si fps no existe o es 0, usa 0.033 segundos como valor por defecto
    frame_time = 1.5 / fps if fps > 0 else 0.033

    # Obtiene el tamaño actual de la terminal
    # Si no puede detectarlo, usa 80 columnas y 24 filas por defecto
    term = shutil.get_terminal_size((80, 24))

    # Ajusta el ancho final para que no se pase del ancho de la terminal
    width = min(WIDTH, term.columns - 1)   # evita wrap

    # Ajusta el alto final para que no se salga verticalmente de la terminal
    height = min(HEIGHT, term.lines - 1)

    # Limpia la terminal una sola vez al inicio y mueve el cursor arriba a la izquierda
    print("\x1b[2J\x1b[H", end="")  # limpia una vez

    next_time = time.perf_counter()

    # Bucle infinito para leer y mostrar todos los frames del video
    while True:

        # Lee el siguiente frame del video
        ret, frame = cap.read()

        # Si no se pudo leer más frames, termina el bucle
        if not ret:
            break

        # Convierte el frame actual en líneas ASCII
        lines = frame_to_ascii_fixed(frame, width, height)

        # Mueve el cursor al inicio de la terminal para sobrescribir el frame anterior
        sys.stdout.write("\x1b[H")

        # Recorre cada línea ASCII generada
        for line in lines:

            # \x1b[K limpia lo que sobre en esa línea para evitar residuos visuales
            sys.stdout.write(line + "\x1b[K\n")  # limpia resto de línea

        # Fuerza la impresión inmediata en pantalla
        sys.stdout.flush()

        # Calcula el momento exacto en el que debe mostrarse el siguiente frame
        next_time += frame_time

        # Calcula cuánto tiempo falta para llegar a ese momento
        sleep = next_time - time.perf_counter()

        # Si todavía falta tiempo, espera para mantener la velocidad del video
        if sleep > 0:
            time.sleep(sleep)

    # Libera el archivo de video cuando termina la reproducción
    cap.release()


if __name__ == "__main__":

    # Llama a la función principal y reproduce el archivo con x nombre"
    play_ascii_video("video.mp4")