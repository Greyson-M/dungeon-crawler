from settings import *
import pygame
import numpy as np
from utils import *
from pytmx.util_pygame import load_pygame
from gun import gun

class animation():
    def __init__(self, set, start, stop, frame) -> None:
        self.set = set
        self.start = start
        self.stop = stop

        self.frame = start
        self.last_tick = frame-1

    def nextFrame(self, tick):
        #print (self.frame)
        slide = self.set[self.frame]
        if tick != self.last_tick:
            if tick % 15 == 0:
                self.frame += 1
                if self.frame > self.stop:
                    self.frame = self.start

                #print (self.frame)

                slide = self.set[self.frame]
                

            self.last_tick = tick

        else: return self.set[self.frame]

        return slide

class player():
    
    def __init__(self, current_map, env) -> None:
        self.current_map = current_map

        self.pos = CENTER
        self.speed = 4
        self.direction = 0
        self.angle = 0
        self.vel = np.array([0, 0])
        self.prevpos = np.array([0, 0])
        
        self.start_frame = env.character_frames[1]
        self.frame = env.character_frames[1]
        self.box = self.frame.get_rect(topleft=self.pos)

        self.weapons = [gun(self, self.current_map, env)]
        self.equipped_slot = 0
        self.equipped_weapon = self.weapons[self.equipped_slot]
        
        self.health = 100
        self.max_health = 100

        self.character_frames = env.character_frames
        self.down_anim = animation(self.character_frames, 0, 2, 0)
        self.left_anim = animation(self.character_frames, 3, 5, 0)
        self.right_anim = animation(self.character_frames, 6, 8, 0)
        self.up_anim = animation(self.character_frames, 9, 11, 0)

        self.collide_dir = self.direction
         
        self.env = env       
        

    def pointAt(self, mouse_pos):
        direction = pygame.math.Vector2(mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])
        angle = direction.angle_to((0, -1))
        self.frame = pygame.transform.rotate(self.start_frame, angle).convert_alpha()
    
    def updateVel(self):
        pos = self.pos
        #print (pos, self.prevpos)
        self.vel = (self.pos - self.prevpos) *dt
        self.prevpos = pos.copy()
        #print(self.vel)

    def draw(self, mouse_pos):
        pos_disp = self.env.font.render("pos: {}".format(mouse_pos), True, BLACK)
        health_disp = self.env.font.render("health: {}".format(self.health), True, BLACK)

        pygame.draw.rect(self.env.WIN, ((50, 50, 50)), (275, 650, 400, 40))
        pygame.draw.rect(self.env.WIN, ((230, 20, 20)), (275, 650, self.health*4, 40))

        self.env.WIN.blit(health_disp, (280, 670))
        self.env.WIN.blit(pos_disp, (10, 20))

        if len(self.weapons) < self.equipped_slot+1:
            self.equipped_slot = 0
        else: self.equipped_weapon = self.weapons[self.equipped_slot]

        #self.pointAt(mouse_pos)

        self.env.WIN.blit(self.frame, self.pos)
        pygame.draw.rect(self.env.WIN, BLACK, self.frame.get_rect(topleft=self.pos), 1)
        #pygame.draw.circle(WIN, WHITE, self.pos, 20)

        self.equipped_weapon.draw()

        if self.equipped_slot == 0:
            pygame.draw.rect(self.env.WIN, (219, 172, 52), (100, HEIGHT-70, 50, 50), 3)
        else: pygame.draw.rect(self.env.WIN, BLACK, (100, HEIGHT-70, 50, 50), 3)

        if self.weapons:
            self.env.WIN.blit(self.weapons[0].start_frame, (90, HEIGHT-80))

        if self.equipped_slot == 1:
            pygame.draw.rect(self.env.WIN, (219, 172, 52), (152, HEIGHT-70, 50, 50), 3)
        else: pygame.draw.rect(self.env.WIN, BLACK, (152, HEIGHT-70, 50, 50), 3)

        if len(self.weapons) > 1 and self.weapons[1] != None:
            self.env.WIN.blit(self.weapons[1].start_frame, (148, HEIGHT-70))

        if self.equipped_slot == 2:
            pygame.draw.rect(self.env.WIN, (219, 172, 52), (203, HEIGHT-70, 50, 50), 3)
        else: pygame.draw.rect(self.env.WIN, BLACK, (203, HEIGHT-70, 50, 50), 3)
        if len(self.weapons) > 2 and self.weapons[2] != None:
            self.env.WIN.blit(self.weapons[2].start_frame, (190, HEIGHT-80))
        
        



    def move(self, movement, frame):
        vhat = self.vel / pythag(self.vel)

        self.vel = np.array([0, 0])
        directions = [[0, -self.speed], [0, self.speed], [-self.speed, 0], [self.speed, 0]]
        i=0
        for mov in movement:
            if mov:
                self.vel += np.array(directions[i])
                if i == 0:
                    self.frame = self.up_anim.nextFrame(frame)
                    self.direction = 0
                elif i == 1:
                    self.frame = self.down_anim.nextFrame(frame)
                    self.direction = 1
                elif i == 2:
                    self.frame = self.left_anim.nextFrame(frame)
                    self.direction = 2
                elif i == 3:
                    self.frame = self.right_anim.nextFrame(frame)
                    self.direction = 3
            i+=1

        self.pos += self.vel
        self.box = self.frame.get_rect(topleft=self.pos)

        for port in self.current_map.portal_group:
            map = load_pygame(port.path)
            if self.box.colliderect(port.box):

                direction = port.dir
                print("TELEPORTING to ", port.path)
                self.current_map = self.current_map.load(map)

                spawns = self.current_map.spawns

                self.pos = spawns[direction]

                print ("portals: ", self.current_map.portal_group)


        for id, rect in self.current_map.collide_group:
            if self.box.colliderect(rect):
                self.pos -= self.vel*1.1

                break

        for chest in self.current_map.chest_group:
            if self.box.colliderect(chest.box):
                if not chest.opened:
                    chest.opened = True
                    item = chest.contents
                    self.weapons.append(self.env.item_dict[item])


    def hit(self, enemy):
        self.health -= enemy.damage
        print ("health: ", self.health)
        self.pos += self.speed * (enemy.vel / pythag(enemy.vel)) * 2
        print ("vel: ", enemy.vel * 60)
