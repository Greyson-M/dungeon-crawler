import pygame
import math
from settings import *

#UTILIY FUNCTIONS
def pythag (vector):
    a = (vector[0]**2) + (vector[1]**2)
    return math.sqrt(a)

def distance (vec1, vec2):
    xdis = vec2[0] - vec1[0]
    ydis = vec2[1] - vec1[1]
    return pythag([xdis, ydis])



def get_sprite(sheet, frame, width, height, scale=1):
    sprite = pygame.Surface([width, height]).convert_alpha()
    sprite.blit(sheet, (0, 0), ((frame*width), 0, width,height))
    sprite = pygame.transform.scale(sprite, (width*scale, height*scale))
    sprite.set_colorkey(BLACK)
    return sprite