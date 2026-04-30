import pygame
import os 
import glob
import random

class TextureLoader:
    def __init__(self, engine, spritesheet_path,spritesheet_tilesize = 16):
        self.engine = engine
        self.texture_atlas = {}
        self.spritesheet_path = spritesheet_path
        self.tile_size = spritesheet_tilesize

        self.texture_atlas = self.__load_textures(self.spritesheet_path)

        print("Loaded tiles!")


    def __load_textures(self, path):
        texture_atlas = {}

        spritesheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = spritesheet.get_size()
        tile_size = self.tile_size

        for y in range(0, sheet_height, tile_size):
            for x in range(0, sheet_width, tile_size):
                tile = spritesheet.subsurface(pygame.Rect(x, y, tile_size, tile_size))
                name = ((x // tile_size), (y // tile_size))  # Generating key based on tile position
    
                texture_atlas[name] = tile
        
        return texture_atlas
    
    def load_image(self, path):
        texture = pygame.image.load(path).convert_alpha()
        return texture

    def get_texture(self, key):
        if key is None:
            return None
        
        if type(key) == list:
            key = random.choice(key)

        if key in self.texture_atlas.keys():
            return self.texture_atlas[key]

        print(f"Texture at position '{key}' not found in atlas")
        return None  
