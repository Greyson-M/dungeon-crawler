import pygame
import math
import time
from random import randint
import numpy as np
from pytmx.util_pygame import load_pygame
from settings import *
from utils import *
from enemy import *
from player import *
from gun import *


class Environment():
    def __init__(self) -> None:
        #load
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIN.fill((217, 217, 217))

        

        self.sysfont = pygame.font.get_default_font()
        self.t0 = time.time()
        self.font = pygame.font.SysFont(None, 18)

        self.sprite_sheet_image = pygame.image.load("assets/sprites/Male 01-1_STRIP.png").convert_alpha()
        self.emnemy_sheet_image = pygame.image.load("assets/sprites/mob_strip.png").convert_alpha()
        self.gun_image = pygame.image.load("assets/sprites/gun.png").convert_alpha()
        self.gun_image = pygame.transform.scale(self.gun_image, (64, 64))
        self.gun_imageFLIP = pygame.transform.flip(self.gun_image, True, False)

        self.deag_img = pygame.image.load("assets/sprites/deagle.png").convert_alpha()
        self.deag_img = pygame.transform.scale(self.deag_img, (64, 64))


        self.character_frames = []
        self.enemy_frames = []

        for i in range(2):
            self.enemy_frames.append(get_sprite(self.emnemy_sheet_image, i, 32, 32, scale=2))

        for i in range(12):
            self.character_frames.append(get_sprite(self.sprite_sheet_image, i, 32, 32, scale=2))

        self.tmx_data = load_pygame('assets/maps/testmap.tmx')
        self.test_map = load_pygame('assets/maps/testmap.tmx')
        self.greymap = load_pygame('assets/maps/greymap.tmx')

        self.current_map = map(self)
        self.current_map.load(self.test_map)

        self.p1 = player(self.current_map, self)

        self.item_dict = {0: gun(self.p1, self.current_map, self), 1: deagle(self.p1, self.current_map, self)}

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

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups=None, scale=1):
        super().__init__(groups)
        self.image = pygame.transform.scale(surf, (16*scale, 16*scale))
        self.rect = self.image.get_rect(topleft=(pos[0]*scale, pos[1]*scale))

class map():
    def __init__(self, env, scale=2) -> None:
        self.sprite_group = pygame.sprite.Group()
        self.scale = scale
        self.collide_group = []
        self.portal_group = []
        self.chest_group = []
        self.enemies = []
        self.spawns = {}

        self.name = 0

        self.env = env



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
                    self.enemies.append(enemy(self, self.env, np.array([object.x * self.scale, object.y * self.scale]), drop))
                else: 
                    self.enemies.append(enemy(self, self.env, np.array([object.x * self.scale, object.y * self.scale])))

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
