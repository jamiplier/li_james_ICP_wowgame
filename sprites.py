import pygame as pg
from pygame.sprite import Sprite
from os import path
from settings import *

vec = pg.math.Vector2

def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite,group,dir):#function because a lotta things will use this
    if dir == 'x': #checking for x collisions
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect) #takes 4 args, last thing is a boolean confirming there was a collision
        if hits:
            #checks to see if we are to the left or right of the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx: #hit[0] > the first thing we hit, what did we just run into
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2 #the core mechanics for collision if collision, then my position of x will reposition
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect) #takes 4 args, last thing is a boolean confirming there was a collision
        if hits:
            #checks to see if we are to the left or right of the wall
            if hits[0].rect.centery > sprite.hit_rect.centery: #hit[0] > the first thing we hit, what did we just run into
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2 #the core mechanics for collision if collision, then my position of x will reposition
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    #defines a player class and initializes it
    def __init__ (self, game,x,y): #init only runs once
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT #will determine our hitbox for walls
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
  
    def get_keys(self):
        #reset v to zero
        #listen for events
        #self.vx, self.vy = 0,0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed() #the left key
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            #self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            #self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            #self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            #self.vy = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel.x *= 0.7071
            self.vel.y *= 0.7071

    def update(self):
        self.get_keys()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt #about framerates and updating every frame
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self,self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center
        

class Wall(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

class Mob(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.vx, self.vy = 100,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        if self.rect.x + 32 > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.y += TILESIZE
        self.x += self.vx * self.game.dt * self.speed
        self.rect.x = self.x
        #self.y += self.vy * self.game.dt * self.speed
        self.rect.y = self.y
