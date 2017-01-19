#!/usr/bin python2
# -*- coding: utf-8 -*-


from __future__ import print_function
import pygame
import random
import serial
import time

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
grey = (220, 220, 220)
red = (255, 0, 0)

pos_x = display_width/4
pos_y = display_width/4.5

screen = pygame.display.set_mode((display_width, display_height))

nCeldas = 0
speed = 0
distance = 0

dFrente = 0
dIzq = 0
dDrcha = 0


#############################################################
# Connection with bluetooh
#############################################################
time.sleep(1)
ser = serial.Serial('/dev/rfcomm0', 9600)
# ser = serial.Serial('/dev/pts/1', 9600)
ser.write('a')
#############################################################


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


# Print text updating the screen


def message_display(size=50, txt1=None, txt2=None, txt3=None, txt4=None,
                    txt5=None, txt6=None, txt7=None):

    x = display_width / 2
    y = display_height / 2

    font = pygame.font.Font(None, size)

    # Clean screen
    screen.fill(grey)

    TextSurf1, TextRect1 = text_objects(txt1, font)
    TextRect1.center = (x, y - size)
    TextSurf2, TextRect2 = text_objects(txt2, font)
    TextRect2.center = (x, y)
    TextSurf3, TextRect3 = text_objects(txt3, font)
    TextRect3.center = (x, y + size)
    TextSurf4, TextRect4 = text_objects(txt4, font)
    TextRect4.center = (x, y + size * 2)
    TextSurf5, TextRect5 = text_objects(txt5, font)
    TextRect5.center = (x, y + size * 3)
    TextSurf6, TextRect6 = text_objects(txt6, font)
    TextRect6.center = (x, y + size * 4)

    TextSurf7, TextRect7 = text_objects(txt7, font)
    TextRect7.center = (x, y - size * 5)

    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)
    screen.blit(TextSurf5, TextRect5)
    screen.blit(TextSurf6, TextRect6)
    screen.blit(TextSurf7, TextRect7)

    pygame.display.update()


# The 'square robot' copy itself X and Y position in the screen.


def move_robot(x1=2, y1=2):
    global pos_x, pos_y

    pos_x = x1
    pos_y = y1
    background = pygame.display.get_surface()

    robot = pygame.image.load("cuadrado.png")
    robot_pos = ((pos_x), (pos_y))
    background.blit(robot, robot_pos)

    pygame.display.update()


# F1 option.


def map_data():

    # ABAJO IZQ UP DRCH
    l = [0, 1, 2, 3]
    active = l[0]

    message_display()
    while not pygame.event.get(pygame.QUIT):
        pygame.display.set_caption('Mapa del robot')

        # Initial map
        move_robot(pos_x, pos_y)

        input1 = ser.readline().strip()

        if '+' in input1:  # UP Send '+'
            if active == 0:
                move_robot(pos_x, pos_y+0.15)
            elif active == 1:
                move_robot(pos_x-0.15, pos_y)
            elif active == 2:
                move_robot(pos_x, pos_y-0.15)
            elif active == 3:
                move_robot(pos_x+0.15, pos_y)
        elif '*' in input1:  # RIGHT Send '*'
            active = l[(active + 1) % len(l)]
        elif '/' in input1:  # LEFT Send '/'
            active = l[(active - 1) % len(l)]


# F2 option


def read_serial():
    global nCeldas, speed, distance
    global dFrente, dIzq, dDrcha

    pygame.display.set_caption('Datos del robot')

    while not pygame.event.get(pygame.QUIT):
        input1 = ser.readline().strip()

        if 'nCeldas' in input1:# Send 'nCeldas'
            nCeldas += 1
            distance += 20
        elif '+' in input1:
            speed = ("%0.2f" % random.uniform(20.0, 20.5))
        elif '$' in input1:  # Send $
            speed = 0
        elif '@' in input1:  # Send @X@Y@Z
            if len(input1) > 2:
                print(input1)
                dFrente = input1.split('@')[1]
                dDrcha = input1.split('@')[2]
                if dDrcha == '0.00':
                    dDrcha = '[no hay].'
                dIzq = input1.split('@')[3]
                if dIzq == '0.00':
                    dIzq = '[no hay].'

        message_display(50, 'nCeldas recorridas: '+str(nCeldas),
                        'Velocidad: '+str(speed)+'cm/s',
                        'Distancia recorrida: '+str(distance)+'cm',
                        'Distancia a obstaculo frente: '+str(dFrente),
                        'Distancia a obstaculo derecha: '+str(dDrcha),
                        'Distancia a obstaculo izquierda: '+str(dIzq),
                        'Tiempo: '+str(pygame.time.get_ticks()/1000)+' s')


# Main menu


def main():
    pygame.init()
    message_display(50, "Conectando bluetooh...")

    while not pygame.event.get(pygame.QUIT):
        for event in pygame.event.get():
            pygame.display.set_caption('Menu principal')
            message_display(50, "F1. Recorrido en el laberinto.",
                            "F2. Numero de celdas recorridas.")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    map_data()
                elif event.key == pygame.K_F2:
                    read_serial()

if __name__ == '__main__':
    main()
    ser.close()
