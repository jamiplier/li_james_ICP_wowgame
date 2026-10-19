import pygame as pg
#full of settings for us to import
FPS = 60
WIDTH = 1024
HEIGHT = 768
TITLE = "Best Game Ever"
TILESIZE = 32
#colors
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
BGCOLOR = (255,100,100)
RED = (255,0,0)
YELLOW = (255,255,0)
#player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE, TILESIZE)

#mobsettings
MOB_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)