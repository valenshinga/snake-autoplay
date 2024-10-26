# En este archivo tenemos las clases que representan jugadores
import json, random
import pygame, sys, random

class Random():
	def __init__(self, juego):
		self.juego = juego 

	def jugar(self):
		juego_terminado = False  
		while not juego_terminado:
			accion = random.choice([0, 1, 2])

			estado_nuevo, recompenza, juego_terminado = self.juego.step(accion)

			self.juego.render()

			self.juego.clock.tick(10)

class IA():
	def __init__(self, juego):
		self.juego = juego
		self.path = None
		self.Q = {}
		self.entrenando = False
		self.reintentos = 10
		self.estado_actual = ""

	def set_path(self, path):
		self.path = path

	def jugar(self):
		juego_terminado = False
		if (self.entrenando):			
			for _ in range(self.reintentos):
				self.juego.reset() 
				juego_terminado = False
				while not juego_terminado:
					self.estado = self.obtener_estado()
					accion = self.seleccionar_accion()

					estado, recompenza, juego_terminado = self.juego.step(accion)

					self.actualizar_Q(estado, recompenza, accion)

					self.juego.render()

					#Esto es por si se queda en un loop loco
					events = pygame.event.get()
					for event in events:
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_r: #Apretar la tecla R para reiniciar el juego. No disminuye intentos
								self.juego.reset()

					self.juego.clock.tick(10)
			print(self.Q)
			self.save()
		else:
			while not juego_terminado:
				accion = self.seleccionar_accion()

				estado, recompenza, juego_terminado = self.juego.step(accion)

				self.juego.render()

				self.juego.clock.tick(10)

	def entrenar(self):
		self.entrenando = True
		self.load()
		print(self.Q)

	def save(self):
		if self.path is not None:
			with open(self.path, 'w') as f: 
				json.dump(self.Q, f) 

	def load(self):
		if self.path is not None:
			with open(self.path, 'r') as f:  
				self.Q = json.load(f) 

	def seleccionar_accion(self):
		estado = self.obtener_estado()
		if estado != "[]":
			if estado not in self.Q:
				self.Q[estado] = [0, 0, 0] 
		else:
			return random.choice([0, 1, 2])

		indices_cero = [i for i, valor in enumerate(self.Q[estado]) if valor == 0]
		if indices_cero:
			return random.choice(indices_cero)
		return self.Q[estado].index(max(self.Q[estado]))

	def actualizar_Q(self, estado, recompenza, accion):
		estado_actual = self.estado
		estado_siguiente = estado
		if estado_actual not in self.Q:
			self.Q[estado_actual] = [0, 0, 0]
		if estado_siguiente not in self.Q:
			self.Q[estado_siguiente] = [0, 0, 0]

		max_valor_siguiente = max(self.Q[estado_siguiente])
		self.Q[estado_actual][accion] += 0.05 * (recompenza - self.Q[estado_actual][accion] + max_valor_siguiente)

	def obtener_estado(self):
		return self.juego.estados
