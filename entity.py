from tile import Tile
import pygame
from enum import Enum

class ResourceType(Enum):
    WOOD = 1
    IRON = 2
    FOOD = 3

class Entity:
    def __init__(self, engine, texture_key="default", pos=(0,0)):
        self.engine = engine
        self.screen = self.engine.screen
        self.x = pos[0]
        self.y = pos[1]
        self.texture_key = texture_key
        texture = self.engine.texture_loader.get_texture(self.engine.tile_atlas[self.texture_key])
        self.tile = Tile(self.engine,texture,(self.x,self.y))
        self.is_selected = False
        self.selected_texture = self.engine.texture_loader.get_texture(self.engine.tile_atlas["default"])
        self.selected_tile = Tile(self.engine,self.selected_texture,(self.x,self.y))

        self.engine.event_handler.subscribe("reset_entity_selection",self.__reset_selection)


    def __reset_selection(self,data):
        self.is_selected = False

    def update(self, dt):
        
        if self.tile.x != self.x:
            self.tile.x = self.x
            self.selected_tile.x = self.x
        if self.tile.y != self.y:
            self.tile.y = self.y
            self.selected_tile.y = self.y

    def tick(self,dt):
        pass


    def draw(self):
        self.tile.draw()

        if self.is_selected:
            self.selected_tile.draw()

    def draw_at(self, tile_x, tile_y):
        self.tile.draw_at(tile_x, tile_y)

        if self.is_selected:
            self.selected_tile.draw_at(tile_x, tile_y)



class Building(Entity):
    def __init__(self, engine, texture_key="human_village", pos=(0, 0)):
        super().__init__(engine, texture_key, pos)
           
        self.status_rect = pygame.Rect(self.tile.real_x, self.tile.real_y-4, self.tile.tile_size,2)
        self.progress_rect = pygame.Rect(self.tile.real_x, self.tile.real_y-4, 1,2)
        
        self.name = str.capitalize(texture_key.replace("_"," "))

        self.progress = 0
        self.resources_gathered = 0
        self.team = -1
    
    def update(self, dt):
        super().update(dt)

        self.tick(dt)
      

    def tick(self,dt):
        self.progress += 1.5*dt
        if self.progress >= self.tile.tile_size:
            self.progress = 0
            self.resources_gathered +=1
            self.engine.event_handler.post_event("entity_gained_resource", (self.texture_key, 1))

        self.progress_rect.width = self.progress

    def draw_at(self, tile_x, tile_y):
        super().draw_at(tile_x, tile_y)

        self.status_rect.x = tile_x
        self.status_rect.y = tile_y - 4
        self.progress_rect.x = tile_x
        self.progress_rect.y = tile_y- 4
        pygame.draw.rect(self.engine.screen,(255,0,0),self.status_rect) 
        pygame.draw.rect(self.engine.screen,(0,255,0),self.progress_rect)


class Mine(Entity):
    def __init__(self, engine, texture_key="mine", pos=(0, 0)):
        super().__init__(engine, texture_key, pos)
        self.available_resources = 10
        self.type = ResourceType.IRON

        self.status_rect = pygame.Rect(self.tile.real_x, self.tile.real_y-4, self.tile.tile_size, 2)
        self.progress_rect = pygame.Rect(self.tile.real_x, self.tile.real_y-4, self.tile.tile_size, 2)
        self.tick_width = self.tile.tile_size / self.available_resources

    
    def update(self, dt):
        super().update(dt)

    def tick(self,dt):
        self.available_resources -= 1

        if self.progress_rect.width > 0:
            self.progress_rect.width -= self.tick_width

        if self.available_resources <= 0:
            self.engine.event_handler.post_event("entity_remove",[self.x,self.y])


        return self.type

    def draw_at(self, tile_x, tile_y):
        super().draw_at(tile_x, tile_y)


        if self.progress_rect.width != self.tile.tile_size:
            self.status_rect.x = tile_x
            self.status_rect.y = tile_y - 4
            self.progress_rect.x = tile_x
            self.progress_rect.y = tile_y- 4
            pygame.draw.rect(self.engine.screen,(255,0,0),self.status_rect) 
            pygame.draw.rect(self.engine.screen,(0,255,0),self.progress_rect)



class Tree(Entity):
    def __init__(self, engine, texture_key="tree_base", pos=(0, 0)):
        super().__init__(engine, texture_key, pos)
        self.available_resources = 10
        self.type = ResourceType.WOOD
        
        self.mid_texture = self.engine.texture_loader.get_texture(self.engine.tile_atlas["tree_mid"])
        self.top_texture = self.engine.texture_loader.get_texture(self.engine.tile_atlas["tree_top"])

        self.middle_tile = Tile(self.engine,self.mid_texture,(self.x,self.y-1))
        self.top_tile = Tile(self.engine,self.top_texture,(self.x,self.y-2))
    
    def update(self, dt):
        super().update(dt)

    def tick(self,dt):
        self.available_resources -= 1

        if self.available_resources <= 0:
            self.engine.event_handler.post_event("entity_remove",[self.x,self.y])
        return self.type


    def draw_at(self, tile_x, tile_y):
        super().draw_at(tile_x, tile_y)

        self.top_tile.draw_at(tile_x,tile_y - (self.tile.tile_size* 2))
        self.middle_tile.draw_at(tile_x,tile_y - (self.tile.tile_size* 1))
        


