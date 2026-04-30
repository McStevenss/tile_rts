from units import *
from config import *
import random 
from camera import Camera

class UnitHandler:
    def __init__(self, engine):
        self.engine = engine

        self.units = {} #(x,y) : unit


    def add_unit(self,unit: Unit):
        unit_pos = (int(unit.x),int(unit.y))

        if unit_pos in self.units.keys():
            self.engine.event_handler.post_event("Error",[f"[UnitHandler:add_unit] Unit already exists on {int(unit.x)},{int(unit.y)}"])
            return
        
        self.units[(int(unit.x),int(unit.y))] = unit

    def remove_unit(self, x,y):
        if (x,y) in self.units.keys():
            del self.units[x,y]

    def get_unit(self,x,y):
        if (x,y) in self.units.keys():
            return self.units[(x,y)]
        
        return None
    
    def update_units(self, dt):
        for unit in self.units.values():
            unit.update(dt)


    def draw_units(self, camera: Camera = None):

        view_w, view_h = camera.view_size
        off_x, off_y = camera.offset

        for (x, y), unit in self.units.items():

            # Cull entities outside camera
            if not (off_x <= x < off_x + view_w and off_y <= y < off_y + view_h):
                continue

            screen_x = (x - off_x) * unit.tile.tile_size
            screen_y = (y - off_y) * unit.tile.tile_size

            unit.draw_at(screen_x, screen_y)