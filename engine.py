import numpy as np
import pygame
from sys import exit

#Initializing Parameters
pygame.init()

displayInfo = pygame.display.Info()
screenWidth = displayInfo.current_w
screenHeight = displayInfo.current_h

display_surface = pygame.display.set_mode((screenWidth, screenHeight-50), pygame.RESIZABLE)
pygame.display.set_caption("Python Physics Engine")

clock = pygame.time.Clock()
fps_limit = 60

backgroundColor = (255,255,255)
objectList = []

class PhysicsObject():
    global objectList

    def convert(self, measurement):
        return int(measurement)*self.conversion_factor

    def __init__(self, x, y, width, height, mass, velocity, acceleration, max_velocity):
        self.conversion_factor = 50 #meaning 50 px = 1m

        self.x = round(x)
        self.y = round(y)
        self.width = self.convert(width)
        self.height = self.convert(height)
        self.mass = mass
        self.velocity = (self.convert(velocity[0]), self.convert(velocity[1]))
        self.acceleration = (self.convert(acceleration[0]), self.convert(acceleration[1]))
        self.max_velocity = (self.convert(max_velocity[0]), self.convert(max_velocity[1]))
        self.color = (255,0,0)
        self.objectRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.canCollide = True
        
    def update(self, dt):
        #updating velocity
        self.velocity = (int(self.velocity[0] + self.acceleration[0] * dt),
                         int(self.velocity[1] + self.acceleration[1] * dt))
        
        #ensuring velocity doesn't go past maximum
        self.velocity = (min(self.velocity[0], self.max_velocity[0]),
                         min(self.velocity[1], self.max_velocity[1]))

        #updating position
        self.x += int(self.velocity[0] * dt)
        self.y += int(self.velocity[1] * dt)

        #checking that object won't go off screen
        screenWidth, screenHeight = display_surface.get_size()

        if self.x < 0:
            self.x = 0
            self.velocity = (-self.velocity[0], self.velocity[1])
        elif self.x + self.width > screenWidth:
            self.x = screenWidth - self.width
            self.velocity = (-self.velocity[0], self.velocity[1])
        
        if self.y < 0:
            self.y = 0
            self.velocity = (self.velocity[0], -self.velocity[1])
        elif self.y + self.height > screenHeight:
            self.y = screenHeight - self.height
            self.velocity = (self.velocity[0], -self.velocity[1])

        self.objectRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.checkPixels()

    def draw(self):
        self.objectRect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(display_surface, self.color, self.objectRect, 0, 1)

    def set_color(self, color):
        self.color = color

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def change_collision_status(self):
        self.canCollide = not self.canCollide
        print("Can collide: ", self.canCollide)

    def checkPixels(self):
        self.x = round(self.x)
        self.y = round(self.y)


def collisionHandler():
    global objectList
    for object in objectList:
        for object2 in objectList:
            if object != object2 and object.objectRect.colliderect(object2.objectRect) and object.canCollide and object2.canCollide:
                calculateCollision(object, object2)

def calculateCollision(object1b, object2b):
    object1b.canCollude = False
    object2b.canCollude = False

    m1 = object1b.mass
    m2 = object2b.mass
    v1x, v1y = object1b.velocity
    v2x, v2y = object2b.velocity

    v1xf = round(((m1-m2)/(m1+m2))*v1x + (2*m2/(m1+m2))*v2x)
    v2xf = round((2*m1/(m1+m2)) * v1x + ((m2-m1)/(m1+m2))*v2x)

    object1b.set_velocity((v1xf, v1y))
    object2b.set_velocity((v2xf, v2y))

    makeCollisions(object1b, object2b)

def makeCollisions(object1a, object2a):
    distance = np.sqrt((object1a.x-object2a.x)**2 + (object1a.y-object2a.y)**2)

gravity = (0, 0)

#input parameters in SI units, class will handle conversion
testObject1 = PhysicsObject(100,             300, 1, 1, 1,  (3,0), gravity, (1000, 1000))
testObject2 = PhysicsObject(screenWidth-100, 275, 2, 2, 100, (-3, 0), gravity, (1000,1000))

testObject2.set_color((0,255,0))

objectList = [testObject1, testObject2]

running = True
#main game loop
while running:
    time_scale =  1e-3
    dt = clock.tick(fps_limit) * time_scale

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

        elif event.type == pygame.VIDEORESIZE:
            display_surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    collisionHandler()
    testObject1.update(dt)
    testObject2.update(dt)
    display_surface.fill(backgroundColor)
    testObject1.draw()
    testObject2.draw()
    
    pygame.time.delay(int(1000/fps_limit))
    pygame.display.flip()

pygame.quit()