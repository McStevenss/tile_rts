from tile import Tile
from config import *
import pygame

class Animator():
    def __init__(self, animation_key, tile, unit_texture_loader, animation_speed=1.0):
        self.animation_key = animation_key
        self.tile = tile
        self.texture_loader = unit_texture_loader
        self.animation_speed = animation_speed

        self.atlas = UNIT_ATLAS[animation_key]

        self.current_animation = "idle"  # default
        self.timer = 0.0
        self.frame = 0

    def set_animation(self, anim_name):
        if anim_name != self.current_animation:
            self.current_animation = anim_name
            self.timer = 0.0
            self.frame = 0

    def update(self, dt):
        start, end = self.atlas[self.current_animation]
        frame_count = end - start + 1

        # advance timer
        self.timer += dt * self.animation_speed
        frame_duration = 0.1

        # compute current frame
        self.frame = int(self.timer / frame_duration) % frame_count
        texture_index = start + self.frame

        texture = self.texture_loader.get_texture((texture_index, 0))
        
        if self.current_animation == "right":
            texture = pygame.transform.flip(texture,1,0)


        self.tile.texture = texture

class Unit:
    def __init__(self, engine, texture_key="grunt", pos=(0,0)):
        self.engine = engine
        self.texture_loader = self.engine.unit_texture_loader
        self.screen = self.engine.screen
        self.x = pos[0]
        self.y = pos[1]
        self.texture_key = texture_key
        texture = self.texture_loader.get_texture((1,0))
        self.tile = Tile(self.engine,texture,(self.x,self.y))
        self.tile.tile_size = 8


        self.is_selected = False
        self.selected_texture = self.engine.texture_loader.get_texture(self.engine.tile_atlas["default"])
        self.selected_tile = Tile(self.engine,self.selected_texture,(self.x,self.y))
        self.animator = Animator(texture_key, self.tile, self.texture_loader, animation_speed=1.0)

        self.path = []
        self.movespeed = 2 #tiles per second
        self.movetimer = 0
        self.move_interval = 1/self.movespeed

    def update(self, dt):
        
        if self.tile.x != self.x:
            self.tile.x = self.x
            self.selected_tile.x = self.x
        if self.tile.y != self.y:
            self.tile.y = self.y
            self.selected_tile.y = self.y

        self.animator.update(dt)

        self.movetimer += dt

        if self.movetimer >= self.move_interval and self.path != []:
            path = self.path.pop(0)
            self.move(path[0],path[1])
            self.movetimer = 0

        if self.path == []:
            self.animator.set_animation("idle")

    def move(self,x,y):

        if self.x < x:
            self.animator.set_animation("right")
        elif self.x > x:
            self.animator.set_animation("left")
        elif self.y > y:
            self.animator.set_animation("up")
        elif self.y < y:
            self.animator.set_animation("down")



        self.x = x
        self.y = y

    def tick(self,dt):
        pass


    def draw(self):
        self.tile.draw()

        if self.is_selected:
            self.selected_tile.draw()


    def draw_at(self, screen_x, screen_y):
        #grunt tiles are 9x10
        tile_offset_y = 2
        tile_offset_x = 1
        self.tile.draw_at(screen_x-tile_offset_x, screen_y-tile_offset_y)

        if self.is_selected:
            self.selected_tile.draw_at(screen_x, screen_y)
