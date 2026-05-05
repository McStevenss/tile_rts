import pygame



class Button:
    def __init__(self, text, size, event_handler, on_pressed_event="button_clicked"):
        self.x = size[0]
        self.y = size[1]
        self.w = size[2]
        self.h = size[3]
        self.text = text
        self.on_pressed_event = on_pressed_event
        self.rect = pygame.rect.Rect(self.x,self.y,self.w,self.h)
        self.event_handler = event_handler

        self.font_small = pygame.font.Font('freesansbold.ttf', 14)
        self.rendered_text = self.font_small.render(text, True, (255,255,255))
        self.textRect = self.rendered_text.get_rect()

        self.textRect.left = self.x + self.w//2 - self.textRect.width//2
        self.textRect.top = self.y + self.h//2 - 12


    def did_click(self,x,y):
        return self.rect.collidepoint(x,y)
    
    def click(self):
        self.event_handler.post_event(self.on_pressed_event, ("clicked", self.x+(self.w//2),self.y+(self.h//2)))



    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,128),self.rect)
        screen.blit(self.rendered_text,self.textRect)



