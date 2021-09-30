import sys
import pygame
from car import Car

# CONSTANTS:
scaling = 2
global WIDTH
SCREENSIZE = WIDTH, HEIGHT = 400*scaling,400*scaling
BLACK = (0, 0, 0)
GREY = (160, 160, 160)

dt = int(0.01 *1000)            # Time interval of simulations in milliseconds

# function to draw Map mentioned in the task
def makeMap(screen):
    map = pygame.image.load('map2.png')
    map = pygame.transform.scale(map, (WIDTH, HEIGHT))
    return map


def checkexit():
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

def draw_cars(car, screen):
    car.draw(screen)
    car.draw_lidar(screen)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((int(WIDTH),int(HEIGHT)))
    map = makeMap(screen)
    car = Car()
    
    ## Simulate the motion every dt seconds
    while (1):
        screen.blit(map, (0, 0))
        car.update(map)
        draw_cars(car, screen)
        clock.tick(0)
        pygame.time.delay(dt) # Simulate the car every dt  milliseconds
        pygame.display.update()
        
    checkexit()        