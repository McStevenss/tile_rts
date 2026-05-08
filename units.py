from tile import Tile
from animator import Animator

class Unit:
    def __init__(self, engine, texture_key="grunt", pos=(0,0)):
        self.engine = engine
        self.texture_loader = self.engine.unit_handler.unit_texture_loader
        self.screen = self.engine.screen
        self.name = str.capitalize(texture_key)
        
        #Unit defaults
        self.x = pos[0]
        self.y = pos[1]
        self.health = 15
        self.team = -1

        #Texture and Tiles
        self.texture_key = texture_key
        texture = self.texture_loader.get_texture((1,0))
        self.tile = Tile(self.engine,texture,(self.x,self.y))
        self.tile.tile_size = 8

        self.is_selected = False
        self.selected_texture = self.engine.texture_loader.get_texture(self.engine.tile_atlas["default"])
        self.selected_tile = Tile(self.engine,self.selected_texture,(self.x,self.y))
        self.animator = Animator(texture_key, self.tile, self.texture_loader, animation_speed=1.0)


        #Pathing and speed
        self.path = []
        self.movespeed = 2 #tiles per second
        self.movetimer = 0
        self.move_interval = 1/self.movespeed

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

        self.animator.update(dt)

        self.movetimer += dt

        if self.movetimer >= self.move_interval and self.path != []:
            path = self.path.pop(0)
            self.move(path[0],path[1])
            self.movetimer = 0

        if self.path == []:
            self.animator.set_animation(self.animator.default_animation)

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


    def draw_at(self, screen_x, screen_y, off_x=None,off_y=None):
        #grunt tiles are 9x10
        tile_offset_y = 2
        tile_offset_x = 1
        self.tile.draw_at(screen_x-tile_offset_x, screen_y-tile_offset_y)

        if self.is_selected:
            self.selected_tile.draw_at(screen_x, screen_y)

        if self.engine.debug and off_x is not None and off_y is not None:
            for px,py in self.path:
                path_screen_x = (px - off_x) * self.tile.tile_size
                path_screen_y = (py - off_y) * self.tile.tile_size
                self.selected_tile.draw_at(path_screen_x, path_screen_y)
