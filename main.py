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
test_map = load_pygame('assets/maps/testmap.tmx')
greymap = load_pygame('assets/maps/greymap.tmx')

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
emnemy_sheet_image = pygame.image.load("assets/sprites/mob_strip.png").convert_alpha()
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
enemy_frames = []

for i in range(2):
    enemy_frames.append(get_sprite(emnemy_sheet_image, i, 32, 32, scale=2))

for i in range(12):
    character_frames.append(get_sprite(sprite_sheet_image, i, 32, 32, scale=2))

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups=None, scale=1):
        super().__init__(groups)
        self.image = pygame.transform.scale(surf, (16*scale, 16*scale))
        self.rect = self.image.get_rect(topleft=(pos[0]*scale, pos[1]*scale))

'''
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
'''

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
    
    def __init__(self, current_map) -> None:
        self.current_map = current_map

        self.pos = CENTER
        self.speed = 4
        self.direction = 0
        self.angle = 0
        self.vel = np.array([0, 0])
        self.prevpos = np.array([0, 0])
        
        self.start_frame = character_frames[1]
        self.frame = character_frames[1]
        self.box = self.frame.get_rect(topleft=self.pos)

        self.weapons = [gun(self, self.current_map)]
        self.equipped_slot = 0
        self.equipped_weapon = self.weapons[self.equipped_slot]
        
        self.health = 100
        self.max_health = 100

        self.character_frames = character_frames
        self.down_anim = animation(self.character_frames, 0, 2, 0)
        self.left_anim = animation(self.character_frames, 3, 5, 0)
        self.right_anim = animation(self.character_frames, 6, 8, 0)
        self.up_anim = animation(self.character_frames, 9, 11, 0)

        self.collide_dir = self.direction
         
        
        
        

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
        pos_disp = font.render("pos: {}".format(mouse_pos), True, BLACK)
        health_disp = font.render("health: {}".format(self.health), True, BLACK)

        pygame.draw.rect(WIN, ((50, 50, 50)), (275, 650, 400, 40))
        pygame.draw.rect(WIN, ((230, 20, 20)), (275, 650, self.health*4, 40))

        WIN.blit(health_disp, (280, 670))
        WIN.blit(pos_disp, (10, 20))

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
                    self.weapons.append(item_dict[item])


    def hit(self, enemy):
        self.health -= enemy.damage
        print ("health: ", self.health)
        self.pos += self.speed * (enemy.vel / pythag(enemy.vel)) * 2
        print ("vel: ", enemy.vel * 60)



class gun():
    def __init__(self, player, current_map) -> None:
        self.current_map = current_map

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
            self.ammo.append(bullet(self, "bullet {}".format(i), self.current_map))

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



        WIN.blit(self.frame, self.pos)

    def attack(self):

        if len(self.ammo) <= 1:
            self.empty = True


        if not self.empty and not self.ammo[-1].shot:
            self.ammo[-1].shoot()


    def reload(self):
        self.empty = False
        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i), self.current_map))


class deagle(gun):
    def __init__(self, player, current_map) -> None:
        super().__init__(player, current_map)
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

        self.frame = deag_img
        self.start_frame = deag_img
        self.start_frame_flip = pygame.transform.flip(deag_img, True, False)

        self.ammo = []
        for i in range(self.magazine_size):
            self.ammo.append(bullet(self, "bullet {}".format(i), self.current_map))

        self.fired_shots = []
        self.empty = False

        self.dirhat = np.array([0, -1])
        self.angle = 0

    
class bullet():
    def __init__(self, weapon, id, current_map) -> None:
        self.current_map = current_map
        self.weapon = weapon
        self.pos = weapon.barrel_pos
        self.bullet_speed = weapon.bullet_speed
        self.radius = weapon.caliber
        self.shot = False
        self.destroyed = False
        self.id = id
        self.box = pygame.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius*2, self.radius*2)
    
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

        pygame.draw.circle(WIN, BLACK, self.pos, self.radius)
        pygame.draw.rect(WIN, ((255, 0, 0)), self.box, 2)

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


class enemy():
    def __init__(self, current_map, pos = np.array([WIDTH/2 + 250, HEIGHT/2 + 100]), drop=None) -> None:
        self.frame = enemy_frames[0]
        
        self.current_map = current_map
        
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

        self.frame = enemy_frames[1]

        if self.drop != None:
            p1.weapons.append(self.drop)

    def update(self):
        pos = self.pos
        self.vel = (self.pos - self.prevpos) *dt
        self.prevpos = pos.copy()

        self.box = self.frame.get_rect(topleft=self.pos)

        xdist = p1.pos[0] - self.pos[0]
        ydist = p1.pos[1] - self.pos[1]
        dirhat = np.array([xdist, ydist])/np.linalg.norm(np.array([xdist, ydist]))

        for id, coll in self.current_map.collide_group:
            if self.box.colliderect(coll):
                self.pos -= dirhat * self.speed

        if time.time() - self.attack_time > self.attack_cooldown:
            if self.box.colliderect(p1.box):
                p1.hit(self)
                self.attacked = True
                self.attack_time = time.time()
            

        self.pos += dirhat * self.speed

    def draw(self):
        if self.health < 1:
            self.death()

        self.update()

        WIN.blit(self.frame, self.pos)
        pygame.draw.rect(WIN, ((255, 0, 0)), self.box, 2)


