import pygame as pg
from settings import *
from math import floor

class Map:
    def __init__(self,filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert() #loading an image, converting png to something pygame can use
 
    def get_image(self,x,y,width,height): #gets images from the Spritesheet and scales it correctly so we can draw and use our image from the spritesheet
        image = pg.Surface((width,height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        new_image = pg.transform.scale(image, (width,height))
        image = new_image
        return image


class Cooldown: # what checks time between different events
    def __init__(self):
        self.event_time = 0
        self.current_time  = 0
        self.delta = 0
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time #when we check how much time has passed
    def start(self):
        self.start_time = pg.time.get_ticks()
