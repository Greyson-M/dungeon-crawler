import pygame
import math
import time
from random import randint
import numpy as np
from pytmx.util_pygame import load_pygame
from settings import *
from environment import Environment
from utils import *
from enemy import enemy


pi = math.pi

environment = Environment()


def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    prevt = 0
    frames = 0
    environment.WIN.fill((217, 217, 217))
    pygame.display.flip()

    direction = 0
    movV = [False, False]
    movH = [False, False]
    mov = [False, False, False, False]

    while running:
        clock.tick(FPS)
        prevt += (1/FPS)
        t += (1/FPS)
        frames += 1
        tick = frames/15

        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        MousePos = np.array((Mouse_x, Mouse_y))

        for event in pygame.event.get():
#check for quit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

#check for keypresses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction = 0
                    movV[0] = True
                    mov[0] = True
                if event.key == pygame.K_s:
                    movV[1] = True
                    mov[1] = True
                    direction = 1
                if event.key == pygame.K_a:
                    movH[0] = True
                    mov[2] = True
                    direction = 2
                if event.key == pygame.K_d:
                    movH[1] = True
                    mov[3] = True
                    direction = 3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    movV[0] = False
                    mov[0] = False
                if event.key == pygame.K_s:
                    movV[1] = False
                    mov[1] = False
                if event.key == pygame.K_a:
                    movH[0] = False
                    mov[2] = False
                if event.key == pygame.K_d:
                    movH[1] = False
                    mov[3] = False

                if event.key == pygame.K_r:
                    environment.p1.equipped_weapon.reload()

                if event.key == pygame.K_1:
                    environment.p1.equipped_slot = 0
                if event.key == pygame.K_2:
                    environment.p1.equipped_slot = 1
                if event.key == pygame.K_3:
                    environment.p1.equipped_slot = 2

                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    environment.p1.equipped_weapon.attack()

        environment.current_map.sprite_group.draw(environment.WIN)

        '''
        if True in movV:
            p1.moveVert(movV)
        if True in movH:
            p1.moveHorz(movH)
        
        '''

        if True in mov:
            environment.p1.move(mov, frames)

        environment.p1.draw(mouse_pos=MousePos)

        if frames % 15 == 0:
            #p1.updateVel()
            pass


        i=0
        #print (len(p1.equipped_weapon.fired_shots))
        for bul in environment.p1.equipped_weapon.fired_shots:
            bul.update()
            if bul.destroyed: 
                environment.p1.equipped_weapon.fired_shots.pop(i)
                
            i+=1


        for enemy in environment.current_map.enemies:
            enemy.draw()


        
        pygame.display.update()     #update screen
        environment.WIN.fill((217,217,217))     #clear prev frame

if __name__ == "__main__":
    main()