class portal():
    def __init__(self, path, rect, dir):
        self.box = rect
        self.dir = dir
        self.path = path

class chest():
        def __init__(self, pos, contents, rect, groups=None):
            self.pos = pos
            self.contents = contents
            self.box = rect
            self.opened = False
            

class map():
    def __init__(self, scale=2) -> None:
        self.sprite_group = pygame.sprite.Group()
        self.scale = scale
        self.collide_group = []
        self.portal_group = []
        self.chest_group = []
        self.enemies = []
        self.spawns = {}

        self.name = 0



    def load_map(self, map):
        self.sprite_group.empty()
        for layer in map.visible_layers:
            if hasattr(layer, "data"):
                for x, y, image in layer.tiles():
                    Tile((x*16, y*16), image, self.sprite_group, scale=self.scale)

        for g in map.objectgroups:
            print(g.name)

    def load_collide(self, map):
        self.collide_group = []
        for object in map.objects:
            if object.type == "wall":
                self.collide_group.append([object.name, pygame.Rect((object.x * self.scale, object.y*self.scale), (object.width*self.scale, object.height*self.scale))])

    def load_portals(self, map):
        self.portal_group = []
        for object in map.objects:
            if object.type == "portal":
                print (object.properties['direction'])
                self.portal_group.append(portal(object.name, pygame.Rect((object.x * self.scale, object.y*self.scale), (object.width*self.scale, object.height*self.scale)), object.properties['direction']))
                #self.portal_group.append([object.name, pygame.Rect((object.x * self.scale, object.y*self.scale), (object.width*self.scale, object.height*self.scale))])


    def load_spawn(self, map):
        for object in map.objects:
            if object.type == "spawn":
                self.spawns[object.properties['direction']] = np.array([object.x * self.scale, object.y * self.scale])


    def load_chests(self, map):
        self.chest_group = []
        for object in map.objects:
            if object.type == "chest":
                contents = object.properties['contents']
                self.chest_group.append(chest(np.array([object.x * self.scale, object.y * self.scale]), contents, pygame.Rect((object.x * self.scale, object.y*self.scale), (object.width*self.scale, object.height*self.scale))))


    def load_enemies(self, map):
        self.enemies = []
        for object in map.objects:
            if object.type == "enemy":
                if object.properties['hasDrop']:
                    drop = object.properties['drop']
                    self.enemies.append(enemy(self, np.array([object.x * self.scale, object.y * self.scale]), drop))
                else: 
                    self.enemies.append(enemy(self, np.array([object.x * self.scale, object.y * self.scale])))

    def load(self, map):
        self.sprite_group = pygame.sprite.Group()
        self.collide_group = []
        self.portal_group = []
        self.chest_group = []
        self.enemies = []
        self.spawns = {}

        self.name = 0

        self.load_map(map)
        self.load_collide(map)
        self.load_portals(map)
        self.load_spawn(map)
        self.load_chests(map)
        self.load_enemies(map)

        self.name = map

        return self

current_map = map()
current_map.load(test_map)



p1 = player(current_map)
item_dict = {0: gun(p1, current_map), 1: deagle(p1, current_map)}

#enemies = [enemy(drop=deagle(p1))]

#for i in range(5):
#    enemies.append(enemy((randint(0, WIDTH), randint(0, HEIGHT))))    

def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    prevt = 0
    frames = 0
    WIN.fill((217, 217, 217))
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

        current_map.sprite_group.draw(WIN)

        '''
        if True in movV:
            p1.moveVert(movV)
        if True in movH:
            p1.moveHorz(movH)
        
        '''

        if True in mov:
            p1.move(mov, frames)

        p1.draw(mouse_pos=MousePos)

        if frames % 15 == 0:
            #p1.updateVel()
            pass


        i=0
        #print (len(p1.equipped_weapon.fired_shots))
        for bul in p1.equipped_weapon.fired_shots:
            bul.update()
            if bul.destroyed: 
                p1.equipped_weapon.fired_shots.pop(i)
                
            i+=1


        for enemy in current_map.enemies:
            enemy.draw()


        
        pygame.display.update()     #update screen
        WIN.fill((217,217,217))     #clear prev frame

if __name__ == "__main__":
    main()
