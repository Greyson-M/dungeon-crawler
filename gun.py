import pygame
import numpy as np
import math
from settings import *


class gun():
    def __init__(self, player, current_map, env) -> None:
        self.current_map = current_map
        self.env = env

        self.name = "gun"
        self.magazine_size = 20
        self.reload_time = 1
        self.fire_rate = 0.1
        self.damage = 34
        self.bullet_speed = 10
        self.caliber = 2
        self.player = player
        self.pos = player.pos + np.array([0, -10])
        self.barrel_pos = self.pos + np.array([35, 35])
        self.frame = env.gun_image
        self.start_frame = env.gun_image
        self.start_frame_flip = pygame.transform.flip(env.gun_image, True, False)
        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i), self.current_map, env))

        self.fired_shots = []

        self.empty = False
        self.dirhat = np.array([0, -1])
        self.angle = 0

    def pointAt(self, mouse_pos):

        distx = mouse_pos[0] - self.pos[0]
        disty = mouse_pos[1] - self.pos[1]
        self.angle = math.atan2(disty, distx)
        self.angle_deg = self.angle * 180/pi

        #print (self.angle_deg)

        self.frame = pygame.transform.rotate(self.start_frame, -self.angle_deg).convert_alpha()
        
        if (self.angle_deg > -180 and self.angle_deg < -90) or (self.angle_deg > 90 and self.angle_deg < 180):
            self.frame = pygame.transform.rotate(self.start_frame_flip, -self.angle_deg - 180).convert_alpha()

    
    def draw(self):
        ammo_disp = self.env.font.render("Ammo: {}".format(len(self.ammo)-1), True, BLACK)
        self.env.WIN.blit(ammo_disp, (10, HEIGHT - 30))

        mouse_pos = pygame.mouse.get_pos()
        self.pointAt(mouse_pos=mouse_pos)
        
        self.pos = self.player.pos + np.array([0, -10])
        self.barrel_pos = self.pos + np.array([35, 35])



        self.env.WIN.blit(self.frame, self.pos)

    def attack(self):

        if len(self.ammo) <= 1:
            self.empty = True


        if not self.empty and not self.ammo[-1].shot:
            self.ammo[-1].shoot()


    def reload(self):
        self.empty = False
        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i), self.current_map, self.env))

class deagle(gun):
    def __init__(self, player, current_map, env) -> None:
        super().__init__(player, current_map, env)
        self.current_map = current_map

        self.name = "deagle"
        self.magazine_size = 8
        self.reload_time = 1
        self.fire_rate = 0.1
        self.damage = 55
        self.bullet_speed = 15
        self.caliber = 5

        self.player = player
        self.pos = player.pos + np.array([0, -10])
        self.barrel_pos = self.pos + np.array([35, 35])

        self.frame = env.deag_img
        self.start_frame = env.deag_img
        self.start_frame_flip = pygame.transform.flip(env.deag_img, True, False)

        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i), self.current_map, env))

        self.fired_shots = []
        self.empty = False

        self.dirhat = np.array([0, -1])
        self.angle = 0

    
class bullet():
    def __init__(self, weapon, id, current_map, env) -> None:
        self.current_map = current_map
        self.weapon = weapon
        self.pos = weapon.barrel_pos
        self.bullet_speed = weapon.bullet_speed
        self.radius = weapon.caliber
        self.shot = False
        self.destroyed = False
        self.id = id
        self.box = pygame.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius*2, self.radius*2)
        self.env = env
    
    def __del__(self):
        #print("bullet deleted")
        pass

    def shoot(self):
        self.shot = True
        self.pos = np.array((self.weapon.barrel_pos[0], self.weapon.barrel_pos[1]))
        self.pos = self.weapon.player.pos.copy()
        self.weapon.fired_shots.append(self)
        self.weapon.ammo.pop()
        self.dirhat = self.weapon.dirhat
        self.angle = self.weapon.angle

        

    def update(self):
        if self.shot:
            speedx = math.cos(self.angle) * self.bullet_speed
            speedy = math.sin(self.angle) * self.bullet_speed
            self.pos += np.array([speedx, speedy])
            self.hitDetect(self.current_map.enemies)
            self.box = pygame.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius*2, self.radius*2)

            for id, rect in self.current_map.collide_group:
                if self.box.colliderect(rect):
                    self.destroyed = True

            self.draw()
        else:
            self.pos = self.weapon.pos

    def draw(self):

        if self.pos[0] < 0 or self.pos[0] > WIDTH or self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.destroyed = True

        #print ("id: {} \t pos: {}".format(self.id, self.pos))

        pygame.draw.circle(self.env.WIN, BLACK, self.pos, self.radius)
        pygame.draw.rect(self.env.WIN, ((255, 0, 0)), self.box, 2)

    def hitDetect(self, enemies):
        for enemy in enemies:
            if self.box.colliderect(enemy.box):
                enemy.health -= self.weapon.damage
                self.destroyed = True
                print("hit enemy")
                print("enemy health: {}".format(enemy.health))
                print("enemy pos: {}".format(enemy.pos))
                print("bullet pos: {}".format(self.pos))
                print("distance: {}".format(np.linalg.norm(self.pos - enemy.pos)))
                print("")
