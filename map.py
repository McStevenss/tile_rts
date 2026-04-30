import pygame

import random
import cv2 
from tile import Tile
from texture_loader import TextureLoader
from player import Player
from config import *
from camera import Camera
from pathfind import astar


class Map:
    def __init__(self, engine,texture_loader:TextureLoader, width, height):
        self.engine = engine
        self.screen = self.engine.screen
        self.texture_loader = texture_loader

        self.map_height,self.map_width = self.engine.game_screen_height // 8,self.engine.game_screen_width // 8
        self.map_height,self.map_width = height, width
        self.map_data = self.generate_map(self.map_width, self.map_height)
        self.offset = (0,0)
        self.populate_maps()
        self.engine.event_handler.post_event("map_ready",[1])

    def load_map(self):
        map = cv2.imread(self.map_path)
        map = cv2.cvtColor(map, cv2.COLOR_BGR2RGB)

        H,W,_ = map.shape
        return map, H,W
    
    def generate_map(self, width, height):
        
        map = []
        for y in range(height):
            map.append([])

            #If its the top row or bottom row, add all walls
            if y == 0 or y == height-1:
                [map[y].append((0,0,0)) for i in range(width)]
                continue

            for x in range(width):
                if x == 0 or x == width-1:
                    map[y].append((0,0,0))
                else:
                    map[y].append((1,1,1))


        print(len(map))
        return map                

    def is_valid_position(self,target_x,target_y):

        if target_x < 0 or target_x > self.map_width-1:
            return False
        
        if target_y < 0 or target_y > self.map_height-1:
            return False

        if target_y == 0 or target_y == self.map_height-1:
            return False
        if target_x == 0 or target_x == self.map_width-1:
            return False
        
        return True
    
    def find_path(self,start_x,start_y, target_x,target_y, additional = None):
        return astar(self, (start_x,start_y), (target_x,target_y), additional)

    def convert_color(self, np_color):
        r,g,b = np_color
        color = (r,g,b)

        return color
    
    def get_tile_from_color(self,color,pos):
        if color in TILE_ATLAS.keys():
            return Tile(self.engine, self.texture_loader.get_texture(TILE_ATLAS[color]),pos)
        else: return Tile(self.engine, self.texture_loader.get_texture(TILE_ATLAS["default"]),pos)
    

    def populate_maps(self):
        game_map = []
        for y in range(0,self.map_height):
            row = []
            for x in range(0,self.map_width):
                color = self.convert_color(self.map_data[y][x])
                tile = self.get_tile_from_color(color, (x,y))    
                row.append(tile)

            game_map.append(row)

        self.map = game_map


    def update(self):
        pass


    def draw(self, camera: Camera):

        view_w, view_h = camera.view_size
        off_x, off_y = camera.offset

        for y in range(off_y, off_y + view_h):
            if y >= len(self.map):
                break

            for x in range(off_x, off_x + view_w):
                if x >= len(self.map[y]):
                    break

                tile = self.map[y][x]

                # Convert world → screen coordinates
                screen_x = (x - off_x) * tile.tile_size
                screen_y = (y - off_y) * tile.tile_size

                tile.draw_at(screen_x, screen_y)


