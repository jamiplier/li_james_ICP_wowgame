#this file was created by James Li
#code inspired by Chris Bradfield who was inspired by Notch
'''
Data types: boolean, JSON strings, integers
Input (events): keyboard, mouse, voice, power button, eye tracking, camera, gyroscoping, location

Process: cursor position, position of the player, score, enemy

Output: Graphics  Sounds: jump, power up, walking, haptics (controller shaking)


Game: CS2

Goals:
- plant the bomb and make sure it goes off
- diffuse the bomb
- eliminate all enemies

Rules:
- cannot leave map
- cannot see where other players are without audio cues
- you have to plant the bomb
- win in thirteen rounds


'''
import pygame as pg
from os import path
from settings import * #impot * imports everything
from sprites import *
from utils import *
#using a class to organize objects
#e.g. factory is the class, water bottle is the product, the object
class Game:
    def __init__(self): #means initiate, to allow properties to be defined and runs first
        pg.init() #initialize pygame
        pg.mixer.init() # initialize the pygame sound
        self.screen = pg.display.set_mode((WIDTH,HEIGHT)) #create the canvas
        print('game initialized')
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
    def load_data(self,map): #function responsible for opening up paths so we can access all the data
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')#join one path to another
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "wind1.wav"))
        self.map = Map(path.join(self.game_dir,map))

        
    def new(self): #where all our sprites and objects get instantiated
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        #self.player = Player(self,12,12) 
        #self.cactus = Wall(self,10,10)
        #self.enemy = Mob(self,12,12)

        #based on the tilemap generates the position for everything
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self,col,row) #we need this kind of instantiation to access all the variables within
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'M':
                    Mob(self,col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'C':
                    self.c = Coin(self,col,row)
        #have background music. The loops is equal to negative one to make it infinite
        #pg.mixer.music.load(path.join(self.snd_dir, ""))
        #pg.mixer.music.play(loops=-1)

        #self is game 
        #self.all_sprites.add(self.player) #draws the player and was shifted later

    def run(self): #the core loop of the game, checking events, updating, and drawing our sprites
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 
            self.events() #this checks for user input and also quitting
            self.update() #allows the game to update all movements and player position
            self.draw() #this handles the main graphics in the front end, update handles the back end logic

    def events(self): #quit mechanism
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False #creates a quit mechanism 
                self.running = False

    def draw_text(self,text, size, color, x, y): #a method in which we can print text on the screen with arial font and customizable position and size with the parameters
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def update(self): #refreshes to make sure our sprites are moving
        self.all_sprites.update()
    
    def draw(self): #this is the method that draws everything including player, walls, and all
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen) #draws our player
        #this order matters, first things are on the bottom because they are the 'first' to be drawn
        #the last lines in this method are drawn on top
        self.draw_text("Frames per second: " + str(floor(1/self.dt)), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Coins:" + str(self.player.coins), 24, WHITE, WIDTH/2, HEIGHT/4 + 20)
        pg.display.flip()



if __name__ == "__main__": # if 'main' is the name of file the underscores indicate something is special
    g = Game() #instantiation
     

while g.running:
    g.new()
    g.run() #makes sure the game actually runs when we want it to run and continues to keep running and refreshing as we keep the game running
