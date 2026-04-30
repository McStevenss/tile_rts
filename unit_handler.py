from units import *
from config import *
import random 
from camera import Camera
from texture_loader import TextureLoader


class UnitHandler:
    def __init__(self, engine):
        self.engine = engine
        self.units = [] #(x, y ,unit)
        self.unit_texture_loader = TextureLoader(engine=self,spritesheet_path="textures/units/Soldier.png",spritesheet_tilesize=10)


    def add_unit(self,unit: Unit):
        ux,uy = (int(unit.x),int(unit.y))

        for x,y,unit in self.units:
            if ux == x and uy == y:
                self.engine.event_handler.post_event("Error",[f"[UnitHandler:add_unit] Unit already exists on {int(unit.x)},{int(unit.y)}"])
                return

        self.units.append((ux,uy,unit))        
        

    def remove_unit(self, x,y):
        idx_to_remove = None
        for idx, (ux,uy,unit) in self.units:
            if ux == x and uy == y:
                idx_to_remove = idx

        if idx_to_remove is not None:
            del self.units[idx_to_remove]
    
    def get_unit(self,x,y):
        for ux,uy,unit in self.units:
            if ux == x and uy == y:
                return unit
            
        return None
    

    def update_units(self, dt):
        to_update = []#(idx,x,y)
        for idx, (x,y,unit) in enumerate(self.units):
            unit.update(dt)
            to_update.append((idx,unit.x,unit.y,unit))

        if to_update != []:
            for idx,x,y,unit in to_update:
                self.units[idx] = (x,y,unit)



    def draw_units(self, camera: Camera = None):

        view_w, view_h = camera.view_size
        off_x, off_y = camera.offset

        # for unit in self.units.values():
        for ux,uy, unit in self.units:
            # Cull using actual unit position
            if not (off_x <= ux < off_x + view_w and off_y <= uy < off_y + view_h):
                continue

            screen_x = (ux - off_x) * unit.tile.tile_size
            screen_y = (uy - off_y) * unit.tile.tile_size

            unit.draw_at(screen_x, screen_y)