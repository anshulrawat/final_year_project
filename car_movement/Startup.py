import pygame
import math
from random import *
pygame.font.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont("", 20)

pygame.init()
width = 1400
height = 700
main_s = pygame.display.set_mode((width, height))
source_ticket=[-1,-1,-1,-1]
destination_ticket=[-1,-1,-1,-1]
object_colors=[(200,155,0),(0,255,255),(255,0,255),(200,200,100)]

def deg_to_rad(degrees):
    return degrees / 180.0 * math.pi
def rad_to_deg(radians):
    return radians *180.0/ math.pi
def generate_source():
    i=randint(0,3)
    while(source_ticket[i]!=-1):
        i = randint(0, 3)
    source_ticket[i]=0
    return i
def generate_destination():
    i=randint(0,3)
    while(destination_ticket[i]!=-1):
        i = randint(0, 3)
    destination_ticket[i]=0
    return i
