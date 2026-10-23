import pygame as pg
from pygame.sprite import Sprite
from os import path
from settings import *
from utils import *

vec = pg.math.Vector2

def collide_hit_rect(one,two): #checks if one thing is colliding with some other thing
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
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png")) #supposed to connect our game with the files of sprite sheet
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT #will determine our hitbox for walls
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        #following code is for animation
        self.last_update = 0
        self.current_frame = 0
        self.dir = "none"
        self.coins = 0
        print('player instantiated')
        print(self.pos)
  
    def get_keys(self):
        #reset v to zero
        #listen for events like pressing the key
        #self.vx, self.vy = 0,0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed() 
        if keys[pg.K_LEFT] or keys[pg.K_a]: #the left key
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

    def animate(self):
        #time element used
        now = pg.time.get_ticks()
        if self.dir == "none":
            if now - self.last_update > 350: #this periodically checks if we have made an update
                #if it has been 350ms and we haven't made an update, the game updates the sprite to make an animation
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE,TILESIZE), #checks the different locations of the spritesheet to generate animation
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE,TILESIZE)]
        self.run_frames = [self.spritesheet.get_image(0,0,TILESIZE,TILESIZE),
                           self.spritesheet.get_image(TILESIZE, 0,TILESIZE,TILESIZE)]


    def update(self):
        self.get_keys()
        self.animate()
        hits = pg.sprite.spritecollide(self,self.game.all_coins, True)
        if hits:
            for i in range(10):

                Particle(self.game, hits[0].pos.x, hits[0].pos.y)
            self.coins += 1
            self.game.pickup_snd.play() #play the audio 
            self.game.score += 1
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt #about framerates and updating every frame
        self.hit_rect.centerx = self.pos.x #i believe this begins the collision checking process during the game loop
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
class Particle(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/8,TILESIZE/8))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x 
        self.y = y 
        self.speed = 25
        self.rect.x = self.x
        self.rect.y = self.y
        self.countdown = Cooldown(5000)
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
    def update(self):
        self.countdown.ticking()
        self.rect.x += self.speed
        self.rect.y += self.speed
        if self.countdown.delta > 3:
            self.kill()
class Mob(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self,self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png")) #shares the same sprite sheet as the player
        self.load_images()
        self.image = pg.Surface((TILESIZE,TILESIZE))
        #self.image.fill(RED)
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.rect = self.image.get_rect()
        self.speed = 100
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.dir = "none"
        self.last_update = 0
        self.current_frame = 0
        self.hit_rect = MOB_HIT_RECT
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(64,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(96,0,TILESIZE, TILESIZE)
                            ]
        self.run_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), #similar mechanic
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]    
    def animate(self):
            now = pg.time.get_ticks()
            if self.dir == "none":
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                    bottom = self.rect.bottom
                    self.image = self.idle_frames[self.current_frame]
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            elif self.dir == "right":
                pass
    #used autocomplete by creating a chase method using pos vectors and obj as a parameter
    def chase(self, obj):
        if self.pos.x < obj.pos.x:
            self.vel.x = self.speed
            self.dir = "right"
        elif self.pos.x > obj.pos.x:
            self.vel.x = -self.speed
            self.dir = "left"
        else:
            self.vel.x = 0

        if self.pos.y < obj.pos.y:
            self.vel.y = self.speed
        elif self.pos.y > obj.pos.y:
            self.vel.y = -self.speed
        else:
            self.vel.y = 0

    def update(self):
        self.animate()
        if self.game.player:
            self.chase(self.game.player)
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

class Coin(Sprite):
    def __init__ (self, game,x,y): #reuse the init from the other classes for now
        coins_collected = 0 #a amethod for collection
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        
        self.image.set_colorkey(BLACK)
        self.pos = vec(x*TILESIZE, y*TILESIZE)


        self.rect.x = self.pos.x
        self.rect.x = self.pos.y

    def update(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
    


