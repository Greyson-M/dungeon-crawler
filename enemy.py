import pygame
from settings import *
import time


class enemy():
    def __init__(self, current_map, env, pos = np.array([WIDTH/2 + 250, HEIGHT/2 + 100]), drop=None) -> None:
        self.frame = env.enemy_frames[0]
        
        self.current_map = current_map
        self.env = env
        
        self.health = 100
        self.damage = 10
        self.attack_cooldown = 1
        self.pos = pos
        self.drop = drop

        self.prevpos = self.pos.copy()

        self.speed = 1

        self.box = self.frame.get_rect(topleft=self.pos)

        self.attacked = False
        self.attack_time = time.time()

        self.vel = np.array([0, 0])


    def death(self):
        self.current_map.enemies.remove(self)

        self.frame = self.env.enemy_frames[1]

        if self.drop != None:
            self.env.p1.weapons.append(self.drop)

    def update(self):
        pos = self.pos
        self.vel = (self.pos - self.prevpos) *dt
        self.prevpos = pos.copy()

        self.box = self.frame.get_rect(topleft=self.pos)

        xdist = self.env.p1.pos[0] - self.pos[0]
        ydist = self.env.p1.pos[1] - self.pos[1]
        dirhat = np.array([xdist, ydist])/np.linalg.norm(np.array([xdist, ydist]))

        for id, coll in self.current_map.collide_group:
            if self.box.colliderect(coll):
                self.pos -= dirhat * self.speed

        if time.time() - self.attack_time > self.attack_cooldown:
            if self.box.colliderect(self.env.p1.box):
                self.env.p1.hit(self)
                self.attacked = True
                self.attack_time = time.time()
            

        self.pos += dirhat * self.speed

    def draw(self):
        if self.health < 1:
            self.death()

        self.update()

        self.env.WIN.blit(self.frame, self.pos)
        pygame.draw.rect(self.env.WIN, ((255, 0, 0)), self.box, 2)