import pygame
import math
pygame.font.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont("", 20)

pygame.init()
width = 1400
height = 700
main_s = pygame.display.set_mode((width, height))


def deg_to_rad(degrees):
    return degrees / 180.0 * math.pi
def rad_to_deg(radians):
    return radians *180.0/ math.pi