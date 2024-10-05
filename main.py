import sys
from juegos import Snake
from jugadores import Random, IA

JUGADORES_PERMITIDOS = {"ia": IA, "random": Random}

def print_help():
    print("Como correr el script: \n")
    print("\t python main.py random si ./train.json")

if __name__ == "__main__":
    try:
        tipo_jugador = sys.argv[1].lower()  # Argumento para el tipo de jugador
        entrenar     = sys.argv[2].lower()  # Si el agente debe ser entrenado
        file_path    = sys.argv[3]          # Ruta al archivo de entrenamiento
 
    except Exception:
        print("Error, parametros pasados de manera incorrecta")
        print_help()
        sys.exit()

    juego = Snake(16)
    if tipo_jugador in JUGADORES_PERMITIDOS:
        jugador = JUGADORES_PERMITIDOS[tipo_jugador](juego)
    else:
        raise Exception("Nombre de jugador no conocido")
 
    # Si es un jugador IA, decide si entrenar o cargar el modelo
    if tipo_jugador == "ia":
        jugador.set_path(file_path)
        if entrenar in {"si", "true"}:
            jugador.entrenar()
            jugador.save()
        else:
            jugador.load()
     
    # Ejecutar el juego con el jugador seleccionado (Random o IA)
    jugador.jugar()
