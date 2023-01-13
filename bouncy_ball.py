import pygame
from sys import exit

pygame.init()

displayInfo = pygame.display.Info()
screenWidth = displayInfo.current_w
screenHeight = displayInfo.current_h

displayWidth, displayHeight = (screenWidth-100, screenHeight-100)

display_surface = pygame.display.set_mode((displayWidth, displayHeight), pygame.RESIZABLE)
pygame.display.set_caption("Bouncing Ball")

clock = pygame.time.Clock()
fps = 60

#consts
GRAVITY = (0, -9.81)
BACKGROUND_COLOR = (255, 255, 255)
RED = (255, 0, 0)

class PhysicsObject():
    global friction
    global gravity

    def __init__(self, name, color, mass, position, velocity, acceleration, coefficient_restitution):
        self.name = name
        self.color = color

        self.m = mass
        self.position = position
        self.x = position[0]
        self.y = position[1]

        self.v = velocity
        self.vx = velocity[0]
        self.vy = velocity[1]

        self.a = acceleration
        self.ax = acceleration[0]
        self.ay = acceleration[1]

        self.e = coefficient_restitution

        self.size = self.m

    def update(self):
        if self.y >= displayHeight-self.size*2:
            if abs(self.vy) <= 0.5:
                self.vy = 0
            else:
                self.y = displayHeight-self.size*2-1
                self.vy = -self.e * self.vy
        if self.ax != 0:
            friction_force = friction*self.m*gravity[1]
            self.ax -= friction_force/self.m

        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        self.position = (self.x, self.y)
    
    def draw(self):
        self.update()
        pygame.draw.circle(display_surface, self.color, self.position, self.size, 0)

gravity = (0, 1)
friction = 1
ball = PhysicsObject("ball", RED, 50, (100, 100), (0,2), gravity, 0.5)

running = True

while running:
    time_scale = 1
    dt = clock.tick(fps * time_scale)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.vy = -25
            if event.key == pygame.K_LEFT:
                ball.ax = -1
            elif event.key == pygame.K_RIGHT:
                ball.ax = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ball.ax = 0

    display_surface.fill(BACKGROUND_COLOR)
    ball.draw()

    pygame.display.flip()

pygame.quit()