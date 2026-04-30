import pygame
from tile import Tile
from config import TILE_ATLAS

class GameMouse:
    def __init__(self, engine):
        self.x = 0
        self.y = 0
        self.engine = engine
        self.texture = self.engine.texture_loader.get_texture(TILE_ATLAS["default"])
        self.tile = Tile(self.engine, self.texture, (self.x,self.y))
        self.previous_pressed = None
        

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        b_pressed = pygame.mouse.get_pressed()

        self.tile.x = ((self.x) * self.engine.screen_ratio_x) // 8
        self.tile.y = ((self.y) * self.engine.screen_ratio_y) // 8

        self.tile.real_x = ((self.x) * self.engine.screen_ratio_x)
        self.tile.real_y = ((self.y) * self.engine.screen_ratio_y)

        camera_offset_x,camera_offset_y =self.engine.camera.offset

        # Initialize previous state if first frame
        if self.previous_pressed is None:
            self.previous_pressed = b_pressed

        # Check each button (left, middle, right)
        for i in range(3):
            # Pressed this frame but not last frame → PRESS event
            if b_pressed[i] and not self.previous_pressed[i]:
                self.engine.event_handler.post_event(
                    "m_pressed", (i, self.x,self.y, self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                )

            # Released this frame but was pressed last frame → RELEASE event
            if not b_pressed[i] and self.previous_pressed[i]:
                self.engine.event_handler.post_event(
                    "m_released", (i, self.x,self.y, self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                )

                if i == 0:
                    self.engine.event_handler.post_event(
                        "create_entity", ("human_village", "building", self.x,self.y, self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                    )
                if i == 2:
                    self.engine.event_handler.post_event(
                        "create_entity", ("orc_village", "building", self.x,self.y,  self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                    )


        self.previous_pressed = b_pressed

    def draw(self):
        self.tile.draw()