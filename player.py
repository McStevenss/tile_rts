import pygame
from texture_loader import TextureLoader
import math

class Player:
    def __init__(self, engine, texture_key, pos=(0,0), speed = 2):
        self.engine = engine
        self.screen = self.engine.screen

        self.texture_loader:TextureLoader = self.engine.texture_loader
        self.texture_key = texture_key

        self.x = pos[0]
        self.y = pos[1]
        self.dir = (0,0)
        self.tile_size = 16
        self.offset = (0,0)
        self.centered_pos = (0,0)
        self.speed = speed
        self.__load_texture()

        self.rect = self.texture.get_rect()


        self.draw_debug = False
       
    
    def set_map(self,map):
        self.map = map
        self.offset_x = (self.map.map_width  *self.texture_loader.tile_size) 
        self.offset_y = (self.map.map_height *self.texture_loader.tile_size)

    def __load_texture(self):
        self.texture = self.texture_loader.get_texture(self.texture_key)

    def update_collision_rect(self):
        self.rect.x = self.x+self.offset[0]
        self.rect.y = self.y+self.offset[1]
        self.rect.width = self.texture.get_width()
        self.rect.height = self.texture.get_height()

    def valid_move(self,pos) -> bool:
        
        test_pos = (self.rect.x + pos[0], self.rect.y + pos[1])

        test_rect:pygame.rect.Rect = pygame.rect.Rect(test_pos,(self.texture.get_width(),self.texture.get_height()))

        for row in self.engine.map.map:
            for tile in row:
                if tile.is_background == False:
                    if pygame.Rect.colliderect(test_rect, tile.rect):                 
                        tile.active = True
                        return False
                    else:
                        tile.active = False
        return True
    
    def valid_move_poscorrection(self,pos) -> tuple:
        
        test_pos = (self.rect.x + math.ceil(pos[0]), self.rect.y + math.ceil(pos[1]))
        
        test_rect_x:pygame.rect.Rect = pygame.rect.Rect((test_pos[0],self.rect.y),(self.texture.get_width(),self.texture.get_height()))
        test_rect_y:pygame.rect.Rect = pygame.rect.Rect((self.rect.x,test_pos[1]),(self.texture.get_width(),self.texture.get_height()))

        valid_x = True
        valid_y = True
        for row in self.engine.map.map:
            for tile in row:
                if tile.is_background == False:
                    if pygame.Rect.colliderect(test_rect_x, tile.rect):
                        tile.active = True                 
                        valid_x = False

                    if pygame.Rect.colliderect(test_rect_y, tile.rect):
                        tile.active = True
                        valid_y = False                 

        return valid_x, valid_y
        

    def update_centered_pos(self):
        self.engine.map.set_offset((self.x, self.y))
        self.centered_pos =  (int((self.offset_x)- (self.tile_size//2)), 
                              int((self.offset_y)- (self.tile_size//2)))

    def update(self): 
        self.update_centered_pos()
        self.weapon.update()

       

    def draw(self, offset):
        if self.engine.zoom_factor != self.zoom_factor:
            self.zoom_factor = self.engine.zoom_factor
            self.__load_texture()

        

        ox,oy = offset
        self.offset = offset
        self.screen.blit(self.texture,(self.x+ox,self.y+oy)) 
        self.weapon.draw()
        
        self.update_collision_rect()

        if self.engine.draw_debug:
            pygame.draw.rect(self.screen,(255,0,0),rect=self.rect)
            pygame.draw.line(self.screen, (255,0,0), (0,self.screen.get_height()//2), (self.screen.get_width(),self.screen.get_height()//2))
            pygame.draw.line(self.screen, (255,0,0), (self.screen.get_width()//2,0), (self.screen.get_width()//2,self.screen.get_height()))
