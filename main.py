import pygame
import math
import time
from random import randint
import numpy as np

#GAME constants
FPS = 60
WIDTH, HEIGHT = 1280, 720
CENTER = np.array([WIDTH/2, HEIGHT/2])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dt = (1/FPS)


pi = math.pi


#load
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill((217, 217, 217))

sysfont = pygame.font.get_default_font()
t0 = time.time()
font = pygame.font.SysFont(None, 18)

#UTILIY FUNCTIONS
def pythag (vector):
    a = (vector[0]**2) + (vector[1]**2)
    return math.sqrt(a)

def distance (vec1, vec2):
    xdis = vec2[0] - vec1[0]
    ydis = vec2[1] - vec1[1]
    return pythag([xdis, ydis])


class player():
    
    def __init__(self) -> None:
        self.pos = CENTER
        self.speed = 5
        
        pass

    def draw(self):
        pygame.draw.circle(WIN, WHITE, self.pos, 20)

    def move(self, up=False, down=False, left=False, right=False):

        if up:
            self.pos[1] -= self.speed
        if down:
            self.pos[1] += self.speed
        if left:
            self.pos[0] -= self.speed
        if right:
            self.pos[0] += self.speed

p1 = player()




def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    prevt = 0
    WIN.fill((217, 217, 217))
    pygame.display.flip()

    mov_up = False
    mov_down = False
    mov_left = False
    mov_right = False

    while running:
        clock.tick(FPS)
        prevt += (1/FPS)
        t += (1/FPS)

        Mouse_x, Mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
#check for quit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

#check for keypresses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    mov_up = True
                if event.key == pygame.K_s:
                    mov_down = True
                if event.key == pygame.K_a:
                    mov_left = True
                if event.key == pygame.K_d:
                    mov_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    mov_up = False
                if event.key == pygame.K_s:
                    mov_down = False
                if event.key == pygame.K_a:
                    mov_left = False
                if event.key == pygame.K_d:
                    mov_right = False

        p1.move(up=mov_up, down=mov_down, left=mov_left, right=mov_right)
        p1.draw()
        
        pygame.display.update()     #update screen
        WIN.fill((217,217,217))     #clear prev frame

if __name__ == "__main__":
    main()
