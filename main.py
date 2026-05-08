import pygame
from config import *
from texture_loader import TextureLoader
from map import Map
from player import Player
from entity import Building
from mouse import GameMouse
from events import EventHandler
from entity_handler import EntityHandler
from units import Unit
from unit_handler import UnitHandler
from camera import Camera
from gui import GUI

#POST EVENT EXAMPLE
#event_handler.post_event("create_entity", ("orc_village", "building", self.x,self.y,  self.tile.x + camera_offset_x, self.tile.y + camera_offset_y))



class Engine:
    def __init__(self):
        self.setup_screens("RTS Game")
        pygame.init()

        self.tick_rate = 100
        self.dt = 0 
        self.clock = pygame.time.Clock()
  
        self.done = False 
        self.placement_active = False
        self.debug = False
        self.event_handler = EventHandler()
        self.tile_atlas = TILE_ATLAS

        self.texture_loader = TextureLoader(engine=self,spritesheet_path="textures/tilesheet.png",spritesheet_tilesize=8)
        self.map = Map(self,texture_loader=self.texture_loader, width=MAP_SIZE[0],height=MAP_SIZE[1])
        self.camera = Camera(view_size=(42,32))

        self.gui = GUI(self,self.gui_size,self.gui_offset)
        self.event_handler.subscribe("arrows_pressed",self.camera.on_arrows)
        self.event_handler.subscribe("m_released",self.on_mouse_pressed)
        self.event_handler.subscribe("toggle_debug",self.on_debug)
        self.event_handler.subscribe("toggle_placement",self.on_placement)

        self.entity_handler = EntityHandler(self)
        self.unit_handler = UnitHandler(self)

        self.test_unit = Unit(self,"grunt",(2,2))
        self.unit_handler.add_unit(self.test_unit)

        self.camera_pan_speed = 16
        self.pan_interval = 1.0 / self.camera_pan_speed  # 0.5s
        self.pan_timer = 0.0


        self.draw_debug = False
        pygame.mouse.set_visible(1)
        self.mouse = GameMouse(self)


    def setup_screens(self, windowTitle="Tile_base"):
        self.screen_width = 1920
        self.screen_height = 1080

        self.target_size = (1440, 1080)

        # self.game_screen_width = 256
        self.game_screen_width = 336#256
        self.game_screen_height = 256

        #Setup main display and game display
        self.size = (self.screen_width, self.screen_height)
        self.display_screen = pygame.display.set_mode(self.size) 
        self.screen = pygame.Surface((self.game_screen_width,self.game_screen_height)) 

        #Calculate game vs screen ratio

        self.display_ratio = (self.screen_width/self.game_screen_width, self.screen_height/self.game_screen_height)

        self.gui_size = (self.screen_width-self.target_size[0], self.screen_height)
        self.gui_offset = (self.target_size[0],0)

        pygame.display.set_caption(windowTitle)

    def on_debug(self,data):
        self.debug = not self.debug
        print("[DEBUG MODE]:",self.debug)

    def on_placement(self,data):
        self.placement_active = not self.placement_active

    def on_mouse_pressed(self,data):
        event_type, *event_data = data
        mb, rx,ry,tx,ty = event_data

        if mb==0 and rx <= self.target_size[0] and ry <= self.target_size[1]:
            entity = self.entity_handler.get_entity(int(tx),int(ty))
            if entity is not None:
                self.event_handler.post_event("reset_entity_selection", ("Single Entity pressed",1))
                entity.tick(self.dt)

                entity.is_selected = not entity.is_selected
                self.event_handler.post_event("entity_selected", (entity.is_selected,entity))
                return
            
            unit = self.unit_handler.get_unit(int(tx),int(ty))
            if unit is not None:
                self.event_handler.post_event("reset_entity_selection", ("Nothing pressed",1))
                unit.is_selected = not unit.is_selected
                self.event_handler.post_event("unit_selected", (unit.is_selected,unit))
                
                return
            

            self.event_handler.post_event("reset_entity_selection", ("Nothing pressed",1))
            

        if mb==2 and rx <= self.target_size[0] and ry <= self.target_size[1]:
            if self.map.is_valid_position(int(tx),int(ty)):
                for unit in self.unit_handler.selected_units:                    
                    path =self.map.find_path(int(unit.x),int(unit.y) ,int(tx),int(ty), self.entity_handler.entities)
                    unit.path = path


        if rx >= self.gui_offset[0]:
            # self.event_handler.post_event("gui_pressed",data)
            self.event_handler.post_event("gui_pressed",(rx,ry))

    def handle_events(self):
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_v and keys[pygame.K_v]:
                   self.draw_debug = not self.draw_debug

        self.handle_input(keys)
        self.kpressed = keys
        
    def handle_input(self, keys):
        
        if keys[pygame.K_ESCAPE]:
            self.done = True

        if keys[pygame.K_DOWN] and self.pan_timer >= self.pan_interval:
            self.event_handler.post_event("arrows_pressed", ("down",(0,1)))

        if keys[pygame.K_UP] and self.pan_timer >= self.pan_interval:
            self.event_handler.post_event("arrows_pressed", ("up",(0,-1)))

        if keys[pygame.K_RIGHT] and self.pan_timer >= self.pan_interval:
            self.event_handler.post_event("arrows_pressed", ("right",(1,0)))

        if keys[pygame.K_LEFT] and self.pan_timer >= self.pan_interval:
            self.event_handler.post_event("arrows_pressed", ("left",(-1,0)))
                
      
     
    def run(self):
        while not self.done:
            # self.screen.fill((0,0,0))
            self.screen.fill((0,255,0))

            self.pan_timer += self.dt

            # --- Main event loop
            self.handle_events()
            #Update objects
            self.map.update()
            self.mouse.update()
            self.entity_handler.update_entities(self.dt)
            self.unit_handler.update_units(self.dt)
            self.gui.update()
            #Draw objects

            self.map.draw(self.camera)
            self.unit_handler.draw_units(self.camera)
            self.entity_handler.draw_entities(self.camera)
            self.mouse.draw()
            scaled = pygame.transform.scale(self.screen, self.target_size)
            self.display_screen.blit(scaled,(0,0))
            self.gui.draw()


            pygame.display.flip()
            tick = self.clock.tick(self.tick_rate)
            self.dt = tick/1000

            if self.pan_timer >= self.pan_interval:
                self.pan_timer = 0

            
            pygame.display.set_caption(f"RTS TEST - FPS:{round(self.clock.get_fps(),2)}")
        # Close the window and quit.
        print("Goodbye!")
        pygame.quit()


if __name__ == "__main__":
    game = Engine()
    game.run()