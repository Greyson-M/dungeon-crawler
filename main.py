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

sprite_sheet_image = pygame.image.load("assets/sprites/Male 01-1_STRIP.png").convert_alpha()
gun_image = pygame.image.load("assets/sprites/gun.png").convert_alpha()
gun_image = pygame.transform.scale(gun_image, (64, 64))
gun_imageFLIP = pygame.transform.flip(gun_image, True, False)

def get_sprite(sheet, frame, width, height, scale=1):
    sprite = pygame.Surface([width, height]).convert_alpha()
    sprite.blit(sheet, (0, 0), ((frame*width), 0, width,height))
    sprite = pygame.transform.scale(sprite, (width*scale, height*scale))
    sprite.set_colorkey(BLACK)
    return sprite

character_frames = []

for i in range(11):
    character_frames.append(get_sprite(sprite_sheet_image, i, 32, 32, scale=2))


class player():
    
    def __init__(self) -> None:
        self.pos = CENTER
        self.speed = 5
        self.frame = character_frames[1]
        self.direction = 0
        self.equipped_weapon = gun(self)
        self.health = 100
        self.max_health = 100

    def draw(self):
        WIN.blit(self.frame, self.pos)
        #pygame.draw.circle(WIN, WHITE, self.pos, 20)

        self.equipped_weapon.draw()

    def move(self, up=False, down=False, left=False, right=False):

        if up:
            self.pos[1] -= self.speed
            self.frame = character_frames[10]
            self.direction = 0
        if down:
            self.pos[1] += self.speed
            self.frame = character_frames[1]
            self.direction = 1
        if left:
            self.pos[0] -= self.speed
            self.frame = character_frames[4]
            self.direction = 2
        if right:
            self.pos[0] += self.speed
            self.frame = character_frames[7]
            self.direction = 3

class gun():
    def __init__(self, player) -> None:
        self.name = "gun"
        self.magazine_size = 10
        self.reload_time = 1
        self.fire_rate = 0.1
        self.damage = 10
        self.bullet_speed = 10
        self.player = player
        self.pos = player.pos + np.array([0, -10])
        self.sprite = gun_image
    
    def draw(self):
        if self.player.direction == 0:
            self.pos = self.player.pos + np.array([0, -35])         #up
            self.sprite = pygame.transform.rotate(gun_image, 90)
        if self.player.direction == 1:
            self.pos = self.player.pos + np.array([-15, 20])          #down
            self.sprite = pygame.transform.rotate(gun_image, 270)
        if self.player.direction == 2:
            self.pos = self.player.pos + np.array([-20, 10])         #left
            self.sprite = gun_imageFLIP
        if self.player.direction == 3:
            self.pos = self.player.pos + np.array([25, 10])          #right
            self.sprite = pygame.transform.rotate(gun_image, 0)


        WIN.blit(self.sprite, self.pos)

    def attack(self):
        print("attack")
        

    


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
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    p1.equipped_weapon.attack()

        p1.move(up=mov_up, down=mov_down, left=mov_left, right=mov_right)
        p1.draw()
        
        pygame.display.update()     #update screen
        WIN.fill((217,217,217))     #clear prev frame

if __name__ == "__main__":
    main()
