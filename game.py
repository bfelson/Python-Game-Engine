import numpy as np
import pygame
import sys, os

from pygame.locals import *
from pygame.color import THECOLORS

#Initialize environment
pygame.init()

#Making the screen
WIDTH = 800
HEIGHT = 600

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Program")
#pygame.display.set_icon() IMPLEMENT LATER

#Clock
clock = pygame.time.Clock()

#drawing
backgroundColor = (255,255,255)
display_surface.fill(backgroundColor)

#initializing variables
fps_limit = 60
time = 0.0

#getting to main loop
running = True

#variables -- not sure where to put yet
left_clicking = False
middle_clicking = False
right_clicking = False

#draw variables
shape = 'circle'
size = 10
currentColor = 'blue'

def draw():
    if shape == 'circle':
        pygame.draw.circle(display_surface, currentColor, mouse_position, size, 0)
    elif shape == 'rect':
        pygame.draw.rect(display_surface, currentColor, pygame.Rect(mouseX-size/2, mouseY-size/2, size, size))
    elif shape == 'triangle':
        points = [(mouseX-size/2, mouseY+size/2), (mouseX, mouseY-size/2), (mouseX+size/2, mouseY+size/2)]
        pygame.draw.polygon(display_surface, currentColor, points)
    
def drawButtons():
    global currentColor
    def colorButton(color, number):
        global currentColor
        y_location = 10+number*75
        baseButton = pygame.Rect(5, y_location-5, 60, 60)
        pygame.draw.rect(display_surface, 'gray', baseButton)
        pygame.draw.rect(display_surface, 'black', pygame.Rect(10, y_location, 50, 50))
        pygame.draw.circle(display_surface, color, (35, y_location+25), 20, 0)

        if baseButton.collidepoint(mouse_position) and left_clicking:
            currentColor = color

    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    for i in range(len(colors)):
        colorButton(colors[i], i)

    colorButton(backgroundColor, 5)

    def shapeButton(shapeType, number):
        global shape

        y_location = 10+number*75
        baseButton = pygame.Rect(WIDTH-65, y_location-5, 60, 60)
        pygame.draw.rect(display_surface, 'gray', baseButton)
        pygame.draw.rect(display_surface, 'black', pygame.Rect(WIDTH-60, y_location, 50, 50))
        if shapeType == 'circle':
            pygame.draw.circle(display_surface, 'gray', (WIDTH-35, y_location+25), 20, 0)
        elif shapeType == 'rect':
            pygame.draw.rect(display_surface, 'gray', pygame.Rect(WIDTH-50, y_location+10, 30, 30))
        elif shapeType == 'triangle':
            points = [(WIDTH-55, y_location+45), (WIDTH-35, y_location+5), (WIDTH-15, y_location+45)]
            pygame.draw.polygon(display_surface, 'gray', points)

        if baseButton.collidepoint(mouse_position) and left_clicking:
            shape = shapeType
    
    shapes = ['circle', 'rect', 'triangle']
    for i in range(len(shapes)):
        shapeButton(shapes[i], i)
        
slider_width = WIDTH/2
slider_height = HEIGHT/10
slider_x = WIDTH/4
slider_y = (8.5/10)*HEIGHT

knobX = slider_x+50
knobY = slider_y+slider_height/2+2
knobSize = slider_height/3

def drawSlider():
    global knobX, knobY, knobSize, size

    #background
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    pygame.draw.rect(display_surface, 'gray', slider_rect)

    #fake line for slider
    line_rect = pygame.Rect(slider_x+25, slider_y+slider_height/2, slider_width-50, 4)
    pygame.draw.rect(display_surface, 'black', line_rect)

    #knob
    knobPosition = (knobX, knobY)
    pygame.draw.circle(display_surface, 'white', knobPosition, knobSize, 0)

    knobHitbox = pygame.Rect(knobX-slider_height/3, slider_y+knobSize/2, knobSize*2.1, knobSize*2.1)
    #pygame.draw.rect(display_surface, 'red', knobHitbox)
    if knobHitbox.collidepoint(mouse_position) and left_clicking:
        knobX = mouseX

    #constrain knob position
    knobX = min(max(knobX, slider_x+knobSize/2), slider_x+slider_width-knobSize/2)

    #adjust size
    size = int((knobX - (slider_x+knobSize/2)) * (100 / (slider_width-knobSize)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()


        if event.type == MOUSEBUTTONDOWN:
            #if left click
            if event.button == 1:
                left_clicking = True
            #middle click
            elif event.button == 2:
                middle_clicking = True
            elif event.button == 3:
                right_clicking = True

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                left_clicking = False
            elif event.button == 2:
                middle_clicking = False
            elif event.button == 3:
                right_clicking = False

    mouse_position = pygame.mouse.get_pos()
    mouseX, mouseY = mouse_position
    #draw stuff

    drawButtons()
    drawSlider()

    if left_clicking and mouseX > 60+size and mouseX < WIDTH-60 and mouseY < HEIGHT-100:
        draw()

    pygame.display.update()