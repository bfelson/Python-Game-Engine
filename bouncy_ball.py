import pygame
from sys import exit

pygame.init()

displayInfo = pygame.display.Info()
screenWidth = displayInfo.current_w
screenHeight = displayInfo.current_h

display_surface = pygame.display.set_mode((screenWidth-100, screenHeight-100), pygame.RESIZABLE)
pygame.display.set_caption("Bouncing Ball")

clock = pygame.time.Clock()
fps = 60

#consts
GRAVITY = (0, -9.81)
BACKGROUND_COLOR = (255, 255, 255)
RED = (255, 0, 0)

class PhysicsObject():
    def __init__(self, name, color, mass, position, velocity, coefficient_restitution):
        self.name = name
        self.color = color

        self.m = mass
        self.position = position
        self.x = position[0]
        self.y = position[1]

        self.v = velocity
        self.vx = velocity[0]
        self.vy = velocity[1]

        self.e = coefficient_restitution
    
    def draw(self):
        pygame.draw.circle(display_surface, self.color, self.position, self.m, 0)

ball = PhysicsObject("ball", RED, 50, (100, 100), (0,0), 0.5)

running = True

while running:
    time_scale = 1
    dt = clock.tick(fps * time_scale)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    display_surface.fill(BACKGROUND_COLOR)
    ball.draw()

    pygame.display.flip()

pygame.quit()