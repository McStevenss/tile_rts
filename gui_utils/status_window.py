import pygame



class Window:
    def __init__(self, width, height, offset):
        self.width = width
        self.height = height
        self.offset = offset

        self.screen = pygame.Surface((self.width,self.height))
        self.enabled = True
        
        self.buttons = []
        self.package = []

    def did_click(self,x,y):
        
        if x >= self.offset[0] and y >= self.offset[1] and self.enabled:
        
            for button in self.buttons:
                wx = x-self.offset[0]
                wy = y-self.offset[1]
                if button.did_click(wx,wy):
                    button.click()
            return True
        
        return False


    def add_button(self, Button):
        self.buttons.append(Button)


    def set_render_package(self, package):
        self.package = package

    def reset_render_package(self):
        self.package = []

    def draw(self, parent_surface):
        if self.enabled:
            self.screen.fill((0,0,0))
            pygame.draw.rect(self.screen, (255,255,255), (0,0,self.screen.get_width(),self.screen.get_height()), 2)

            if len(self.package) > 0:
                for renderable, coords in self.package:
                    self.screen.blit(renderable,coords)

            for button in self.buttons:
                button.draw(self.screen)

            parent_surface.blit(self.screen, self.offset)
