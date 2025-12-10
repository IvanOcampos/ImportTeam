import pygame
import random
import os
import sys
import cv2
import math
from moviepy import VideoFileClip
import time
from pathlib import Path

#---INICIALIZACION---
pygame.init()
pygame.mixer.init()
contador_victorias = 0 

#Pantalla principal
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TERERE QUEST")
reloj = pygame.time.Clock()
FPS = 10

#Colores
BLANCO = (255, 255, 255)
ROJO = (200, 0, 0)
NARANJA = (255,150,50)
VERDE = (0, 200, 0)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)
AZUL = (50, 50, 200)
GRIS = (80,80,80)

#---FUENTES---
#Fuente Pagina Principal
fuente_titulo = pygame.font.SysFont(None, 50)
fuente_texto = pygame.font.SysFont(None, 28)
fuente_pequena = pygame.font.SysFont(None, 24)
#Fuente Villarrica
fuente_info = pygame.font.SysFont(None, 40)
fuente_instruccion = pygame.font.SysFont(None, 80)

#---VIDEO DE LA PRIMERA PANTALLA---
video = VideoFileClip("static/pantalla_inicio.mp4")
video = video.resized((ANCHO, ALTO))
generador_frames = video.iter_frames(fps=FPS, dtype="uint8")

#---SEGUNDA PANTALLA IMAGEN---
segunda_pantalla_fondo = pygame.image.load("static/segunda_pantalla_fondo.png")
segunda_pantalla_fondo = pygame.transform.scale(segunda_pantalla_fondo, (ANCHO, ALTO))

#---CONFIGURACIÓN DE LA TERCERA PANTALLA (SELECCIÓN DE PERSONAJES)---
tercera_pantalla_fondo = pygame.image.load("static/tercera_pantalla_fondo.png")
tercera_pantalla_fondo = pygame.transform.scale(tercera_pantalla_fondo, (ANCHO, ALTO))

posiciones_jugadores = [
    (180, 300),
    (300, 300),
    (420, 300),
    (540, 300),
    (660, 300)
]
radio = 40
jugador_seleccionado = None

#Imagenes de los personajes
imagenes_jugadores = [
    pygame.image.load("static/juan_personaje.png"),
    pygame.image.load("static/Jeremy.png"),
    pygame.image.load("static/navi.png"),
    pygame.image.load("static/Cazador.png"),
    pygame.image.load("static/aquiles_lu.png")
]

#Redimensionar las imagenes de los jugadores
imagenes_jugadores = [pygame.transform.scale(img, (200, 350)) for img in imagenes_jugadores]

#---FUNCIONES---
def pantalla_inicio_1():
    """Pantalla de inicio con video de fondo"""
    ejecutando = True
    global generador_frames

    while ejecutando:
        try:
            frame = next(generador_frames)
        except StopIteration:
            # Reiniciar video al terminar
            generador_frames = video.iter_frames(fps=FPS, dtype="uint8")
            frame = next(generador_frames)

        # Convertir frame a superficie y dibujar
        superficie_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        pantalla.blit(superficie_frame, (0, 0))

        # Texto de instrucción
        texto = fuente_texto.render("Haz clic para continuar...", True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - 120, ALTO - 80))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pantalla_inicio_2()  # Ir a la segunda pantalla
                ejecutando = False

        pygame.display.flip()
        reloj.tick(FPS)

def pantalla_inicio_2():
    """Pantalla informativa con imagen, título y texto"""
    ejecutando = True
    while ejecutando:
        pantalla.blit(segunda_pantalla_fondo, (0, 0))
        
        # Instrucción
        instruccion = fuente_pequena.render("Haz clic para elegir tu personaje...", True, BLANCO)
        pantalla.blit(instruccion, (ANCHO // 2 - 140, ALTO - 80))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pantalla_3()
                ejecutando = False

        pygame.display.flip()
        reloj.tick(FPS)

#---TERCERA PANTALLA DE SELECCION DE PERSONAJES---
def pantalla_3():
    """Pantalla de selección de personajes"""
    if contador_victorias >= 5:
        pantalla_final()
        
    global jugador_seleccionado
    ejecutando = True
    while ejecutando:
        pantalla.blit(tercera_pantalla_fondo, (0, 0))
        titulo = fuente_titulo.render("Selecciona tu personaje", True, BLANCO)
        texto = fuente_texto.render(f"Victorias: {contador_victorias}/5", True, (255, 255, 255))
        pantalla.blit(texto, (10, 10))
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 80))

        dibujar_jugadores()

        pos_mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                clickeado = jugador_clickeado(pos_mouse)
                if clickeado is not None:
                    jugador_seleccionado = clickeado
                    if jugador_seleccionado == 0:
                        pantalla_personaje_Juan()
                    elif jugador_seleccionado == 1:
                        pantalla_personaje_Jeremy()
                    elif jugador_seleccionado == 2:
                        pantalla_personaje_Navi()
                    elif jugador_seleccionado == 3:
                        pantalla_personaje_Johana()
                    elif jugador_seleccionado == 4:
                        pantalla_personaje_Aquiles()

        pygame.display.flip()
        reloj.tick(FPS)
        
