import pygame
from config import *

class Animator():
    def __init__(self, animation_key, tile, unit_texture_loader, animation_speed=1.0):
        self.animation_key = animation_key
        self.tile = tile
        self.texture_loader = unit_texture_loader
        self.animation_speed = animation_speed

        self.atlas = ANIMATION_ATLAS[animation_key]

        self.default_animation = "idle"
        self.current_animation = self.default_animation  # default

        self.timer = 0.0
        self.frame = 0

        self.stop_animation = False

    def set_animation(self, anim_name):
        if anim_name != self.current_animation:
            self.current_animation = anim_name
            self.timer = 0.0
            self.frame = 0
            self.stop_animation = False

    def update(self, dt):
        start, end = self.atlas[self.current_animation]
        frame_count = end - start + 1

        # advance timer
        self.timer += dt * self.animation_speed
        frame_duration = 0.1

        # compute current frame
        self.frame = int(self.timer / frame_duration) % frame_count
        texture_index = start + self.frame

        if self.current_animation == "die" and self.frame+1 == frame_count:
            texture_index = end
            self.stop_animation = True

        texture = self.texture_loader.get_texture((texture_index, 0))
        
        if "right" in self.current_animation:
            texture = pygame.transform.flip(texture,1,0)

        if not self.stop_animation:
            self.tile.texture = texture
