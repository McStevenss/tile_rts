from config import *

class Camera:
    def __init__(self, view_size=(16,16)):
        self.view_size = view_size
        self.offset = (0,0)

        if view_size[0] < MAP_SIZE[0] and view_size[1] < MAP_SIZE[1]:
            self.offset = (self.view_size[0]//4,self.view_size[1]//4)

    def on_arrows(self,data):
        event_type, *event_data = data
        direction_string, direction = event_data
        self._apply_direction(direction)
        
    def _apply_direction(self, direction):
        x_dir = self.offset[0] + direction[0]
        y_dir = self.offset[1] + direction[1]
        
        if x_dir >= 0 and x_dir+self.view_size[0] <= MAP_SIZE[0]:
            y_offset = self.offset[1]
            self.offset = (x_dir,y_offset)

        if y_dir >= 0 and y_dir+self.view_size[1] <= MAP_SIZE[1]:
            x_offset = self.offset[0]
            self.offset = (x_offset,y_dir)
            
        

