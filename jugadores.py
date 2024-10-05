# En este archivo tenemos las clases que representan jugadores
import pickle, random

class Random():
	def __init__(self, juego):
		self.juego = juego  # Referencia a una instancia de Snake

	def jugar(self):
		juego_terminado = False  # Controla si el juego ha terminado
		while not juego_terminado:
			# Elige una acción aleatoria: 0 (recto), 1 (izquierda), 2 (derecha)
			accion = random.choice([0, 1, 2])

			# Realiza el movimiento y obtiene el nuevo estado del juego
			estado_nuevo, recompenza, juego_terminado = self.juego.step(accion)

			# Renderizar el juego después de cada paso
			self.juego.render()

			# Controla la velocidad del juego (FPS)
			self.juego.clock.tick(10)  # Ajusta a la velocidad deseada

class IA():
	def __init__(self, juego):
		self.juego = juego
		self.path = None
		self.Q = {}

		### Completar

	def set_path(self, path):
		self.path = path

	# Juega al juego hasta que este termine, cada vez que mueve (en cada step) decide cual es la mejor accion segun el diccionario Q.
	def jugar(self):
		### Completar
		pass

	# Juega el juego muchas veces y en cada vez completa la informacion de la tabla Q, en base al aprendizaje observado.
	def entrenar(self):
		### Completar
		pass

	def save(self):
		if self.path is not None:
			with open(self.path, 'wb') as f:
				pickle.dump(self.Q, f, protocol=pickle.HIGHEST_PROTOCOL)

	def load(self):
		if self.path is not None:
			with open(self.path, 'rb') as f:
				self.Q = pickle.load(f)