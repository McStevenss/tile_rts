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
        self.drag_start = (0,0)
        self.min_drag_distance = 1

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
        # print(b_pressed)

        for i in range(3):
            # Pressed this frame but not last frame → PRESS event
            if b_pressed[i] and not self.previous_pressed[i]:
                self.engine.event_handler.post_event(
                    "m_pressed", (i, self.x,self.y, self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                )
                if i == 0:
                    self.drag_start = (self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)

            # Released this frame but was pressed last frame → RELEASE event
            if not b_pressed[i] and self.previous_pressed[i]:
                self.engine.event_handler.post_event(
                    "m_released", (i, self.x,self.y, self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                )

                if i == 0:
                    if self.engine.placement_active:
                        self.engine.event_handler.post_event(
                            "create_entity", ("human_village", "building", self.x,self.y, self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                        )

                    if abs(self.drag_start[0] - (self.tile.x + camera_offset_x)) > self.min_drag_distance:
                        print("mouse drag", abs(self.drag_start[0] - (self.tile.x+ camera_offset_x)))
                        if self.drag_start[0] > self.tile.x + camera_offset_x:
                            start_x = self.tile.x + camera_offset_x
                            end_x = self.drag_start[0]
                        else:
                            start_x = self.drag_start[0]
                            end_x = self.tile.x + camera_offset_x

                        if self.drag_start[1] > self.tile.y + camera_offset_y:
                            start_y = self.tile.y + camera_offset_y
                            end_y = self.drag_start[1]
                        else:
                            start_y = self.drag_start[1]
                            end_y = self.tile.y + camera_offset_y

                        self.engine.event_handler.post_event(
                            "m_drag", (start_x,start_y,end_x,end_y)
                        )


                if i == 2 and self.engine.placement_active:
                    self.engine.event_handler.post_event(
                        "create_entity", ("orc_village", "building", self.x,self.y,  self.tile.x + camera_offset_x, self.tile.y + camera_offset_y)
                    )


        if b_pressed != self.previous_pressed:
            self.previous_pressed = b_pressed

    def draw(self):
        self.tile.draw()