import pygame
import math
import time
from random import randint
import numpy as np
from pytmx.util_pygame import load_pygame

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

tmx_data = load_pygame('assets/maps/testmap.tmx')
#print(tmx_data.layers)

layer1 = tmx_data.layers[0]
print(layer1.tiles())

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

deag_img = pygame.image.load("assets/sprites/deagle.png").convert_alpha()
deag_img = pygame.transform.scale(deag_img, (64, 64))

def get_sprite(sheet, frame, width, height, scale=1):
    sprite = pygame.Surface([width, height]).convert_alpha()
    sprite.blit(sheet, (0, 0), ((frame*width), 0, width,height))
    sprite = pygame.transform.scale(sprite, (width*scale, height*scale))
    sprite.set_colorkey(BLACK)
    return sprite

character_frames = []

for i in range(11):
    character_frames.append(get_sprite(sprite_sheet_image, i, 32, 32, scale=2))

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups=None, scale=1):
        super().__init__(groups)
        self.image = pygame.transform.scale(surf, (16*scale, 16*scale))
        self.rect = self.image.get_rect(topleft=(pos[0]*scale, pos[1]*scale))

sprite_group = pygame.sprite.Group()

collide_group = []
scale = 2
for layer in tmx_data.visible_layers:
    if hasattr(layer, "data"):
        for x, y, image in layer.tiles():
            Tile((x*16, y*16), image, sprite_group, scale=scale)

for g in tmx_data.objectgroups:
    print(g.name)

for object in tmx_data.objects:
    collide_group.append([object.type, pygame.Rect((object.x * scale, object.y*scale), (object.width*scale, object.height*scale))])

print(collide_group)

class player():
    
    def __init__(self) -> None:
        self.pos = CENTER
        self.speed = 4
        self.direction = 0
        self.angle = 0
        self.vel = np.array([0, 0])
        self.prevpos = np.array([0, 0])
        
        self.start_frame = character_frames[1]
        self.frame = character_frames[1]
        self.box = self.frame.get_rect(topleft=self.pos)

        self.weapons = [gun(self)]
        self.equipped_slot = 0
        self.equipped_weapon = self.weapons[self.equipped_slot]
        
        self.health = 100
        self.max_health = 100
        
        

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
        

        if len(self.weapons) < self.equipped_slot+1:
            self.equipped_slot = 0
        else: self.equipped_weapon = self.weapons[self.equipped_slot]

        #self.pointAt(mouse_pos)

        WIN.blit(self.frame, self.pos)
        pygame.draw.rect(WIN, BLACK, self.frame.get_rect(topleft=self.pos), 1)
        #pygame.draw.circle(WIN, WHITE, self.pos, 20)

        self.equipped_weapon.draw()

        if self.equipped_slot == 0:
            pygame.draw.rect(WIN, (219, 172, 52), (100, HEIGHT-70, 50, 50), 3)
        else: pygame.draw.rect(WIN, BLACK, (100, HEIGHT-70, 50, 50), 3)

        if self.weapons:
            WIN.blit(self.weapons[0].start_frame, (90, HEIGHT-80))

        if self.equipped_slot == 1:
            pygame.draw.rect(WIN, (219, 172, 52), (152, HEIGHT-70, 50, 50), 3)
        else: pygame.draw.rect(WIN, BLACK, (152, HEIGHT-70, 50, 50), 3)

        if len(self.weapons) > 1 and self.weapons[1] != None:
            WIN.blit(self.weapons[1].start_frame, (148, HEIGHT-70))

        if self.equipped_slot == 2:
            pygame.draw.rect(WIN, (219, 172, 52), (203, HEIGHT-70, 50, 50), 3)
        else: pygame.draw.rect(WIN, BLACK, (203, HEIGHT-70, 50, 50), 3)
        if len(self.weapons) > 2 and self.weapons[2] != None:
            WIN.blit(self.weapons[2].start_frame, (190, HEIGHT-80))
        
        



    def move(self, up=False, down=False, left=False, right=False):
        self.box = self.frame.get_rect(topleft=self.pos + self.vel)
        vhat = self.vel / pythag(self.vel)
        
        '''
        for rect in collide_group:
            if rect.colliderect(self.box):
                print ("collide at {}".format(self.pos))
                self.pos -= vhat * self.speed
        '''


        if up:
            collision = False
            for id, rect in collide_group:
                if rect.colliderect(self.box):
                    if pythag(vhat) > 0 and id == 'top':
                        self.pos[1] += self.speed
                    #self.move(down=True)
                    collision = True
                    print ("collide at {}".format(id))
                    print (vhat)
            if not collision:
                self.pos[1] -= self.speed
                self.frame = character_frames[10]
                self.direction = 0

        if down:
            collision = False
            for id, rect in collide_group:
                if rect.colliderect(self.box):
                    if pythag(vhat) > 0 and id == 'bottom':
                        self.pos[1] -= self.speed
                    collision = True
                    print ("collide at {}".format(id))
            if not collision:
                self.pos[1] += self.speed
                self.frame = character_frames[1]
                self.direction = 1
        if left:
            collision = False
            for id, rect in collide_group:
                if rect.colliderect(self.box):
                    if pythag(vhat) > 0 and id == 'left':
                        self.pos[0] += self.speed
                    collision = True
                    print ("collide at {}".format(id))
            if not collision:
                self.pos[0] -= self.speed
                self.frame = character_frames[4]
                self.direction = 2
        if right:
            collision = False
            for id, rect in collide_group:
                if rect.colliderect(self.box):
                    if pythag(vhat) > 0 and id == 'right':
                        self.pos[0] -= self.speed
                    collision = True
                    print ("collide at {}".format(id))
            if not collision:
                self.pos[0] += self.speed
                self.frame = character_frames[7]
                self.direction = 3

