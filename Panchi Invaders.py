import pygame
import random
import math
from pygame import mixer
#Inicializar Pygame
pygame.init()


#Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

#Titulo e icono
pygame.display.set_caption('Panchi Invaders')
icono = pygame.image.load('panchi.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('background.jpg')

#Agregar musica
mixer.music.load('MusicGame.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.6)

#Variables del jugador
img_jugador = pygame.image.load('starship.png')
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0

#Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 10

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('enemy.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(1)
    enemigo_y_cambio.append(50)

#Variables de bullet
img_bullet = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 536
bullet_x_cambio = 0
bullet_y_cambio = 2
bullet_visible = False

#Score
score = 0
fuente = pygame.font.Font('m04.TTF', 32)
text_x = 10
text_y = 10

#Funcion Score
def mostrar_score(x, y):
    text = fuente.render(f'Score: {score}', True, (255, 255, 0))
    pantalla.blit(text, (x, y))


#Mostrar score
#Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#Funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#Funcion bullet
def disparar_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    pantalla.blit(img_bullet, (x + 16, y + 10))

# Funcion colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2,2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta = True
while se_ejecuta:

    #Imagen de fondo
    pantalla.blit(fondo, (0,0))

    #Iterar eventos
    for evento in pygame.event.get():

        #Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                soundbullet = mixer.Sound('LaserGun.mp3')
                mixer.music.set_volume(0.1)
                soundbullet.play()
                if not bullet_visible:
                    bullet_x = jugador_x
                    disparar_bullet(bullet_x, bullet_y)
        #Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #Modificar ubicacion
    jugador_x += jugador_x_cambio

    #Mantener dentro de bordes
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicacion enemiga
    for e in range(cantidad_enemigos):
        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener dentro de bordes enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

    #Movimiento bullet
        if bullet_y <= -57:
            bullet_y = 536
            bullet_visible = False
        if bullet_visible:
            disparar_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_cambio

    #Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bullet_x, bullet_y)
        if colision:
            soundenemy = mixer.Sound('ColisionEnemiga.mp3')
            mixer.music.set_volume(0.1)
            soundenemy.play()
            bullet_y = 536
            bullet_visible = False
            score +=1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)


    jugador(jugador_x, jugador_y)
    mostrar_score(text_x, text_y)
    #Actualizar cambios
    pygame.display.update()


