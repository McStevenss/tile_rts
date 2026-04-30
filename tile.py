import pygame
import random

class Tile:
    def __init__(self, engine, texture, pos=(0,0), background=False):

        self.engine = engine
        self.screen = self.engine.screen
        self.x = pos[0]
        self.y = pos[1]

        self.tile_size = 8
        self.texture = texture
        if self.texture is not None:
            self.rect:pygame.rect.Rect = self.texture.get_rect()
            self.rect.x = self.x * self.tile_size
            self.rect.y = self.y * self.tile_size

        self.is_background = background

        self.draw_debug = False
        self.active = False

        self.real_x = self.x*self.tile_size
        self.real_y = self.y*self.tile_size
    
    def draw(self):
        self.screen.blit(self.texture,(self.x*self.tile_size,self.y*self.tile_size)) 

    def draw_at(self, screen_x, screen_y):
        self.screen.blit(self.texture, (screen_x, screen_y))

           
    
                
                    