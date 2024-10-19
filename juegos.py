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

		nueva_cabeza = self.serpiente[0] + self.direccion

		if not (0 <= nueva_cabeza.x < self.tamano and 0 <= nueva_cabeza.y < self.tamano):
			return None, -1, True

		if nueva_cabeza in self.serpiente:
			return None, -1, True

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
