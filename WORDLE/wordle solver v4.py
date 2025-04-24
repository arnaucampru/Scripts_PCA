import random  # Para seleccionar palabras aleatorias
import unicodedata  # Para manejar caracteres con acentos

# Función para eliminar acentos de una palabra
def quitar_acentos(palabra):
    return ''.join((c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn'))

# Función para cargar las palabras del diccionario desde un archivo de texto
def cargar_diccionario(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        # Leer cada línea del archivo, quitar espacios, convertir a minúsculas y eliminar acentos
        # Solo se mantienen palabras de 5 letras
        palabras = [quitar_acentos(linea.strip().lower()) for linea in archivo if len(linea.strip()) == 5]
    return palabras

# Función para recibir feedback del usuario sobre el intento actual
def obtener_feedback(guess):
    while True:
        feedback = input("Feedback (B/M/C): ").strip().upper()  # Solicitar feedback y convertirlo a mayúsculas
        # Validar que el feedback sea de 5 caracteres y solo contenga 'B', 'M' o 'C'
        if len(feedback) == 5 and all(f in ['B', 'M', 'C'] for f in feedback):
            return feedback
        print("Feedback inválido. Usa exactamente 5 letras (B, M o C)")

# Función para filtrar palabras basadas en el feedback recibido
def filtrar_palabras(posibles_palabras, guess, feedback):
    palabras_filtradas = []  # Lista donde guardaremos las palabras válidas tras el filtrado

    for palabra in posibles_palabras:
        match = True  # Bandera que indica si la palabra sigue siendo válida
        cuenta_palabra = {letra: palabra.count(letra) for letra in set(palabra)}  # Conteo de letras en la palabra

        # Procesar 'B' (letra correcta y en la posición correcta)
        for i in range(5):
            if feedback[i] == 'B':
                if palabra[i] != guess[i]:  # Si la letra no está en la posición correcta, descartamos la palabra
                    match = False
                    break
                cuenta_palabra[guess[i]] -= 1  # Reducimos el conteo de esta letra en la palabra

        # Procesar 'C' (letra correcta pero en la posición incorrecta)
        for i in range(5):
            if feedback[i] == 'C':
                # La letra debe estar en la palabra pero en otra posición
                if guess[i] not in palabra or palabra[i] == guess[i] or cuenta_palabra[guess[i]] <= 0:
                    match = False
                    break
                cuenta_palabra[guess[i]] -= 1  # Reducimos el conteo de esta letra en la palabra

        # Procesar 'M' (letra no está en la palabra)
        for i in range(5):
            if feedback[i] == 'M':
                if guess[i] in palabra and cuenta_palabra[guess[i]] > 0:
                    match = False
                    break

        if match:
            palabras_filtradas.append(palabra)  # Si la palabra cumple con las reglas, la añadimos a la lista

    return palabras_filtradas  # Retornamos la lista de palabras filtradas

# Función principal que resuelve Wordle
def resolver_wordle(ruta_diccionario):
    palabras = cargar_diccionario(ruta_diccionario)  # Cargar todas las palabras del diccionario
    posibles_palabras = palabras.copy()  # Crear una copia de la lista de palabras

    # Permitir al usuario elegir la palabra inicial
    guess = input("Palabra inicial: ").strip().lower()  # Leer la palabra inicial ingresada por el usuario
    if len(guess) != 5 or not guess.isalpha():  # Si la palabra es inválida, se elige una aleatoria
        print("Palabra inicial inválida. Se seleccionará una aleatoria.")
        guess = random.choice(posibles_palabras)

    for intento in range(1, 7):  # Wordle permite un máximo de 6 intentos
        print(f"\nIntento {intento}: {guess.upper()}")

        feedback = obtener_feedback(guess)  # Obtener feedback del usuario

        if feedback == 'BBBBB':  # Si todas las letras son correctas y están en su posición, hemos ganado
            print(f"¡Palabra correcta! {intento} intentos")
            return

        posibles_palabras = filtrar_palabras(posibles_palabras, guess, feedback)  # Filtrar palabras

        if not posibles_palabras:  # Si no quedan palabras posibles, algo salió mal
            print("No se encontraron palabras posibles")
            return

        guess = random.choice(posibles_palabras)  # Seleccionar una nueva palabra de las posibles

    print("No se encontró la palabra...")  # Si no se adivinó en 6 intentos, el bot falla

# Ruta al diccionario de palabras
ruta_diccionario = 'diccionario.txt'

# Ejecutar el solucionador
resolver_wordle(ruta_diccionario)