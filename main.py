#this file was created by James Li
#code inspired by Chris Bradfield who was inspired by Notch
'''
Data types: boolean, JSON strings, integers
Input (events): keyboard, mouse, voice, power button, eye tracking, camera, gyroscoping, location

Process: cursor position, position of the player, score, enemy

Output: Graphics  Sounds: jump, power up, walking, haptics (controller shaking)
'''
import pygame as pg
from os import path
from settings import * #impot * imports everything
from sprites import *
from utils import *
#using a class to organize objects
#e.g. factory is the class, water bottle is the product, the object
class Game:
    def __init__(self): #means initiate, to allow properties to be defined
        pg.init() #initialize pygame
        pg.mixer.init() # initialize the pygame sound
        self.screen = pg.display.set_mode((WIDTH,HEIGHT)) #create the canvas
        print('game initialized')
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
    def load_data(self,map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')#join one path to another
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.map = Map(path.join(self.game_dir,map))
    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        #self.player = Player(self,12,12) 
        self.cactus = Wall(self,10,10)
        self.enemy = Mob(self,12,12)

        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'P':
                    Player(self,col,row)
        # puts the player at 0,0, we're putting self in here because its the argument for game
        #self is game 
        #self.all_sprites.add(self.player) #draws the player

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 
            self.events()
            self.update() #allows the game to update all movements and player position
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False #creates a quit mechanism 
                self.running = False
    

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen) #draws our player
        pg.display.flip()



if __name__ == "__main__": # if 'main' is the name of file the underscores indicate something is special
    g = Game()
     

while g.running:
    g.new()
    g.run() #makes sure the game actually runs when we want it to run
