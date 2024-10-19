import pygame, sys, random
from pygame.math import Vector2

class Snake():
	def __init__(self, tamano):
		pygame.init()
		self.tamano = tamano
		self.screen = pygame.display.set_mode((self.tamano * 30, self.tamano * 30))
		self.clock = pygame.time.Clock()
		self.reset()

	def reset(self):
		self.serpiente = [Vector2(random.randint(0, self.tamano - 1), random.randint(0, self.tamano - 1))]
		self.direccion = Vector2(1, 0)
		self.fruta = self.generar_fruta()

	def generar_fruta(self):
		return Vector2(random.randint(0, self.tamano - 1), random.randint(0, self.tamano - 1))

	def run_game(self):
		while True:
			self.handle_events()
			self.render()
			self.clock.tick(10)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	def step(self, accion):
		assert accion in {0, 1, 2}, "Accion invalida"

		if accion == 1:
			self.direccion = Vector2(-self.direccion.y, self.direccion.x)
		elif accion == 2:
			self.direccion = Vector2(self.direccion.y, -self.direccion.x)

		self.definir_estados(accion)
		print(self.estados)

		nueva_cabeza = self.serpiente[0] + self.direccion

		if not (0 <= nueva_cabeza.x < self.tamano and 0 <= nueva_cabeza.y < self.tamano):
			return None, -1, False

		if nueva_cabeza in self.serpiente:
			return None, -1, False

		self.serpiente = [nueva_cabeza] + self.serpiente[:-1]

		if nueva_cabeza == self.fruta:
			self.serpiente.append(self.serpiente[-1])
			self.fruta = self.generar_fruta()
			return None, 1, False

		return None, 0, False
	
	def render(self):
		try:
			self.screen.fill((175, 215, 70))
			pasto = (167,209,61)
			for row in range(self.tamano * 30):
				if row % 2 == 0:
					for col in range(self.tamano * 30):
						if col % 2 == 0:
							grilla_pasto = pygame.Rect(col * self.tamano, row * self.tamano, self.tamano, self.tamano)
							pygame.draw.rect(self.screen, pasto, grilla_pasto)
				else:
					for col in range(self.tamano * 30):
						if col % 2 != 0:
							grilla_pasto = pygame.Rect(col * self.tamano, row * self.tamano, self.tamano, self.tamano)
							pygame.draw.rect(self.screen, pasto, grilla_pasto)

			for segmento in self.serpiente:
				x_pos = int(segmento.x * 30)
				y_pos = int(segmento.y * 30)
				bloque = pygame.Rect(x_pos, y_pos, 30, 30)
				pygame.draw.rect(self.screen, (0, 0, 255), bloque)  

			fruta_rect = pygame.Rect(int(self.fruta.x * 30), int(self.fruta.y * 30), 30, 30)
			pygame.draw.rect(self.screen, (255, 0, 0), fruta_rect)

			pygame.display.update()
		except Exception as e:
			print(f"Ocurrió un error al renderizar: {e}")
			pygame.quit()
			sys.exit()

	def definir_estados(self, accion):
		self.estados = []
		self.estados.extend(self.verificar_movimientos())
		self.estados.extend(self.detectar_direccion(accion))
		self.estados.extend(self.detectar_comida())
					  
		
	def morira_en_direccion(self,direccion):
		nueva_cabeza = self.serpiente[0] + direccion

		if not (0 <= nueva_cabeza.x < self.tamano and 0 <= nueva_cabeza.y < self.tamano):
			return 1
		if nueva_cabeza in self.serpiente:
			return 1
		return 0

	def calcular_direcciones(self):
		adelante = self.direccion
		izquierda = Vector2(-self.direccion.y, self.direccion.x)
		derecha = Vector2(self.direccion.y, -self.direccion.x)

		return adelante, izquierda, derecha
	
	def verificar_movimientos(self):
		adelante, izquierda, derecha = self.calcular_direcciones()
		morira_adelante = self.morira_en_direccion(adelante)
		morira_izquierda = self.morira_en_direccion(izquierda)
		morira_derecha = self.morira_en_direccion(derecha)

		return [morira_adelante, morira_izquierda, morira_derecha]

	def detectar_direccion(self, accion):
		if self.direccion == Vector2(1,0):
			return [0,1,0,0]
		elif self.direccion == Vector2(-1,0):
			return [1,0,0,0]
		elif self.direccion == Vector2(0,1):
			return [0,0,0,1]
		elif self.direccion == Vector2(0,-1):
			return [0,0,1,0]

	def detectar_comida(self):
		direccion_fruta_x = self.fruta.x - self.serpiente[0].x
		direccion_fruta_y = self.fruta.y - self.serpiente[0].y
		direccion_fruta = []
		if direccion_fruta_x < 0:
			direccion_fruta.append(1)
			direccion_fruta.append(0)
		else:
			direccion_fruta.append(0)
			direccion_fruta.append(1)
		if direccion_fruta_y < 0:
			direccion_fruta.append(1)
			direccion_fruta.append(0)
		else:
			direccion_fruta.append(0)
			direccion_fruta.append(1)
		return direccion_fruta