class gun():
    def __init__(self, player) -> None:
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
        self.frame = gun_image
        self.start_frame = gun_image
        self.start_frame_flip = pygame.transform.flip(gun_image, True, False)
        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i)))

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
            #print ("flip")
            #self.frame = pygame.transform.rotate(self.frame, -180)
            self.frame = pygame.transform.rotate(self.start_frame_flip, -self.angle_deg - 180).convert_alpha()

    
    def draw(self):
        ammo_disp = font.render("Ammo: {}".format(len(self.ammo)-1), True, BLACK)
        WIN.blit(ammo_disp, (10, HEIGHT - 30))

        mouse_pos = pygame.mouse.get_pos()
        self.pointAt(mouse_pos=mouse_pos)
        
        self.pos = self.player.pos + np.array([0, -10])
        self.barrel_pos = self.pos + np.array([35, 35])



        '''
        if self.player.direction == 0:
            self.pos = self.player.pos + np.array([0, -35])         #up
            self.frame = pygame.transform.rotate(gun_image, 90)
            self.dirhat = np.array([0, -1])
        if self.player.direction == 1:
            self.pos = self.player.pos + np.array([-15, 20])          #down
            self.frame = pygame.transform.rotate(gun_image, 270)
            self.dirhat = np.array([0, 1])
        if self.player.direction == 2:
            self.pos = self.player.pos + np.array([-20, 10])         #left
            self.frame = gun_imageFLIP
            self.dirhat = np.array([-1, 0])
        if self.player.direction == 3:
            self.pos = self.player.pos + np.array([25, 10])          #right
            self.frame = pygame.transform.rotate(gun_image, 0)
            self.dirhat = np.array([1, 0])
        
        #distx = mouse_pos[0] - self.pos[0]
        #disty = mouse_pos[1] - self.pos[1]
        #self.angle = math.atan2(disty, distx)
        #self.dirhat = np.array((mouse_pos[0], mouse_pos[1])) / pythag(mouse_pos)
        #print ("dirhat: ", self.dirhat)
        '''

         


        WIN.blit(self.frame, self.pos)

    def attack(self):

        if len(self.ammo) <= 1:
            self.empty = True


        if not self.empty and not self.ammo[-1].shot:
            self.ammo[-1].shoot()

            print(self.ammo[-1].id)
        print (self.empty)
        print(len(self.ammo))

    def reload(self):
        self.empty = False
        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i)))


