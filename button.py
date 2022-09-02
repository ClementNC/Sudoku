from re import I
import pygame

#button class
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.img = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        
        self.rect = self.img.get_rect()
        
        self.rect.topleft = (x,y)

        self.clicked = False

    def get_clicked(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))


class AddOn(Button):
    def __init__(self, x, y, image, scale):
        super().__init__(x,y,image,scale)
        self.width = self.img.get_width()
        self.is_on = False


    def get_clicked(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not (self.clicked):
                self.clicked = True
                action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))
        if self.is_on:
            pygame.draw.circle(surface, (0,0,255), self.rect.center,self.width/2, 2)
