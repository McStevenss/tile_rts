from entity import *
from config import *
import random 
from camera import Camera

class EntityHandler:
    def __init__(self, engine):
        self.engine = engine
        self.entities = {} #(x,y) : entity

        self.map_width,self.map_height = MAP_SIZE
        #Generate mines on map
        self.generate_map_resources()

        self.engine.event_handler.subscribe("entity_remove",self.on_remove_entity)


    def on_remove_entity(self,data):
        event_type, *event_data = data
        ex,ey = event_data
        self.remove_entity(ex,ey)

    def generate_map_resources(self):

        for y in range(self.map_height):
            if y == 0 or y == self.map_height-1:
                continue

            for x in range(self.map_width):
                if x == 0 or x == self.map_width-1:
                    continue

                if random.random() < 0.05:

                    if random.random() <= 0.5:
                        self.add_entity(Mine(self.engine,pos=(x,y)))
                    else:
                        self.add_entity(Tree(self.engine,pos=(x,y)))



    def add_entity(self,entity: Entity):

        entity_pos = (int(entity.x),int(entity.y))

        if entity_pos in self.entities.keys():
            self.engine.event_handler.post_event("Error",[f"[EntityHandler:add_entity] Entity already exists on {int(entity.x)},{int(entity.y)}"])
            return
        
        if entity_pos[0] > 0 and entity_pos[0] < self.map_width-1:   
            if entity_pos[1] > 0 and entity_pos[1] < self.map_height-1:
                self.entities[(int(entity.x),int(entity.y))] = entity
            return
        
        self.engine.event_handler.post_event("Error",[f"[EntityHandler:add_entity] Entity would be outside the map at {int(entity.x)},{int(entity.y)}"])

    

    def remove_entity(self, x,y):
        if (x,y) in self.entities.keys():
            del self.entities[x,y]

    def get_entity(self,x,y):
        if (x,y) in self.entities.keys():
            return self.entities[(x,y)]
        
        return None

    def update_entities(self, dt):
        for entity in self.entities.values():
            entity.update(dt)


    def draw_entities(self, camera: Camera = None):

        view_w, view_h = camera.view_size
        off_x, off_y = camera.offset

        for (x, y), entity in self.entities.items():

            # Cull entities outside camera
            if not (off_x <= x < off_x + view_w and off_y <= y < off_y + view_h):
                continue

            screen_x = (x - off_x) * entity.tile.tile_size
            screen_y = (y - off_y) * entity.tile.tile_size

            entity.draw_at(screen_x, screen_y)