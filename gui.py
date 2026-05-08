import pygame
from gui_utils.button import Button
from gui_utils.status_window import Window
from units import Unit
from entity import Entity,Building
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class GUI:
    def __init__(self, engine, size, offset=(0,0)):
        self.engine = engine
        self.display_screen = self.engine.display_screen
        self.width = size[0]
        self.height = size[1]
        self.offset = offset

        self.screen = pygame.Surface((self.width,self.height)) 

        self.window = Window(width=self.width, height=int(self.height*0.35), offset=(0,int(self.height*0.65)))



        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.font_medium = pygame.font.Font('freesansbold.ttf', 24)
        self.font_small = pygame.font.Font('freesansbold.ttf', 12)

        self.row_height = 32
        self.max_selected_entities = 22
        self.texts = []
        self.render_packages = []
        self.selected_entities = []
        self.buttons = []

        self.engine.event_handler.subscribe("entity_selected",self.on_selected_entity)
        self.engine.event_handler.subscribe("unit_selected",self.on_selected_entity)
        self.engine.event_handler.subscribe("gui_pressed",self.on_gui_pressed)
        self.engine.event_handler.subscribe("reset_entity_selection",self.reset_selected)
        self.engine.event_handler.subscribe("entity_remove",self.on_entity_removed)
        self.engine.event_handler.subscribe("exit_window",self.on_exit_window)


        ####################TEMPS######################
        self.add_text("Selected entities:", (0,0))
        self.placement_text_idx = self.add_text(f"Placement Active:{self.engine.placement_active}", (0,28*32))
        self.add_button("Reset Selection", "reset_entity_selection", (40,self.height-64-32,128,64))
        self.add_button("Placement", "toggle_placement", (40,self.height-64-100,128,64),is_toggle=True)

        self.window.add_button(Button("X",(self.width-35 ,2,32,32),self.engine.event_handler,"exit_window"))

        debug_button = Button("Path", (4,self.window.height-68 ,128,64), self.engine.event_handler, "toggle_debug", True)
        self.window.add_button(debug_button)
        # self.add_button("test window", "test_pressed", (128,128,128,64),is_toggle=True)



    #########################################################
    # Event posted by entity to be removed, contains itself #
    #########################################################
    def on_entity_removed(self,data):
        event, *event_data = data
        entity = event_data

        if entity in self.selected_entities:
            self.selected_entities.remove(entity)

    def on_exit_window(self,data):
        if len(self.selected_entities) == 1:
            self.window.enabled=False
            self.selected_entities 

    def update(self):
        self.render_packages = []

        placement_text, placement_rect = self.get_text_renderable(f"Placement Active:{self.engine.placement_active}",(0,23*32))
        self.texts[self.placement_text_idx-1] = (placement_text, placement_rect)


        # if len(self.selected_entities) == 1:
        if self.window.enabled and len(self.selected_entities) == 1:
            self.draw_entity_submenu(self.selected_entities[0])

        for entity in self.selected_entities:
                self.show_selected_entity_info(entity)

        if len(self.selected_entities) == 0 or len(self.selected_entities) > 1:
            self.window.enabled = False


        # Wrap renderpackages in UI
        if len(self.render_packages) > self.max_selected_entities:
            diff = len(self.render_packages) - self.max_selected_entities
            for _ in range(diff):
                self.render_packages.pop(0)

    def get_text_renderable(self,text,coords):
        rendered_text = self.font.render(text, True, (255,255,255))
        textRect = rendered_text.get_rect()

        textRect.left = coords[0]
        textRect.top = coords[1]
        
        #Small padding
        if textRect.left == 0:
            textRect.left += 10

        return rendered_text, textRect

    def add_text(self,text,coords):
        rendered_text, textRect = self.get_text_renderable(text,coords)
        self.texts.append((rendered_text,textRect))

        return len(self.texts)

    def add_button(self, button_text, event_call, size, is_toggle=False):
        new_button = Button(button_text, size, self.engine.event_handler, event_call, is_toggle)
        self.buttons.append(new_button)

    def on_selected_entity(self,data):
        event_type, *event_data = data
        is_selected,entity = event_data

        if is_selected and entity not in self.selected_entities:
            self.selected_entities.append(entity)

        if not is_selected and entity in self.selected_entities:
            self.selected_entities.remove(entity)

        if len(self.selected_entities) == 1:
            self.window.enabled = True

    def on_gui_pressed(self,data):
        event_type, *event_data = data
        rx,ry= event_data

        gx,gy = rx-self.offset[0],ry
        # wx,wy = rx-self.window_offset[0], ry-self.window_offset[1]


        if not self.window.did_click(gx,gy):
            for button in self.buttons:
                if button.enabled:
                    if button.did_click(gx,gy):
                        button.click()

    def show_selected_entity_info(self,entity):
        package = []

        package.append(self.get_text_renderable(f"X: {int(entity.x)}",(64,1+len(self.render_packages))))
        package.append(self.get_text_renderable(f"Y: {int(entity.y)}",(155,1+len(self.render_packages))))

        texture_scaled = pygame.transform.scale(entity.tile.texture, (32,32))
        texture_coords = (0,1+len(self.render_packages))

        if texture_coords[0] == 0:
            texture_coords = (10,texture_coords[1])
        
        package.append((texture_scaled,texture_coords))
        self.render_packages.append(package)



    def draw_entity_submenu(self,entity):
        if type(entity) not in [Building, Unit]:
            self.show_window = False
            return

        package = []    
        line_height = 30
        first_row = 54
        num_attrs = 0
        #Entity/Unit texture
        texture_scaled = pygame.transform.scale(entity.tile.texture, (64,64))
        texture_coords = (32,64)
        package.append((texture_scaled, texture_coords))
        # self.window.blit(texture_scaled, texture_coords)

        #Info text
        package.append(self.get_text_renderable(f"{entity.name}",(128,first_row)))

        if hasattr(entity, "available_resources"):
            num_attrs += 1
            package.append(self.get_text_renderable(f"Res: {entity.available_resources}",(128, first_row + (num_attrs*line_height))))

        if hasattr(entity, "health"):
            num_attrs += 1
            package.append(self.get_text_renderable(f"HP: {entity.health}",(128, first_row + (num_attrs*line_height))))

        if hasattr(entity, "team"):
            num_attrs += 1
            package.append(self.get_text_renderable(f"Team: {entity.team}",(128,first_row + (num_attrs*line_height))))


        self.window.set_render_package(package)
        self.window.enabled = True

    def reset_selected(self,data):
        self.selected_entities = []

    def draw(self):

        self.screen.fill((0,0,0))

        for button in self.buttons:
            # button.draw(self.screen)
            button.draw(self.screen)

        for text,rect in self.texts:
            self.screen.blit(text,rect)

        for idx, package in enumerate(self.render_packages):
            for renderable,coord in package:
                coord = (coord[0],(idx+1)*self.row_height)
                self.screen.blit(renderable,coord)


        self.window.draw(self.screen)

        self.display_screen.blit(self.screen,self.offset)
