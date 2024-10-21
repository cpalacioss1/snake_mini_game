import pygame
import time
import random

# Inicializamos Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (213, 50, 80)
VERDE = (0, 255, 0)
AZUL = (50, 153, 213)
AMARILLO = (255, 255, 0)  # Color para la comida especial

# Dimensiones de la pantalla
ANCHO = 900
ALTO = 600

# Tamaño del bloque de la serpiente
TAMAÑO_BLOQUE = 10
VELOCIDAD = 15

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Snake - La Serpiente - creado por Cristian Palacios')

# Fuente
fuente = pygame.font.SysFont("bahnschrift", 25)

# Reloj
reloj = pygame.time.Clock()

# Función para mostrar la puntuación
def mostrar_puntuacion(puntuacion):
    valor = fuente.render("Puntuación: " + str(puntuacion), True, BLANCO)
    pantalla.blit(valor, [0, 0])

# Función para dibujar la serpiente
def dibujar_serpiente(tamaño_bloque, lista_serpiente):
    for bloque in lista_serpiente:
        pygame.draw.rect(pantalla, VERDE, [bloque[0], bloque[1], tamaño_bloque, tamaño_bloque])

# Función para mostrar el mensaje de fin de juego con el puntaje
def mensaje_final(msg, puntuacion, color):
    mensaje = fuente.render(msg, True, color)
    pantalla.blit(mensaje, [ANCHO / 6, ALTO / 3])
    puntaje_total = fuente.render("Tu puntuación total: " + str(puntuacion), True, color)
    pantalla.blit(puntaje_total, [ANCHO / 6, ALTO / 2])

# El juego principal
def juego():
    game_over = False
    game_cerrado = False

    # Posición inicial de la serpiente
    x_cabeza = ANCHO / 2
    y_cabeza = ALTO / 2

    # Movimiento
    x_cambio = 0
    y_cambio = 0

    # Lista de la serpiente y longitud inicial
    lista_serpiente = []
    longitud_serpiente = 1

    # Posición inicial de la comida
    comida_x = round(random.randrange(0, ANCHO - TAMAÑO_BLOQUE) / 10.0) * 10.0
    comida_y = round(random.randrange(0, ALTO - TAMAÑO_BLOQUE) / 10.0) * 10.0

    # Variables para la comida especial
    comida_especial_x = None
    comida_especial_y = None
    comida_especial_tiempo = 0
    comida_especial_presente = False

    while not game_over:

        while game_cerrado == True:
            pantalla.fill(NEGRO)
            mensaje_final("Oops! Presiona Q para salir o C para jugar de nuevo", longitud_serpiente - 1, ROJO)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_cerrado = False
                    if evento.key == pygame.K_c:
                        juego()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True  # Cerrar el juego cuando se haga clic en la X de la ventana
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x_cambio = -TAMAÑO_BLOQUE
                    y_cambio = 0
                elif evento.key == pygame.K_RIGHT:
                    x_cambio = TAMAÑO_BLOQUE
                    y_cambio = 0
                elif evento.key == pygame.K_UP:
                    y_cambio = -TAMAÑO_BLOQUE
                    x_cambio = 0
                elif evento.key == pygame.K_DOWN:
                    y_cambio = TAMAÑO_BLOQUE
                    x_cambio = 0

        if x_cabeza >= ANCHO or x_cabeza < 0 or y_cabeza >= ALTO or y_cabeza < 0:
            game_cerrado = True

        x_cabeza += x_cambio
        y_cabeza += y_cambio
        pantalla.fill(NEGRO)

        # Dibujar comida regular
        pygame.draw.rect(pantalla, AZUL, [comida_x, comida_y, TAMAÑO_BLOQUE, TAMAÑO_BLOQUE])

        # Ocasionalmente generar una comida especial
        if not comida_especial_presente and random.randint(0, 100) < 1:  # 1% de probabilidad de aparecer
            comida_especial_x = round(random.randrange(0, ANCHO - TAMAÑO_BLOQUE) / 10.0) * 10.0
            comida_especial_y = round(random.randrange(0, ALTO - TAMAÑO_BLOQUE) / 10.0) * 10.0
            comida_especial_presente = True
            comida_especial_tiempo = pygame.time.get_ticks()  # Marcar el tiempo de aparición

        # Mostrar la comida especial si está presente
        if comida_especial_presente:
            pygame.draw.rect(pantalla, AMARILLO, [comida_especial_x, comida_especial_y, TAMAÑO_BLOQUE, TAMAÑO_BLOQUE])

            # Si la comida especial no es consumida en 5 segundos, desaparece
            if pygame.time.get_ticks() - comida_especial_tiempo > 5000:
                comida_especial_presente = False

        # Actualizar la serpiente
        cabeza_serpiente = []
        cabeza_serpiente.append(x_cabeza)
        cabeza_serpiente.append(y_cabeza)
        lista_serpiente.append(cabeza_serpiente)
        if len(lista_serpiente) > longitud_serpiente:
            del lista_serpiente[0]

        for bloque in lista_serpiente[:-1]:
            if bloque == cabeza_serpiente:
                game_cerrado = True

        dibujar_serpiente(TAMAÑO_BLOQUE, lista_serpiente)
        mostrar_puntuacion(longitud_serpiente - 1)

        pygame.display.update()

        # Comprobar si la serpiente come la comida regular
        if x_cabeza == comida_x and y_cabeza == comida_y:
            comida_x = round(random.randrange(0, ANCHO - TAMAÑO_BLOQUE) / 10.0) * 10.0
            comida_y = round(random.randrange(0, ALTO - TAMAÑO_BLOQUE) / 10.0) * 10.0
            longitud_serpiente += 1

        # Comprobar si la serpiente come la comida especial
        if comida_especial_presente and x_cabeza == comida_especial_x and y_cabeza == comida_especial_y:
            comida_especial_presente = False
            longitud_serpiente += 3  # La comida especial vale 3 puntos

        reloj.tick(VELOCIDAD)

    pygame.quit()
    quit()

juego()