def dibujar_jugadores():
    """Dibuja los íconos de los personajes distribuidos uniformemente en el ancho de la pantalla"""
    global posiciones_jugadores  # Para usar las posiciones en la detección de clic
    cantidad = len(imagenes_jugadores)
    espacio = 800 // (cantidad + 1)  # Separación horizontal uniforme
    y = 340  # Altura centrada
    lista = ["Juan", "Jeremy", "Ivan", "Johana", "Aquiles"]

    posiciones_jugadores = []  # Reinicia la lista de posiciones cada vez

    for i, imagen in enumerate(imagenes_jugadores):
        x = espacio * (i + 1)
        pos = (x, y)
        posiciones_jugadores.append(pos)

        rect = imagen.get_rect(center=pos)
        pantalla.blit(imagen, rect)

        # Si está seleccionado, dibuja un círculo resaltado
        if jugador_seleccionado == i:
            pygame.draw.circle(pantalla, AMARILLO, pos, radio + 15, 4)

        # Dibuja el nombre correspondiente debajo del personaje
        nombre = lista[i] if i < len(lista) else f"Personaje {i + 1}"
        etiqueta = fuente_pequena.render(nombre, True, BLANCO)
        pantalla.blit(etiqueta, (pos[0] - etiqueta.get_width() // 2, pos[1] + 180))


def jugador_clickeado(pos_mouse):
    """Devuelve el índice del jugador clickeado"""
    for i, pos in enumerate(posiciones_jugadores):
        x, y = pos
        if (pos_mouse[0] - x) ** 2 + (pos_mouse[1] - y) ** 2 <= radio ** 2:
            return i
    return None


def pantalla_mini_juego(indice_jugador):
    """Pantalla temporal al seleccionar un personaje"""
    lista = ["Juan", "Jeremy", "Ivan", "Johana", "Aquiles"]
    nombre = lista[indice_jugador] if indice_jugador < len(lista) else f"Personaje {indice_jugador + 1}"

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill((50, 50, 100))
        mensaje = fuente_titulo.render(f"Mini juego de {nombre}", True, BLANCO)
        pantalla.blit(mensaje, mensaje.get_rect(center=(ANCHO // 2, ALTO // 2)))
        sub_mensaje = fuente_pequena.render("Presiona ESC para volver", True, BLANCO)
        pantalla.blit(sub_mensaje, sub_mensaje.get_rect(center=(ANCHO // 2, ALTO // 2 + 50)))

        # Volver con ESC
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            ejecutando = False

        pygame.display.flip()
        reloj.tick(FPS)

#---MINIJUEGOS POR PERSONAJE
#0
def pantalla_personaje_Juan():
    pygame.display.set_caption("🐄 Capiatá “La vaca me persigue” ")
    reloj = pygame.time.Clock()
    FPS_CAPIATA = 60
    LARGO_MUNDO = ANCHO * 6

    FUENTE_UI = pygame.font.Font(None, 30)
    FUENTE_GRANDE = pygame.font.Font(None, 74)
    FUENTE_MEDIANA = pygame.font.Font(None, 50)

    # --- 4. CARGA DE IMÁGENES Y AUDIO ---
    TAMAÑO_PERSONAJE = (120, 120)
    TAMAÑO_AO_AO = (250, 250)
    TAMAÑO_ESTABLO = (400, 300)
    TAMAÑO_TERMO = (50, 80)
    TAMAÑO_LOGO_PANTALLA_INICIO = (800, 600) 
    TAMAÑO_PANTALLA_FINAL = (ANCHO, ALTO)

    VELOCIDAD_ANIMACION = 5
    VELOCIDAD_ANIMACION_AO_AO = 10 

    # ✅ Rutas de Video y Imagen (¡Importante la extensión!)
    video1 = VideoFileClip("static/ganastecap.mp4")
    video1 = video1.resized((ANCHO, ALTO))
    generador_frames1 = video1.iter_frames(fps=FPS_CAPIATA, dtype="uint8")
    # CORREGIDO: Ahora apunta a una imagen


    # Declaración de variables globales de recursos (Sin cambios)
    FRAMES_PERSONAJE = []
    FRAMES_AO_AO = []
    IMAGEN_ESTABLO = None
    IMAGEN_TERMO = None
    IMAGEN_FONDO_TILE = None
    ANCHO_FONDO_REAL = ANCHO
    IMAGEN_LOGO = None 
    IMAGEN_GANAR = None
    IMAGEN_PERDER = None # Agregada la variable para la imagen de derrota


    class MockSound:
        def play(self): pass
    SONIDO_MUDA = MockSound()
    SONIDO_TROPPIEZO = MockSound()
    RUTA_MUSICA = None

    try:
        # Helper para cargar imagen y manejar errores de ruta
        def load_img(nombre, tamaño):
            ruta = os.path.join('static', nombre)
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, tamaño)

        # --- Carga de Animaciones y Objetos (Mismo código) ---
        FRAMES_PERSONAJE_NOMBRES = ['juanpaso1.png', 'juanpaso2.png', 'juanpaso3.png']
        for nombre in FRAMES_PERSONAJE_NOMBRES:
            FRAMES_PERSONAJE.append(load_img(nombre, TAMAÑO_PERSONAJE))
            
        FRAMES_AO_AO_NOMBRES = ['vaca_paso1cap.png', 'vaca_paso2cap.png', 'vaca_paso3cap.png']
        for nombre in FRAMES_AO_AO_NOMBRES:
            FRAMES_AO_AO.append(load_img(nombre, TAMAÑO_AO_AO))

        IMAGEN_ESTABLO = load_img('llegadacap.png', TAMAÑO_ESTABLO)
        IMAGEN_TERMO = load_img('termocap.png', TAMAÑO_TERMO)

        IMAGEN_LOGO = load_img('primera_pantallacap.png', TAMAÑO_LOGO_PANTALLA_INICIO)
        
        # CORRECCIÓN: Carga la imagen de derrota
        IMAGEN_PERDER = load_img('perdistecap.png', TAMAÑO_PANTALLA_FINAL)
        
        # 4. Fondo (Mismo código)
        IMAGEN_FONDO_TILE_ORIGINAL = pygame.image.load(os.path.join('static', 'capiatalit.png')).convert_alpha()
        ALTO_FONDO_TILE_ORIGINAL = IMAGEN_FONDO_TILE_ORIGINAL.get_height()
        ESCALA = ALTO / ALTO_FONDO_TILE_ORIGINAL
        ANCHO_FONDO_REAL = int(IMAGEN_FONDO_TILE_ORIGINAL.get_width() * ESCALA)
        IMAGEN_FONDO_TILE = pygame.transform.scale(
            IMAGEN_FONDO_TILE_ORIGINAL, (ANCHO_FONDO_REAL, ALTO)
        )
        
        # 5. Carga de Audio (Mismo código)
        RUTA_MUSICA = os.path.join('static', 'musica_fondocap.mp3')
        SONIDO_MUDA = pygame.mixer.Sound(os.path.join('static', 'muucap.wav'))
        SONIDO_TROPPIEZO = pygame.mixer.Sound(os.path.join('static', 'tropezarcap.wav'))

    except pygame.error as e:
        print(f"Error al cargar recursos: {e}")
    # ... (Fin del bloque de carga) ...


    # --- 5. Funciones del Mundo (En lugar de Clase Estancia) ---
    def crear_estancia():
        # Usamos un Sprite genérico como contenedor de datos
        estancia = pygame.sprite.Sprite() 
        estancia.offset_x = 0
        estancia.limite_scroll = LARGO_MUNDO - ANCHO
        estancia.scroll_speed = 0
        estancia.fondo_tile = IMAGEN_FONDO_TILE
        estancia.ancho_tile = ANCHO_FONDO_REAL
        estancia.y_suelo_general = ALTO - 10 
        return estancia

    def draw_background(estancia, pantalla): 
        num_tiles = ANCHO // estancia.ancho_tile + 2
        offset_dibujo = estancia.offset_x % estancia.ancho_tile
        for i in range(num_tiles):
            x_pos = (i * estancia.ancho_tile) - offset_dibujo 
            pantalla.blit(estancia.fondo_tile, (x_pos, 0))

    # --- 6. Funciones del Juego (En lugar de Clases de Sprites) ---

    # --- Personaje ---
    def crear_personaje():
        personaje = pygame.sprite.Sprite() # Contenedor
        personaje.frames = FRAMES_PERSONAJE
        personaje.indice_frame = 0
        personaje.image = personaje.frames[personaje.indice_frame]
        personaje.contador_animacion = 0
        personaje.VELOCIDAD_ANIMACION = VELOCIDAD_ANIMACION

        personaje.rect = personaje.image.get_rect()
        personaje.y_suelo = ALTO - personaje.rect.height - 10
        personaje.rect.bottom = personaje.y_suelo
        personaje.rect.left = ANCHO // 4

        personaje.vel_base = 5.0
        personaje.vel_vertical = 0 
        personaje.gravedad = 1.2 
        personaje.fatiga = 0
        personaje.FATIGA_MAX = 80
        personaje.en_salto = False
        personaje.posicion_mundo_x = personaje.rect.x
        return personaje

    def saltar_personaje(personaje, _):
        if not personaje.en_salto and personaje.fatiga < personaje.FATIGA_MAX:
            personaje.en_salto = True
            personaje.vel_vertical = -25 
            personaje.fatiga += 20
            if personaje.fatiga >= personaje.FATIGA_MAX:
                return True
        return False

    def animar_personaje(personaje):
        personaje.contador_animacion += 1
        if personaje.contador_animacion >= personaje.VELOCIDAD_ANIMACION:
            personaje.contador_animacion = 0
            personaje.indice_frame = (personaje.indice_frame + 1) % len(personaje.frames)
            personaje.image = personaje.frames[personaje.indice_frame]

    def update_personaje(personaje, estancia):
        movimiento_x = personaje.vel_base
        
        if not personaje.en_salto and movimiento_x > 0:
            animar_personaje(personaje) # Llamada a la función
        elif movimiento_x == 0 and not personaje.en_salto:
            personaje.image = personaje.frames[0] 
            
        if estancia.offset_x < estancia.limite_scroll:
            estancia.scroll_speed = movimiento_x
            personaje.posicion_mundo_x += movimiento_x
        else:
            estancia.scroll_speed = 0
            personaje.rect.x += movimiento_x
            personaje.posicion_mundo_x += movimiento_x

        estancia.offset_x = min(estancia.limite_scroll, estancia.offset_x + estancia.scroll_speed)

        if personaje.en_salto:
            personaje.rect.y += personaje.vel_vertical
            personaje.vel_vertical += personaje.gravedad

            if personaje.rect.bottom >= personaje.y_suelo:
                personaje.rect.bottom = personaje.y_suelo
                personaje.en_salto = False
                personaje.vel_vertical = 0

        if personaje.fatiga > 0 and not personaje.en_salto:
            personaje.fatiga = max(0, personaje.fatiga - 1.0) 
            
    def tropezar_personaje(personaje):
        personaje.vel_base = 1.0 
        personaje.fatiga = min(personaje.FATIGA_MAX, personaje.fatiga + 30)
        SONIDO_TROPPIEZO.play()
        return 60 

    # --- AoAo ---
    def crear_aoao(personaje_pos_x, personaje_y_suelo):
        aoao = pygame.sprite.Sprite() # Contenedor
        aoao.frames = FRAMES_AO_AO
        aoao.indice_frame = 0
        aoao.image = aoao.frames[aoao.indice_frame]
        aoao.contador_animacion = 0
        aoao.VELOCIDAD_ANIMACION = VELOCIDAD_ANIMACION_AO_AO

        aoao.rect = aoao.image.get_rect()
        aoao.rect.bottom = personaje_y_suelo
        
        aoao.posicion_mundo_x = personaje_pos_x - 300
        aoao.rect.left = aoao.posicion_mundo_x
        
        aoao.velocidad = 4.0
        return aoao

    def animar_aoao(aoao):
        aoao.contador_animacion += 1
        if aoao.contador_animacion >= aoao.VELOCIDAD_ANIMACION:
            aoao.contador_animacion = 0
            aoao.indice_frame = (aoao.indice_frame + 1) % len(aoao.frames)
            aoao.image = aoao.frames[aoao.indice_frame]
            
    def update_aoao(aoao, personaje, estancia):
        velocidad_real = aoao.velocidad + (personaje.vel_base * 0.1) 
        
        dx = personaje.posicion_mundo_x - aoao.posicion_mundo_x
        if abs(dx) > velocidad_real * 0.5:
            if dx > 0:
                aoao.posicion_mundo_x += velocidad_real
                animar_aoao(aoao) # Llamada a la función
            else:
                aoao.posicion_mundo_x -= velocidad_real
                animar_aoao(aoao) # Llamada a la función
        else:
            aoao.image = aoao.frames[0]
            
        aoao.rect.bottom = estancia.y_suelo_general 
        aoao.rect.x = int(aoao.posicion_mundo_x - estancia.offset_x)

    # --- Establo ---
    def crear_establo():
        establo = pygame.sprite.Sprite() # Contenedor
        establo.image = IMAGEN_ESTABLO
        establo.rect = establo.image.get_rect()
        establo.posicion_mundo_x = LARGO_MUNDO - establo.rect.width - 20 
        establo.rect.bottom = ALTO - 10
        return establo

    def update_establo(establo, estancia):
        establo.rect.x = int(establo.posicion_mundo_x - estancia.offset_x)

    # --- Obstaculo ---
    def crear_obstaculo(posicion_mundo_x, y_suelo):
        obstaculo = pygame.sprite.Sprite() # Contenedor
        obstaculo.image = IMAGEN_TERMO
        obstaculo.rect = obstaculo.image.get_rect()
        obstaculo.rect.bottom = y_suelo
        obstaculo.posicion_mundo_x = posicion_mundo_x
        return obstaculo

    def update_obstaculo(obstaculo, estancia):
        obstaculo.rect.x = int(obstaculo.posicion_mundo_x - estancia.offset_x)
        if obstaculo.rect.right < 0:
            obstaculo.kill() # .kill() funciona porque es un Sprite

    # --- 7. Funciones de UI y Pantallas (Actualizadas) ---
    # ... (Función dibujar_ui sin cambios) ...
    def dibujar_ui(pantalla, personaje):
        barra_ancho = 200
        barra_alto = 20
        barra_x = 50
        barra_y = 20

        pygame.draw.rect(pantalla, NEGRO, (barra_x - 2, barra_y - 2, barra_ancho + 4, barra_alto + 4), 2)
        relleno_ancho = (personaje.fatiga / personaje.FATIGA_MAX) * barra_ancho
        color_fatiga = ROJO if personaje.fatiga > personaje.FATIGA_MAX * 0.6 else VERDE
        pygame.draw.rect(pantalla, color_fatiga, (barra_x, barra_y, relleno_ancho, barra_alto))

        texto_fatiga = FUENTE_UI.render("Fatiga", True, NEGRO)
        pantalla.blit(texto_fatiga, (barra_x + barra_ancho + 10, barra_y))

    # ... (Función mostrar_mensaje sin cambios) ...
    def mostrar_mensaje(pantalla, mensaje, color):
        texto = FUENTE_GRANDE.render(mensaje, True, color)
        texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(texto, texto_rect)

    # ... (Función pantalla_inicio sin cambios) ...
    def pantalla_inicio(pantalla):
        pygame.mixer.music.stop() 
        
        pantalla.fill(AZUL)
        
        titulo = FUENTE_GRANDE.render("", True, BLANCO)
        instruccion = FUENTE_MEDIANA.render("Haz clic o toca la pantalla para saltar y empezar", True, BLANCO)
        
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 4 - 50)) 
        y_instruccion = titulo_rect.bottom + 100
        
        if IMAGEN_LOGO is not None:
            imagen_rect = IMAGEN_LOGO.get_rect(center=(ANCHO // 2, ALTO // 2)) 
            pantalla.blit(IMAGEN_LOGO, imagen_rect)
            y_instruccion = imagen_rect.bottom + 40
        
        instruccion_rect = instruccion.get_rect(center=(ANCHO // 2, y_instruccion))
        
        pantalla.blit(titulo, titulo_rect)
        pantalla.blit(instruccion, instruccion_rect)
        
        pygame.display.flip()
        
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False
            reloj.tick(FPS_CAPIATA)

        # ... (Función pantalla_final_ganar sin cambios) ...
    def pantalla_final_ganar(pantalla):
        global contador_victorias
        pygame.mixer.music.stop()
        contador_victorias += 1  # ✅ Aumentar contador de victorias

        nonlocal generador_frames1, video1

        ejecutando = True
        while ejecutando:
            try:
                frame = next(generador_frames1)
            except StopIteration:
                generador_frames1 = video1.iter_frames(fps=FPS_CAPIATA, dtype="uint8")
                frame = next(generador_frames1)

            superficie_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            superficie_frame = pygame.transform.scale(superficie_frame, (ANCHO, ALTO))
            pantalla.blit(superficie_frame, (0, 0))

            # Texto sobre el video
            texto_instruccion = FUENTE_MEDIANA.render("Haz clic para continuar", True, BLANCO)
            texto_instruccion_rect = texto_instruccion.get_rect(center=(ANCHO // 2, ALTO - 60))
            pantalla.blit(texto_instruccion, texto_instruccion_rect)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    ejecutando = False
                    pantalla_3()  # ✅ Redirigir a pantalla_3()

            pygame.display.flip()
            reloj.tick(FPS_CAPIATA)


    def pantalla_final_perder(pantalla):
        pygame.mixer.music.stop()
        
        try:
            if IMAGEN_PERDER is not None:
                pantalla.blit(IMAGEN_PERDER, (0, 0))
            else:
                pantalla.fill(ROJO)
        except Exception as e:
            print(f"Error al dibujar la pantalla de derrota: {e}")
            pantalla.fill(ROJO)
            mostrar_mensaje(pantalla, "¡CAPTURA! (Error fatal)", BLANCO)

        # Mensajes de opciones
        texto_esc = FUENTE_MEDIANA.render("Presiona ESC para volver", True, BLANCO)
        texto_r = FUENTE_MEDIANA.render("Presiona R para intentarlo nuevamente", True, BLANCO)
        pantalla.blit(texto_esc, (ANCHO // 2 - texto_esc.get_width() // 2, ALTO - 120))
        pantalla.blit(texto_r, (ANCHO // 2 - texto_r.get_width() // 2, ALTO - 60))
        pygame.display.flip()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pantalla_3()  # ✅ Volver a pantalla_3()
                        esperando = False
                    elif evento.key == pygame.K_r:
                        pantalla_personaje_Juan()  # ✅ Reintentar el juego
                        esperando = False
            reloj.tick(FPS_CAPIATA)



    # ----------------------------------------------------------------------
    ## 🎮 Función Principal (Bucle de juego - ACTUALIZADO)
    def juego():
        try:
            if RUTA_MUSICA:
                pygame.mixer.music.load(RUTA_MUSICA)
                pygame.mixer.music.play(-1) 
        except pygame.error as e:
            print(f"Advertencia: No se pudo reproducir la música de fondo. {e}")

        # --- CREACIÓN USANDO FUNCIONES ---
        estancia = crear_estancia()
        personaje = crear_personaje()
        aoao = crear_aoao(personaje.posicion_mundo_x, personaje.y_suelo)
        establo = crear_establo()

        # Grupos de sprites (Esto sigue igual, ¡porque los creadores devuelven Sprites!)
        obstaculos = pygame.sprite.Group()
        todos_los_sprites = pygame.sprite.Group(personaje, aoao, establo) 

        corriendo = True
        juego_terminado = False
        ganado = False
        
        fatiga_stunt_timer = 0
        tropezon_stunt_timer = 0
        
        GENERAR_OBSTACULO_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(GENERAR_OBSTACULO_EVENT, random.randint(1500, 3000)) 

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
                    # --- LLAMADA A FUNCIÓN ---
                    if saltar_personaje(personaje, pygame.mouse.get_pos()):
                        fatiga_stunt_timer = 60
                
                if evento.type == GENERAR_OBSTACULO_EVENT and not juego_terminado and estancia.offset_x < estancia.limite_scroll:
                    pos_x_mundo = estancia.offset_x + ANCHO 
                    # --- LLAMADA A FUNCIÓN ---
                    nuevo_obstaculo = crear_obstaculo(pos_x_mundo, personaje.y_suelo)
                    obstaculos.add(nuevo_obstaculo)
                    todos_los_sprites.add(nuevo_obstaculo)
                    pygame.time.set_timer(GENERAR_OBSTACULO_EVENT, random.randint(1500, 3000)) 
                    
            if not juego_terminado:
                
                if fatiga_stunt_timer > 0:
                    personaje.vel_base = 2.0
                    fatiga_stunt_timer -= 1
                elif tropezon_stunt_timer > 0:
                    tropezon_stunt_timer -= 1
                else:
                    personaje.vel_base = 5.0

                # --- LLAMADAS A FUNCIONES DE UPDATE ---
                update_personaje(personaje, estancia)
                update_aoao(aoao, personaje, estancia)
                update_establo(establo, estancia)
                
                # ¡IMPORTANTE! obstaculos.update() ya no funciona 
                # porque los sprites no tienen un método .update
                # Debemos iterar y llamar a nuestra función manualmente.
                for obstaculo in obstaculos:
                    update_obstaculo(obstaculo, estancia)
                # --- FIN DEL CAMBIO IMPORTANTE ---

                obstaculos_colisionados = pygame.sprite.spritecollide(personaje, obstaculos, True)
                if obstaculos_colisionados:
                    if not personaje.en_salto and tropezon_stunt_timer == 0:
                        # --- LLAMADA A FUNCIÓN ---
                        tropezon_stunt_timer = tropezar_personaje(personaje)

                if pygame.sprite.collide_rect(personaje, aoao):
                    juego_terminado = True
                    ganado = False
                    estancia.scroll_speed = 0
                    SONIDO_MUDA.play() 

                if personaje.posicion_mundo_x > establo.posicion_mundo_x:
                    juego_terminado = True
                    ganado = True
                    estancia.scroll_speed = 0 
            
            # --- LLAMADA A FUNCIÓN ---
            draw_background(estancia, pantalla) 
            
            # .draw() sigue funcionando porque los objetos SON sprites
            todos_los_sprites.draw(pantalla)
            
            dibujar_ui(pantalla, personaje)

            if juego_terminado:
                corriendo = False

            pygame.display.flip()
            reloj.tick(FPS_CAPIATA)
        
        pygame.time.set_timer(GENERAR_OBSTACULO_EVENT, 0)
        return ganado

    # ----------------------------------------------------------------------
    ## 🚀 Bucle Principal de Ejecución (Sin cambios)
    if __name__ == "__main__":
        juego_activo = True
        while juego_activo:
            
            pantalla_inicio(pantalla)
            
            resultado = juego()
            
            if resultado is True: 
                pantalla_final_ganar(pantalla)
            elif resultado is False: 
                pantalla_final_perder(pantalla)
            
        pygame.quit()
        sys.exit()

#1
def pantalla_personaje_Jeremy():

    # === UTILIDAD DE RUTAS SEGURAS ===
    BASE_DIR = Path(__file__).resolve().parent
    def asset_path(*parts) -> str:
        return str(BASE_DIR.joinpath(*parts))

    # === FUNCIÓN PRINCIPAL ===
    def pantalla_personaje_Jeremy():
        global contador_victorias
        pygame.display.set_caption("🕳 San Lorenzo - Esquivar")
        FPS = 60

        fuente = pygame.font.Font(None, 36)

        # --- FONDOS ---
        def cargar_fondo(rel_path, color=(0,0,0)):
            ruta = asset_path(rel_path)
            try:
                img = pygame.image.load(ruta).convert()
                return pygame.transform.scale(img, (ANCHO, ALTO))
            except Exception as e:
                print(f"[WARN] No se pudo cargar {ruta}: {e}")
                surf = pygame.Surface((ANCHO, ALTO))
                surf.fill(color)
                return surf

        fondo_inicio   = cargar_fondo("static/fondo_inicio_SL.png", (30, 30, 30))
        fondo_juego    = cargar_fondo("static/Fondo1_SL.png",       (0, 0, 0))
        fondo_derrota  = cargar_fondo("static/fondo_derrota_SL.png",(50, 0, 0))
        video_victoria = VideoFileClip("static/Video-Victoria-SL.mp4").resized((ANCHO, ALTO))

        # --- SPRITESHEET ANIMADO DEL JUGADOR ---
        COLUMNS = 4
        ROWS    = 2
        FRAME_SIZE = (100, 100)

        def parse_spritesheet(sheet: pygame.Surface, columns: int, rows: int, scale_to):
            frames = []
            sw, sh = sheet.get_width(), sheet.get_height()
            fw, fh = sw // columns, sh // rows
            for r in range(rows):
                for c in range(columns):
                    rect = pygame.Rect(c * fw, r * fh, fw, fh)
                    frame = sheet.subsurface(rect)
                    frame = pygame.transform.scale(frame, scale_to)
                    frames.append(frame)
            return frames

        try:
            ss_img = pygame.image.load(asset_path("static", "personaje_spritesheet.png")).convert_alpha()
            all_frames = parse_spritesheet(ss_img, COLUMNS, ROWS, FRAME_SIZE)
            jugador_frames = {"idle": all_frames[0:4], "move": all_frames[4:8]}
        except Exception as e:
            print(f"[WARN] No se pudo cargar spritesheet: {e}")
            fallback = pygame.Surface(FRAME_SIZE, pygame.SRCALPHA)
            fallback.fill(VERDE)
            jugador_frames = {"idle": [fallback], "move": [fallback]}

        # --- IMAGENES Y AUDIO ---
        try:
            bache_img = pygame.image.load(asset_path("static", "bache.png")).convert_alpha()
            bache_img = pygame.transform.scale(bache_img, (80, 60))
        except Exception:
            bache_img = pygame.Surface((80, 60)); bache_img.fill(ROJO)

        try:
            corazon_img = pygame.image.load(asset_path("static", "corazon.png")).convert_alpha()
            corazon_img = pygame.transform.scale(corazon_img, (32, 32))
        except Exception:
            corazon_img = None

        img_golpe = None

        try:
            pygame.mixer.music.load(asset_path("static", "musica_fondo.mp3"))
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[WARN] Música no cargada: {e}")

        try:
            snd_victoria = pygame.mixer.Sound(asset_path("static", "victoria.mp3"))
        except Exception:
            snd_victoria = None

        # === PANTALLA INICIO ===
        def pantalla_inicio():
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            pantalla_juego(); return
                        if e.key == pygame.K_ESCAPE:
                            pygame.quit(); sys.exit()

                pantalla.blit(fondo_inicio, (0, 0))
                texto = fuente.render("Presiona ESPACIO para comenzar", True, BLANCO)
                pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 + 230))
                pygame.display.flip()
                reloj.tick(FPS)

        # === PANTALLA JUEGO ===
        def pantalla_juego():
            global contador_victorias  # ✅ necesario para modificar la variable global

            jugador_rect = pygame.Rect(0, 0, FRAME_SIZE[0], FRAME_SIZE[1])
            jugador_rect.midbottom = (ANCHO // 2, ALTO - 20)
            vel = 8
            mirando_izq = False
            anim_state, anim_index = "idle", 0
            anim_last = pygame.time.get_ticks()
            anim_speed_idle, anim_speed_move = 200, 100

            baches = []
            vidas, puntaje, meta = 5, 0, 20
            bache_timer = 0

            while True:
                dt = reloj.tick(FPS)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit()

                # Movimiento + animación
                mov = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    mov -= vel; mirando_izq = True
                if keys[pygame.K_RIGHT]:
                    mov += vel; mirando_izq = False

                jugador_rect.x += mov
                anim_state = "move" if mov != 0 else "idle"
                if jugador_rect.left < 0: jugador_rect.left = 0
                if jugador_rect.right > ANCHO: jugador_rect.right = ANCHO

                # Spawn baches
                bache_timer += dt
                if bache_timer > 800:
                    bache_timer = 0
                    x = random.randint(0, ANCHO - bache_img.get_width())
                    rect = bache_img.get_rect(topleft=(x, -bache_img.get_height()))
                    baches.append({"rect": rect, "vel": 5})

                pantalla.blit(fondo_juego, (0, 0))

                # Animación jugador
                now = pygame.time.get_ticks()
                speed = anim_speed_move if anim_state == "move" else anim_speed_idle
                frames = jugador_frames[anim_state]
                if now - anim_last >= speed:
                    anim_last = now
                    anim_index = (anim_index + 1) % len(frames)
                frame_img = frames[anim_index]
                if mirando_izq:
                    frame_img = pygame.transform.flip(frame_img, True, False)
                pantalla.blit(frame_img, jugador_rect)

                # Baches
                for b in baches[:]:
                    b["rect"].y += b["vel"]
                    pantalla.blit(bache_img, b["rect"])

                    if b["rect"].colliderect(jugador_rect):
                        vidas -= 1
                        if img_golpe:
                            pantalla.blit(img_golpe, img_golpe.get_rect(center=jugador_rect.center))
                            pygame.display.flip()
                            pygame.time.delay(250)
                        baches.remove(b)
                        if vidas <= 0:
                            pantalla_derrota(); return

                    elif b["rect"].top > ALTO:
                        baches.remove(b)
                        puntaje += 1
                        if puntaje >= meta:
                            if snd_victoria: snd_victoria.play()
                            pantalla_victoria(); return

                # HUD
                if corazon_img:
                    for i in range(vidas):
                        pantalla.blit(corazon_img, (10 + i * 36, 10))
                else:
                    for i in range(vidas):
                        pygame.draw.circle(pantalla, ROJO, (30 + i*40, 30), 15)

                pts = fuente.render(f"Puntos: {puntaje}/{meta}", True, BLANCO)
                pantalla.blit(pts, (ANCHO - 220, 20))
                pygame.display.flip()

        # === PANTALLA VICTORIA ===
        def pantalla_victoria():
            global contador_victorias
            contador_victorias += 1  # ✅ Aumenta el contador al entrar

            # Reproducir video frame por frame
            for frame in video_victoria.iter_frames(fps=FPS, dtype='uint8'):
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        pantalla_3()  # Ir a la siguiente pantalla al hacer click
                        return

                # Convertir frame de MoviePy a superficie de Pygame
                frame_surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                pantalla.blit(frame_surf, (0, 0))

                # Textos encima del video
                t3 = fuente.render("Haz clic para continuar", True, BLANCO)
                pantalla.blit(t3, t3.get_rect(center=(ANCHO//2, ALTO - 80)))

                pygame.display.flip()
                reloj.tick(FPS)

            # Cuando termine el video, esperar click para continuar
            esperando_click = True
            while esperando_click:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        pantalla_3()
                        return
                reloj.tick(FPS)
        # === PANTALLA DERROTA ===
        def pantalla_derrota():
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            pantalla_3(); return  # ESC para volver
                        if e.key == pygame.K_r:
                            pantalla_personaje_Jeremy(); return  # R para intentar nuevamente

                pantalla.blit(fondo_derrota, (0, 0))
                t1 = fuente.render("Presiona ESC para volver", True, BLANCO)
                t2 = fuente.render("Presiona R para intentarlo nuevamente", True, BLANCO)
                pantalla.blit(t1, t1.get_rect(center=(ANCHO//2, ALTO//2 + 160)))
                pantalla.blit(t2, t2.get_rect(center=(ANCHO//2, ALTO//2 + 200)))
                pygame.display.flip()
                reloj.tick(FPS)
        # Inicia desde pantalla inicio
        pantalla_inicio()

    # === EJECUTAR ===
    if __name__ == "__main__":
        pantalla_personaje_Jeremy()

#2
def pantalla_personaje_Navi():
    # Cargar imágenes
    fondo = pygame.image.load("static/villarrica_fondo.png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    imagen_inicio = pygame.image.load("static/villarrica_inicio.png")
    imagen_inicio = pygame.transform.scale(imagen_inicio, (ANCHO, ALTO))

    imagen_perder = pygame.image.load("static/perdiste.png")
    imagen_perder = pygame.transform.scale(imagen_perder, (ANCHO, ALTO))

    # Tamaño del personaje
    TAM_PERSONAJE = 350
    pos_personaje = (ANCHO // 2 - TAM_PERSONAJE // 2, ALTO - TAM_PERSONAJE - 20)

    # Personajes
    personaje_inicio = pygame.image.load("static/navi.png")
    personaje_inicio = pygame.transform.scale(personaje_inicio, (TAM_PERSONAJE, TAM_PERSONAJE))

    personajes_direccion = {
        "ARRIBA": pygame.image.load("static/arriba.png"),
        "ABAJO": pygame.image.load("static/abajo.png"),
        "IZQUIERDA": pygame.image.load("static/izquierda.png"),
        "DERECHA": pygame.image.load("static/derecha.png")
    }

    for clave in personajes_direccion:
        personajes_direccion[clave] = pygame.transform.scale(personajes_direccion[clave], (TAM_PERSONAJE, TAM_PERSONAJE))

    opuesto = {
        "ARRIBA": "ABAJO",
        "ABAJO": "ARRIBA",
        "IZQUIERDA": "DERECHA",
        "DERECHA": "IZQUIERDA"
    }

    # Estado del juego
    vidas = 3
    puntos = 0
    puntos_maximos = 10
    direccion_actual = random.choice(list(personajes_direccion.keys()))
    mostrar_inicio = True
    reloj = pygame.time.Clock()

    # Funciones
    def mostrar_texto(texto, fuente, color, y):
        imagen = fuente.render(texto, True, color)
        rect = imagen.get_rect(center=(ANCHO // 2, y))
        pantalla.blit(imagen, rect)

    def pantalla_inicial():
        esperando_click = True
        while esperando_click:
            pantalla.blit(imagen_inicio, (0, 0))
            mostrar_texto("Haz clic para comenzar", fuente_info, BLANCO, ALTO - 50)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    esperando_click = False

    def perder():
        global pantalla
        nonlocal imagen_perder  # Usa global si están fuera de la función
        pygame.mixer.music.stop()

        pantalla.blit(imagen_perder, (0, 0))

        fuente = pygame.font.Font(None, 50)
        texto_esc = fuente.render("Presiona ESC para volver", True, (255, 255, 255))
        texto_r = fuente.render("Presiona R para intentarlo nuevamente", True, (255, 255, 255))

        pantalla.blit(texto_esc, (ANCHO // 2 - texto_esc.get_width() // 2, ALTO - 150))
        pantalla.blit(texto_r, (ANCHO // 2 - texto_r.get_width() // 2, ALTO - 90))

        pygame.display.flip()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pantalla_3()  # ✅ Volver al menú
                        esperando = False
                    elif evento.key == pygame.K_r:
                        pantalla_personaje_Navi()  # ✅ Reintentar el juego
                        esperando = False


    def ganar():
        global contador_victorias
        contador_victorias += 1  # ✅ Aumentar el contador

        video = VideoFileClip("static/ganaste.mp4")
        video = video.resized((ANCHO, ALTO))
        generador_frames = video.iter_frames(fps=30, dtype="uint8")

        clock = pygame.time.Clock()
        ejecutando = True

        while ejecutando:
            try:
                frame = next(generador_frames)
            except StopIteration:
                break

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pantalla_3()  # ✅ Ir a pantalla_3() al hacer clic
                    ejecutando = False

            superficie = pygame.image.frombuffer(frame.tobytes(), video.size, "RGB")
            pantalla.blit(superficie, (0, 0))

            fuente = pygame.font.Font(None, 50)
            texto_click = fuente.render("Haz clic para continuar", True, (255, 255, 255))
            pantalla.blit(texto_click, (ANCHO // 2 - texto_click.get_width() // 2, ALTO - 80))

            pygame.display.flip()
            clock.tick(30)


    # Mostrar pantalla inicial
    pantalla_inicial()

    # Bucle principal
    while True:
        pantalla.blit(fondo, (0, 0))

        texto_vidas = fuente_info.render(f"Vidas: {vidas} / 3", True, BLANCO)
        pantalla.blit(texto_vidas, (20, 20))
        texto_puntos = fuente_info.render(f"Puntos: {puntos} / {puntos_maximos}", True, BLANCO)
        pantalla.blit(texto_puntos, (20, 60))

        instruccion = f"Mira hacia {direccion_actual.lower()}"
        mostrar_texto(instruccion, fuente_instruccion, BLANCO, 120)

        if mostrar_inicio:
            pantalla.blit(personaje_inicio, pos_personaje)
        else:
            pantalla.blit(personajes_direccion[direccion_actual], pos_personaje)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                mapa_teclas = {
                    pygame.K_UP: "ARRIBA",
                    pygame.K_DOWN: "ABAJO",
                    pygame.K_LEFT: "IZQUIERDA",
                    pygame.K_RIGHT: "DERECHA"
                }

                if evento.key in mapa_teclas:
                    tecla_presionada = mapa_teclas[evento.key]
                    respuesta_correcta = opuesto[direccion_actual]

                    if tecla_presionada == respuesta_correcta:
                        puntos += 1
                    else:
                        vidas -= 1

                    direccion_actual = random.choice(list(personajes_direccion.keys()))
                    mostrar_inicio = False

                    if vidas == 0:
                        perder()
                    if puntos == puntos_maximos:
                        ganar()

        pygame.display.flip()
        reloj.tick(30)

#3 
def pantalla_personaje_Johana():
    # ---- Utilidad de rutas seguras (relativas a este .py) ----
    BASE_DIR = Path(__file__).resolve().parent
    def asset_path(*parts) -> Path:
        return BASE_DIR.joinpath(*parts)

    def load_image(relative_path, *, alpha=False, scale=None, fallback=None, warn_name=""):
        p = asset_path(relative_path)
        try:
            img = pygame.image.load(str(p))
            img = img.convert_alpha() if alpha else img.convert()
            if scale:
                img = pygame.transform.scale(img, scale)
            return img
        except FileNotFoundError:
            msg = f"[ERROR] No se encontró: {p}"
            if warn_name:
                msg += f"  (Esperado para: {warn_name})"
            print(msg)
            if fallback is not None:
                return fallback
            raise

    # --- CONFIGURACIÓN DE LA PANTALLA ---
    pygame.display.set_caption("Duck Shooter - Pedro Juan")

    # Control de velocidad (FPS)
    reloj = pygame.time.Clock()
    FPS = 60

    # --- CARGA DE IMÁGENES Y VIDEO ---
    Inicio_fondo_JP = load_image("static/Fondo_inicio_PJ.png", alpha=False, scale=(ANCHO, ALTO), warn_name="Fondo inicio")
    Juego_fondo_JP  = load_image("static/Fondo_de_juego.png", alpha=False, scale=(ANCHO, ALTO), warn_name="Fondo juego")
    Fondo_derrota_JP= load_image("static/Fondo_derrota_PJ.png", alpha=False, scale=(ANCHO, ALTO), warn_name="Fondo derrota")

    pato_img    = load_image("static/Pato_PJ.png", alpha=True, scale=(120, 120), warn_name="Pato")
    mira_img    = load_image("static/Mira.png", alpha=True, scale=(100, 100), warn_name="Mira")
    jugador_img = load_image("static/Cazador.png", alpha=True, scale=(150, 150), warn_name="Cazador")

    try:
        bala_img_original = load_image("static/Bala_PJ.png", alpha=True, scale=(40, 20), warn_name="Bala")
    except FileNotFoundError:
        print("[WARN] Usando bala de respaldo.")
        bala_img_original = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.rect(bala_img_original, (255, 0, 0), (0, 0, 30, 10))

    try:
        VICTORY_VIDEO_PATH = asset_path("static", "Video-Victoria-PJ.mp4")
        video_clip = VideoFileClip(str(VICTORY_VIDEO_PATH), audio=True).resized((ANCHO, ALTO))
        pygame.mixer.init()
    except Exception as e:
        print(f"[WARN] No se pudo cargar el video: {e}")
        video_clip = None

    pygame.mouse.set_visible(True)

    # =========================================================
    #      REEMPLAZO DE CLASES POR FUNCIONES / DICCIONARIOS
    # =========================================================
    def crear_pato():
        rect = pato_img.get_rect()
        rect.x = random.randint(0, ANCHO - rect.width)
        rect.y = random.randint(80, ALTO // 2)
        return {
            "image": pato_img,
            "rect": rect,
            "vel_x": random.choice([-3, -2, 2, 3]),
            "vel_y": random.choice([-2, 2]),
            "vivo": True,
        }

    def actualizar_pato(p):
        p["rect"].x += p["vel_x"]
        p["rect"].y += p["vel_y"]
        if p["rect"].left < 0 or p["rect"].right > ANCHO:
            p["vel_x"] *= -1
        if p["rect"].top < 60 or p["rect"].bottom > ALTO - 150:
            p["vel_y"] *= -1

    def dibujar_pato(pant, p):
        pant.blit(p["image"], p["rect"])

    def crear_bala(x, y, destino):
        dx = destino[0] - x
        dy = destino[1] - y
        dist = math.hypot(dx, dy) or 1
        vel_x = dx / dist * 12
        vel_y = dy / dist * 12
        angulo = math.degrees(math.atan2(-dy, dx))  # 0° derecha
        image = pygame.transform.rotate(bala_img_original, angulo)
        rect = image.get_rect(center=(int(x), int(y)))
        return {
            "original_image": bala_img_original,
            "image": image,
            "angulo": angulo,
            "cx": float(x),
            "cy": float(y),
            "vel_x": vel_x,
            "vel_y": vel_y,
            "rect": rect,
            "viva": True,
        }

    def actualizar_bala(b):
        b["cx"] += b["vel_x"]
        b["cy"] += b["vel_y"]
        b["image"] = pygame.transform.rotate(b["original_image"], b["angulo"])
        b["rect"] = b["image"].get_rect(center=(int(b["cx"]), int(b["cy"])))
        if (b["rect"].x < -100 or b["rect"].x > ANCHO + 100 or
            b["rect"].y < -100 or b["rect"].y > ALTO + 100):
            b["viva"] = False

    def dibujar_bala(pant, b):
        pant.blit(b["image"], b["rect"])

    def colisiona(rect_a, rect_b):
        return rect_a.colliderect(rect_b)

    def reiniciar_juego():
        global patos, balas, puntaje, balas_restantes, estado, video_start_time, victoria_contada
        patos = [crear_pato() for _ in range(10)]
        balas = []
        puntaje = 0
        balas_restantes = 15
        estado = "inicio"
        video_start_time = 0
        victoria_contada = False

    # --- VARIABLES ---
    patos = [crear_pato() for _ in range(10)]
    balas = []
    jugador_pos = (ANCHO // 2, ALTO - 60)
    fuente = pygame.font.Font(None, 48)
    fuente_small = pygame.font.Font(None, 36)

    puntaje = 0
    balas_restantes = 15
    puntaje_meta = 10
    estado = "inicio"
    video_start_time = 0

    global contador_victorias
    victoria_contada = False  # evita sumar más de una vez

    # --- LOOP PRINCIPAL con control de salida ---
    running = True
    goto = None  # "pantalla_3" | "retry"

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                try:
                    if pygame.mixer.get_init():
                        pygame.mixer.quit()
                finally:
                    pygame.quit()
                    sys.exit()

            # ---------------------- Eventos por estado ----------------------
            if estado == "inicio":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    estado = "jugando"

            elif estado == "jugando":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if balas_restantes > 0:
                        destino = pygame.mouse.get_pos()
                        balas.append(crear_bala(jugador_pos[0], jugador_pos[1] - 50, destino))
                        balas_restantes -= 1

            elif estado == "victoria":
                # Click para continuar -> ir a pantalla_3()
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    goto = "pantalla_3"
                    running = False

            elif estado == "derrota":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        # Reintentar: llamar pantalla_personaje_johana()
                        goto = "retry"
                        running = False
                    elif evento.key == pygame.K_ESCAPE:
                        # Volver: ir a pantalla_3()
                        goto = "pantalla_3"
                        running = False

        # ---------------------- Lógica ----------------------
        if estado == "jugando":
            for p in patos:
                if p["vivo"]:
                    actualizar_pato(p)
            for b in balas:
                if b["viva"]:
                    actualizar_bala(b)
            for b in balas:
                if not b["viva"]:
                    continue
                for p in patos:
                    if p["vivo"] and colisiona(b["rect"], p["rect"]):
                        b["viva"] = False
                        p["vivo"] = False
                        puntaje += 1
                        break
            patos = [p for p in patos if p["vivo"]]
            balas = [b for b in balas if b["viva"]]

            # Condiciones de victoria/derrota
            if puntaje >= puntaje_meta:
                estado = "victoria"
                if not victoria_contada:
                    contador_victorias += 1   # ✅ suma una sola vez
                    victoria_contada = True
                video_start_time = time.time()
            elif balas_restantes <= 0 and puntaje < puntaje_meta:
                estado = "derrota"

        # ---------------------- Dibujado ----------------------
        if estado == "inicio":
            pantalla.blit(Inicio_fondo_JP, (0, 0))
            texto = fuente.render("Presiona ESPACIO para comenzar", True, (255, 255, 255))
            pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO - 50)))

        elif estado == "jugando":
            pantalla.blit(Juego_fondo_JP, (0, 0))
            for p in patos: dibujar_pato(pantalla, p)
            for b in balas: dibujar_bala(pantalla, b)
            pantalla.blit(jugador_img, jugador_img.get_rect(center=jugador_pos))
            pantalla.blit(fuente.render(f"Puntos: {puntaje}/{puntaje_meta}", True, (255, 255, 255)), (20, 20))
            pantalla.blit(fuente.render(f"Balas: {balas_restantes}", True, (255, 60, 60)), (20, 70))

        elif estado == "victoria":
            if video_clip:
                t = max(0.0, min(time.time() - video_start_time, video_clip.duration - 0.01))
                frame_array = video_clip.get_frame(t)
                frame_pygame = pygame.image.frombuffer(frame_array.tobytes(), video_clip.size, "RGB")
                pantalla.blit(frame_pygame, (0, 0))
            else:
                pantalla.fill((0, 0, 0))

            # Mensajes
            sub = fuente_small.render("Haz clic para continuar", True, (255, 255, 255))
            pantalla.blit(sub, sub.get_rect(center=(ANCHO // 2, ALTO - 40)))

        
            

        elif estado == "derrota":
            pantalla.blit(Fondo_derrota_JP, (0, 0))
            sub1 = fuente_small.render("Presiona R para intentarlo nuevamente", True, (255, 255, 255))
            sub2 = fuente_small.render("Presiona ESC para volver", True, (255, 255, 255))
            pantalla.blit(sub1, sub1.get_rect(center=(ANCHO // 2, ALTO - 80)))
            pantalla.blit(sub2, sub2.get_rect(center=(ANCHO // 2, ALTO - 40)))

        # Mira del mouse
        pantalla.blit(mira_img, mira_img.get_rect(center=pygame.mouse.get_pos()))
        pygame.display.flip()
        reloj.tick(FPS)

    # ---------- Salida del minijuego: redirección ----------
    if goto == "pantalla_3":
        pantalla_3()
    elif goto == "retry":
        pantalla_personaje_Johana()

 
#4        
def pantalla_personaje_Aquiles():
    pygame.display.set_caption("Aquiles en Luque - Atrapa los Cerdos")

    # Rutas
    STATIC_PATH = "static"

    # Cargar imágenes
    fondo = pygame.image.load(os.path.join(STATIC_PATH, "fondo_lu.png"))
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    cerdo_img = pygame.image.load(os.path.join(STATIC_PATH, "cerdo_lu.png"))
    cerdo_img = pygame.transform.scale(cerdo_img, (120, 120))

    pantalla_inicio_img = pygame.image.load(os.path.join(STATIC_PATH, "pantalla_inicio_lu.png"))
    pantalla_inicio_img = pygame.transform.scale(pantalla_inicio_img, (ANCHO, ALTO))

    pantalla_derrota_img = pygame.image.load(os.path.join(STATIC_PATH, "pantalla_derrota_lu.png"))
    pantalla_derrota_img = pygame.transform.scale(pantalla_derrota_img, (ANCHO, ALTO))

    # Animaciones
    aquiles_der_imgs = [
        pygame.transform.scale(pygame.image.load(os.path.join(STATIC_PATH, f"aquiles_der_{i}.png")), (120, 180))
        for i in range(1, 4)
    ]
    aquiles_izq_imgs = [
        pygame.transform.scale(pygame.image.load(os.path.join(STATIC_PATH, f"aquiles_izq_{i}.png")), (120, 180))
        for i in range(1, 4)
    ]

    # Sonidos
    sonido_cerdo = pygame.mixer.Sound(os.path.join(STATIC_PATH, "cerdo_atrapado.wav"))
    pygame.mixer.music.load(os.path.join(STATIC_PATH, "musica_fondo.mp3"))
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont("Arial", 28)
    clock = pygame.time.Clock()
    FPS = 60

    def pantalla_inicio():
        while True:
            pantalla.blit(pantalla_inicio_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()

    def pantalla_victoria():
        global contador_victorias
        contador_victorias += 1  # Aumenta 1 victoria

        video_path = os.path.join(STATIC_PATH, "video_victoria.mp4")
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (ANCHO, ALTO))
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            pantalla.blit(surface, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    sys.exit()

        cap.release()

        # Mostrar mensaje y esperar clic
        esperando_click = True
        while esperando_click:
            texto2 = font.render("Haz clic para continuar", True, (255, 255, 255))
            pantalla.blit(texto2, (ANCHO//2 - texto2.get_width()//2, ALTO//2 + 230))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    esperando_click = False
                    pantalla_3()  # Redirige a pantalla_3()
                    return


    def pantalla_derrota():
        while True:
            pantalla.blit(pantalla_derrota_img, (0, 0))

            texto2 = font.render("Presiona ESC para volver", True, (255, 255, 255))
            texto3 = font.render("Presiona R para intentarlo nuevamente", True, (255, 255, 255))

            pantalla.blit(texto2, (ANCHO//2 - texto2.get_width()//2, ALTO//2 + 190))
            pantalla.blit(texto3, (ANCHO//2 - texto3.get_width()//2, ALTO//2 + 220))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pantalla_3()  # Volver a pantalla_3()
                        return
                    if event.key == pygame.K_r:
                        pantalla_personaje_Aquiles()  # Reintentar
                        return
                    
    def jugar():
        score = 0
        tiempo_limite = 15
        start_ticks = pygame.time.get_ticks()

        aquiles_rect = aquiles_der_imgs[0].get_rect(topleft=(100, 400))
        aquiles_speed = 4

        anim_index = 0
        anim_timer = 0

        cerdos = []
        ultimo_cerdo = pygame.time.get_ticks()
        cerdo_generado = 0
        max_cerdos = 10

        posiciones_y = [350, 390, 430, 470, 510]

        while True:
            pantalla.blit(fondo, (0,0))
            clock.tick(FPS)

            segundos = tiempo_limite - ((pygame.time.get_ticks() - start_ticks) // 1000)
            if segundos <= 0:
                pantalla_derrota()
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                aquiles_rect.x -= aquiles_speed
                imgs = aquiles_izq_imgs
            elif keys[pygame.K_RIGHT]:
                aquiles_rect.x += aquiles_speed
                imgs = aquiles_der_imgs
            else:
                imgs = aquiles_der_imgs

            anim_timer += 1
            if anim_timer >= 10:
                anim_index = (anim_index + 1) % 3
                anim_timer = 0

            if cerdo_generado < max_cerdos and pygame.time.get_ticks() - ultimo_cerdo > 1000:
                y = random.choice(posiciones_y)
                lado = random.choice(["izq", "der"])
                x = -120 if lado == "izq" else ANCHO + 120
                vel = 3 if lado == "izq" else -3
                cerdos.append([cerdo_img.get_rect(topleft=(x, y)), vel])
                cerdo_generado += 1
                ultimo_cerdo = pygame.time.get_ticks()

            for c in cerdos[:]:
                c[0].x += c[1]
                if c[0].right < -200 or c[0].left > ANCHO + 200:
                    cerdos.remove(c)
                if aquiles_rect.colliderect(c[0]):
                    sonido_cerdo.play()
                    cerdos.remove(c)
                    score += 1

            if score >= 10:
                pantalla_victoria()
                return

            for rect, _ in cerdos:
                pantalla.blit(cerdo_img, rect.topleft)

            pantalla.blit(imgs[anim_index], aquiles_rect.topleft)
            pantalla.blit(fuente_titulo.render(f"Cerdos atrapados: {score}/10", True, GRIS), (20, 50))
            pantalla.blit(fuente_titulo.render(f"Tiempo: {segundos}", True, GRIS), (20, 20))
            pygame.display.flip()

    pantalla_inicio()
    jugar()

#---PANTALLA FINAL---
# --- Función de pantalla final ---
def pantalla_final():
    # --- Primera pantalla: video ---
    clip = VideoFileClip("static/final_final.mp4").resized((ANCHO, ALTO))
    video_surface = pygame.Surface((ANCHO, ALTO))
    texto_font = pygame.font.Font(None, 50)
    texto = texto_font.render("Haz click para continuar", True, (255, 255, 255))
    
    playing = True
    for frame in clip.iter_frames(fps=FPS, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                playing = False
                break
        
        if not playing:
            break

        # Convertir frame a superficie Pygame
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        pantalla.blit(frame_surface, (0,0))
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO - 100))
        pygame.display.update()
        reloj.tick(FPS)
    
    # --- Segunda pantalla: imagen de fondo ---
    pantalla_final = pygame.image.load("static/fotogrupal.png")
    pantalla_final = pygame.transform.scale(pantalla_final, (ANCHO, ALTO))
    pantalla2 = True
    while pantalla2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        pantalla.blit(pantalla_final, (0,0))
        pygame.display.update()
        reloj.tick(FPS)
        

pantalla_inicio_1()

pygame.quit()   
sys.exit()
