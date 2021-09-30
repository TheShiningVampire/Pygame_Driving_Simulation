import pygame
from math import *
import numpy as np

# Paramters
scaling = 2
SCREENSIZE = WIDTH, HEIGHT = 400*scaling, 400*scaling
car_width = scaling * 15
car_length = scaling *15

K_theta = 1.5                   # Sensitivity with which omaega changes when the angle with least obstruction is detected


# lidar PARAMETERS
N = 7
d = 12*scaling
phi = 90

class Car:
    def __init__(self):
        self.surface = pygame.image.load("car.png")
        self.surface = pygame.transform.scale(self.surface, (car_width, car_length))
        self.rotate_surface = self.surface
        self.pos = [scaling * 50, WIDTH - scaling * 50]
        self.angle = 0
        self.speed = 7
        self.omega = 0
        self.center = [self.pos[0], self.pos[1]]
        self.lidars = []


    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
        self.draw_lidar(screen)

    def draw_lidar(self, screen):
        for r in self.lidars:
            pos, dist = r
            pygame.draw.line(screen, (0, 255, 0), (self.center[0]  , self.center[1] ), pos, 1)
            pygame.draw.circle(screen, (0, 255, 0), pos, 5)

    def check_lidar(self, degree, map):
        len = 0
        x = self.center[0] + cos(radians(360 -(self.angle + degree))) * len
        y = self.center[1] + sin(radians(360 -(self.angle + degree))) * len

        while not map.get_at((int(x),int(y)))== (0, 0, 0, 255) and len - car_length/2 < d:
            len = len + 0.1
            x = self.center[0] + cos(radians(360 -(self.angle + degree))) * len
            y = self.center[1] + sin(radians(360 -(self.angle + degree))) * len

            if (x>= WIDTH -1):
                x = WIDTH - 1
                break
            
            if (y>= HEIGHT -1):
                y = HEIGHT - 1
                break
            
        dist = (sqrt(pow(x - self.center[0], 2) + pow(y - self.center[1], 2)))
        self.lidars.append([(x, y), dist])


    def update(self, map):
        # check position
        self.rotate_surface = self.rot_center(self.surface, self.angle)

        self.pos[0] += cos(radians(360 - self.angle)) * self.speed
        self.pos[1] += sin(radians(360 - self.angle)) * self.speed
        
        # Modify the center
        self.center = [(self.pos[0]) +car_width/2 , (self.pos[1])+ car_length/2 ]

        #Get new readings from the lidar corresponding to the new center
        self.lidars.clear()
        angles = np.linspace(-int(phi/2) , int(phi/2), N)
        for angle in angles:
            self.check_lidar(angle, map)

        readings = self.get_data_from_lidar()
        self.determine_theta(readings)

    def get_data_from_lidar(self):
        lidars = self.lidars
        angles = np.linspace(-int(phi/2) , int(phi/2) , N)
        readings = {}
        for i,r in enumerate(lidars):
            readings[angles[i]] =  int(r[1]/scaling)
        return readings

    def determine_theta(self , readings):
        max_dist = 0
        min_dist = WIDTH
        least_hindered_angle = 0
        list_least_hindered_angles = []

    
        for angle , distance in readings.items():
            if (distance > max_dist):
                max_dist = distance
                least_hindered_angle = angle
                list_least_hindered_angles.clear()
                list_least_hindered_angles.append(angle)
            
            if (distance == max_dist):
                list_least_hindered_angles.append(angle)

            if (distance <= min_dist):
                min_dist = distance      

        if (max_dist == min_dist):
            least_hindered_angle = 0
        elif (min_dist <= d):  # In case the car is rubbing against the boundary, move the car away by making it turn in the direction away from 0 degree.
            # This is done by finding the weighted average of the angles which have minimum obstacle. The weights have been taken to be proportional to the 
            # square root of the angle
            sum_angle = 0
            for angle in list_least_hindered_angles:
                least_hindered_angle += angle*sqrt(abs(angle))
                sum_angle += sqrt(abs(angle))
            
            least_hindered_angle = least_hindered_angle/sum_angle
        
        self.omega = K_theta * least_hindered_angle
        self.angle += self.omega

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