class deagle(gun):
    def __init__(self, player) -> None:
        super().__init__(player)
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

        self.frame = deag_img
        self.start_frame = deag_img
        self.start_frame_flip = pygame.transform.flip(deag_img, True, False)

        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i)))

        self.fired_shots = []
        self.empty = False

        self.dirhat = np.array([0, -1])
        self.angle = 0

    
class bullet():
    def __init__(self, weapon, id) -> None:
        self.weapon = weapon
        self.pos = weapon.barrel_pos
        self.bullet_speed = weapon.bullet_speed
        self.radius = weapon.caliber
        self.shot = False
        self.destroyed = False
        self.id = id

    
    def __del__(self):
        #print("bullet deleted")
        pass

    def shoot(self):
        self.shot = True
        self.pos = np.array((self.weapon.barrel_pos[0], self.weapon.barrel_pos[1]))
        self.weapon.fired_shots.append(self)
        self.weapon.ammo.pop()
        self.dirhat = self.weapon.dirhat
        self.angle = self.weapon.angle

    def update(self):
        if self.shot:
            speedx = math.cos(self.angle) * self.bullet_speed
            speedy = math.sin(self.angle) * self.bullet_speed
            self.pos += np.array([speedx, speedy])
            self.hitDetect(enemies)
            self.draw()
        else:
            self.pos = self.weapon.pos

    def draw(self):

        if self.pos[0] < 0 or self.pos[0] > WIDTH or self.pos[1] < 0 or self.pos[1] > HEIGHT:
            print("destroying bullet..")
            self.destroyed = True

        #print ("id: {} \t pos: {}".format(self.id, self.pos))

        pygame.draw.circle(WIN, BLACK, self.pos, self.radius)

    def hitDetect(self, enemies):
        for enemy in enemies:
            if np.linalg.norm(self.pos - enemy.pos) < self.radius + 20:
                enemy.health -= self.weapon.damage
                self.destroyed = True
                print("hit enemy")
                print("enemy health: {}".format(enemy.health))
                print("enemy pos: {}".format(enemy.pos))
                print("bullet pos: {}".format(self.pos))
                print("distance: {}".format(np.linalg.norm(self.pos - enemy.pos)))
                print("")


class enemy():
    def __init__(self, pos = np.array([WIDTH/2 + 250, HEIGHT/2 + 100]), drop=None) -> None:
        self.health = 100
        self.pos = pos
        self.drop = drop

    def death(self):
        enemies.remove(self)
        if self.drop != None:
            p1.weapons.append(self.drop)

    def draw(self):
        if self.health > 0:
            pygame.draw.circle(WIN, (((255/self.health), self.health * 2, 0)), self.pos, 20)
        else:
            self.death()
            
        
        
        

p1 = player()

enemies = [enemy(drop=deagle(p1))]

for i in range(5):
    enemies.append(enemy((randint(0, WIDTH), randint(0, HEIGHT))))    

def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    prevt = 0
    frames = 0
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
        frames += 1

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

                if event.key == pygame.K_r:
                    p1.equipped_weapon.reload()

                if event.key == pygame.K_1:
                    p1.equipped_slot = 0
                if event.key == pygame.K_2:
                    p1.equipped_slot = 1
                if event.key == pygame.K_3:
                    p1.equipped_slot = 2

                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    p1.equipped_weapon.attack()

        sprite_group.draw(WIN)

        p1.move(up=mov_up, down=mov_down, left=mov_left, right=mov_right)
        p1.draw(mouse_pos=MousePos)

        if frames % 15 == 0:
            p1.updateVel()


        i=0
        #print (len(p1.equipped_weapon.fired_shots))
        for bul in p1.equipped_weapon.fired_shots:
            bul.update()
            if bul.destroyed: 
                p1.equipped_weapon.fired_shots.pop(i)
                
            i+=1


        for enemy in enemies:
            enemy.draw()


        
        pygame.display.update()     #update screen
        WIN.fill((217,217,217))     #clear prev frame

if __name__ == "__main__":
    main()
