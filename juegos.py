import pygame, sys, random
from pygame.math import Vector2

class Snake():
    def __init__(self, tamano):
        pygame.init()
        self.tamano = tamano  # Número de celdas en el tablero
        self.cell_size = 30   # Tamaño de cada celda en píxeles
        self.screen = pygame.display.set_mode((self.tamano * self.cell_size, self.tamano * self.cell_size))
        self.clock = pygame.time.Clock()

        # Cargar imágenes de la cabeza
        self.snake_head_imgs = {
            "up": pygame.image.load('images/head_up.png'),
            "down": pygame.image.load('images/head_down.png'),
            "left": pygame.image.load('images/head_left.png'),
            "right": pygame.image.load('images/head_right.png')
        }

        # Cargar imágenes del cuerpo
        self.snake_body_imgs = {
            "vertical": pygame.image.load('images/body_vertical.png'),
            "horizontal": pygame.image.load('images/body_horizontal.png'),
            "curve_ur": pygame.image.load('images/body_tr.png'),
            "curve_ul": pygame.image.load('images/body_tl.png'),
            "curve_dr": pygame.image.load('images/body_br.png'),
            "curve_dl": pygame.image.load('images/body_bl.png')
        }

        # Cargar imágenes de la cola
        self.snake_tail_imgs = {
            "up": pygame.image.load('images/tail_up.png'),
            "down": pygame.image.load('images/tail_down.png'),
            "left": pygame.image.load('images/tail_left.png'),
            "right": pygame.image.load('images/tail_right.png')
        }

        # Cargar la imagen de la manzana
        self.apple_img = pygame.image.load('images/apple.png')

        # Escalar todas las imágenes
        self.scale_images()

        self.reset()

    def scale_images(self):
        # Escalar todas las imágenes a las dimensiones de los segmentos de la serpiente (en píxeles)
        for key in self.snake_head_imgs:
            self.snake_head_imgs[key] = pygame.transform.scale(self.snake_head_imgs[key], (self.cell_size, self.cell_size))
        for key in self.snake_body_imgs:
            self.snake_body_imgs[key] = pygame.transform.scale(self.snake_body_imgs[key], (self.cell_size, self.cell_size))
        for key in self.snake_tail_imgs:
            self.snake_tail_imgs[key] = pygame.transform.scale(self.snake_tail_imgs[key], (self.cell_size, self.cell_size))
        
        # Escalar la imagen de la manzana al tamaño de una celda
        self.apple_img = pygame.transform.scale(self.apple_img, (self.cell_size, self.cell_size))

    def reset(self):
        # Inicializar serpiente en una posición central y dirección derecha
        self.serpiente = [Vector2(self.tamano // 2, self.tamano // 2)]
        self.direccion = Vector2(1, 0)  # Se mueve hacia la derecha
        self.direccion_anterior = self.direccion  # Para evitar giros opuestos
        self.fruta = self.generar_fruta()

    def generar_fruta(self):
        while True:
            fruta_pos = Vector2(random.randint(0, self.tamano - 1), random.randint(0, self.tamano - 1))
            if fruta_pos not in self.serpiente:
                return fruta_pos

    def run_game(self):
        while True:
            self.handle_events()
            self.step()  # Ejecuta un paso del juego
            self.render()
            self.clock.tick(10)  # Mantener la velocidad constante

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def step(self, accion=0):
        assert accion in {0, 1, 2}, "Acción inválida"

        # Determinar la nueva dirección (en celdas, no píxeles)
        if accion == 1:  # Girar a la izquierda
            nueva_direccion = Vector2(-self.direccion.y, self.direccion.x)
        elif accion == 2:  # Girar a la derecha
            nueva_direccion = Vector2(self.direccion.y, -self.direccion.x)
        else:
            nueva_direccion = self.direccion

        # Evitar giro hacia la dirección opuesta
        if nueva_direccion + self.direccion_anterior != Vector2(0, 0):
            self.direccion = nueva_direccion

        # Mover la serpiente
        nueva_cabeza = self.serpiente[0] + self.direccion

        # Verificar si la nueva cabeza está dentro de los límites (en celdas)
        if not (0 <= nueva_cabeza.x < self.tamano and 0 <= nueva_cabeza.y < self.tamano):
            print(f"Colisión con la pared en posición: {nueva_cabeza}")
            return None, -1, True  # Colisión con pared

        # Verificar colisión con el cuerpo (antes de mover)
        if nueva_cabeza in self.serpiente:
            print("Colisión con el cuerpo")
            return None, -1, True  # Colisión con el cuerpo

        # Mover la serpiente
        self.serpiente.insert(0, nueva_cabeza)  # Agregar nueva cabeza al inicio

        # Verificar si comió una fruta
        if nueva_cabeza == self.fruta:
            self.fruta = self.generar_fruta()  # Generar nueva fruta
            return None, 1, False  # Comió fruta
        else:
            self.serpiente.pop()  # Eliminar el último segmento si no ha comido
            return None, 0, False  # No pasó nada

        # Actualizar la última dirección válida
        self.direccion_anterior = self.direccion  

    def render(self):
        try:
            
            # Dibujar el fondo con la grilla
            self.draw_grid()
            
            # Dibujar la serpiente
            for index, block in enumerate(self.serpiente):
                x_pos = int(block.x * self.cell_size)  # Convertir de celdas a píxeles
                y_pos = int(block.y * self.cell_size)  # Convertir de celdas a píxeles
                block_rect = pygame.Rect(x_pos, y_pos, self.cell_size, self.cell_size)

                if index == 0:  # Cabeza de la serpiente
                    head_direction = self.get_head_direction()
                    self.screen.blit(self.snake_head_imgs[head_direction], block_rect)
                elif index == len(self.serpiente) - 1:  # Cola de la serpiente
                    tail_direction = self.get_tail_direction()
                    self.screen.blit(self.snake_tail_imgs[tail_direction], block_rect)
                else:  # Cuerpo de la serpiente
                    body_type = self.get_body_type(index)
                    self.screen.blit(self.snake_body_imgs[body_type], block_rect)

            # Dibujar la manzana
            fruta_x_pos = int(self.fruta.x * self.cell_size)  # Convertir la posición de la fruta a píxeles
            fruta_y_pos = int(self.fruta.y * self.cell_size)  # Convertir la posición de la fruta a píxeles
            fruta_rect = pygame.Rect(fruta_x_pos, fruta_y_pos, self.cell_size, self.cell_size)
            self.screen.blit(self.apple_img, fruta_rect)  # Dibujar la manzana en la pantalla

            pygame.display.update()

        except Exception as e:
            print(f"Error al renderizar: {e}")
            
    def draw_grid(self):
        # Colores
        color_fondo_oscuro = (167, 209, 61)  # Verde más oscuro
        color_fondo_claro = (175, 215, 70)   # Verde más claro

        for fila in range(self.tamano):
            for col in range(self.tamano):
                x_pos = col * self.cell_size
                y_pos = fila * self.cell_size
                rect = pygame.Rect(x_pos, y_pos, self.cell_size, self.cell_size)
                # Alternar los colores
                if (fila + col) % 2 == 0:
                    pygame.draw.rect(self.screen, color_fondo_claro, rect)
                else:
                    pygame.draw.rect(self.screen, color_fondo_oscuro, rect)


    def get_head_direction(self):
        # Determina la dirección de la cabeza
        if self.direccion == Vector2(0, -1):
            return "up"
        elif self.direccion == Vector2(0, 1):
            return "down"
        elif self.direccion == Vector2(-1, 0):
            return "left"
        else:
            return "right"

    def get_tail_direction(self):
        # Determina la dirección de la cola basada en los últimos dos segmentos
        tail_direction = self.serpiente[-1] - self.serpiente[-2]
        if tail_direction == Vector2(0, -1):
            return "up"
        elif tail_direction == Vector2(0, 1):
            return "down"
        elif tail_direction == Vector2(-1, 0):
            return "left"
        else:
            return "right"

    def get_body_type(self, index):
        # Determina si el cuerpo está en línea recta o en curva
        previous_segment = self.serpiente[index - 1] - self.serpiente[index]
        next_segment = self.serpiente[index + 1] - self.serpiente[index]

        if previous_segment.x == next_segment.x:
            return "vertical"
        elif previous_segment.y == next_segment.y:
            return "horizontal"
        else:
            return self.get_curve_type(previous_segment, next_segment)

    def get_curve_type(self, previous_segment, next_segment):
        # Determina el tipo de curva
        if previous_segment == Vector2(-1, 0) and next_segment == Vector2(0, 1):
            return "curve_dl"
        elif previous_segment == Vector2(0, 1) and next_segment == Vector2(-1, 0):
            return "curve_dl"
        elif previous_segment == Vector2(1, 0) and next_segment == Vector2(0, 1):
            return "curve_dr"
        elif previous_segment == Vector2(0, 1) and next_segment == Vector2(1, 0):
            return "curve_dr"
        elif previous_segment == Vector2(-1, 0) and next_segment == Vector2(0, -1):
            return "curve_ul"
        elif previous_segment == Vector2(0, -1) and next_segment == Vector2(-1, 0):
            return "curve_ul"
        elif previous_segment == Vector2(1, 0) and next_segment == Vector2(0, -1):
            return "curve_ur"
        elif previous_segment == Vector2(0, -1) and next_segment == Vector2(1, 0):
            return "curve_ur"
