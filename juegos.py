import pygame, sys, random
from pygame.math import Vector2

class Snake():
	def __init__(self, tamano):
		pygame.init()
		self.tamano = tamano
		self.screen = pygame.display.set_mode((self.tamano * 30, self.tamano * 30))
		self.clock = pygame.time.Clock()  # Para controlar la velocidad del juego
		self.reset()

	# Reinicia el juego
	def reset(self):
		# Inicializa la serpiente con un solo segmento en una posición aleatoria
		self.serpiente = [Vector2(random.randint(0, self.tamano - 1), random.randint(0, self.tamano - 1))]
		self.direccion = Vector2(1, 0)  # Inicia moviéndose hacia la derecha
		self.fruta = self.generar_fruta()  # Genera la fruta en una posición aleatoria

	# Genera una nueva fruta en una posición aleatoria
	def generar_fruta(self):
		return Vector2(random.randint(0, self.tamano - 1), random.randint(0, self.tamano - 1))

	# Bucle principal del juego
	def run_game(self):
		while True:
			self.handle_events()  # Maneja los eventos de pygame
			self.render()         # Dibuja el juego en la pantalla
			self.clock.tick(10)   # Controla la velocidad (10 FPS)

	# Maneja eventos de pygame (incluyendo cerrar la ventana)
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	# Mueve al jugador una vez, en función a la acción realizada
	def step(self, accion):
		assert accion in {0, 1, 2}, "Accion invalida"

		# Cambia la dirección de la serpiente en base a la acción:
		if accion == 1:  # Gira a la izquierda
			self.direccion = Vector2(-self.direccion.y, self.direccion.x)
		elif accion == 2:  # Gira a la derecha
			self.direccion = Vector2(self.direccion.y, -self.direccion.x)

		# Actualiza la posición de la serpiente
		nueva_cabeza = self.serpiente[0] + self.direccion

		# Revisa si la serpiente colisiona con las paredes
		if not (0 <= nueva_cabeza.x < self.tamano and 0 <= nueva_cabeza.y < self.tamano):
			return None, -1, True  # Colisión con los bordes (juego terminado)

		# Revisa si la serpiente colisiona consigo misma
		if nueva_cabeza in self.serpiente:
			return None, -1, True  # Colisión con su cuerpo (juego terminado)

		# Mueve la serpiente
		self.serpiente = [nueva_cabeza] + self.serpiente[:-1]  # Desplaza los segmentos

		# Revisa si la serpiente ha comido la fruta
		if nueva_cabeza == self.fruta:
			self.serpiente.append(self.serpiente[-1])  # Alarga la serpiente
			self.fruta = self.generar_fruta()  # Genera una nueva fruta
			return None, 1, False  # Recompensa de 1 (fruta comida)

		# Si no colisiona ni come fruta, sigue normal
		return None, 0, False  # Recompensa de 0, juego continúa
	
	# Actualiza la información que se muestra en pantalla usando pygame
	def render(self):
		try:
			self.screen.fill((175, 215, 70))  # Fondo

			# Dibujar la serpiente
			for segmento in self.serpiente:
				x_pos = int(segmento.x * 30)
				y_pos = int(segmento.y * 30)
				bloque = pygame.Rect(x_pos, y_pos, 30, 30)
				pygame.draw.rect(self.screen, (0, 0, 255), bloque)  

			# Dibujar la fruta
			fruta_rect = pygame.Rect(int(self.fruta.x * 30), int(self.fruta.y * 30), 30, 30)
			pygame.draw.rect(self.screen, (255, 0, 0), fruta_rect)  # Fruta en rojo

			pygame.display.update()  # Actualizar la pantalla
		except Exception as e:
			print(f"Ocurrió un error al renderizar: {e}")  # Mensaje de error en caso de fallo
			pygame.quit()
			sys.exit()
