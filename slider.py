import pygame




class Button:
   def __init__(self, pos, menu_screen, size, color):
       self.pos_correct = False
       self.font = pygame.font.Font('Grand9K.ttf', 52)
       self.rect = None
       self.clicked = False
       self.buttons = []
       self.color = color
       self.menu_open = False
       self.size = size
       self.pos = pos
       self.rect = pygame.Rect((pos[0] * menu_screen.get_width() / 1280, pos[1] * menu_screen.get_height() / 720),
                               size)


   def update(self, screen, new_colour):
       self.rect.center = (self.pos[0] * screen.get_width() / 1280, self.pos[1] * screen.get_height() / 720)
       self.rect.size = (self.size[0] * screen.get_width() / 1280, self.size[1] * screen.get_height() / 720)
       pygame.draw.rect(screen, self.color, self.rect)
       action = False
       if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
           self.clicked = True
           if self.rect.collidepoint(pygame.mouse.get_pos()):
               self.pos_correct = True


       if self.rect.collidepoint(pygame.mouse.get_pos()):
           pygame.draw.rect(screen, new_colour, self.rect)
           if self.pos_correct and pygame.mouse.get_pressed()[0] == 0 and self.clicked:
               action = True
               self.pos_correct = False
               self.clicked = False
       if pygame.mouse.get_pressed()[0] == 0:
           self.clicked = False




       return action




class slider(Button):
   def __init__(self, pos, menu_screen, size, color, pos2, size2, max_value, min_value, colour_2):
       super().__init__(pos, menu_screen, size, color)
       self.pos_correct_slider = False
       self.slider_box = pygame.Rect(
           (pos2[0], pos2[1]),
           size2)
       self.pos2 = pos2
       self.max = max_value
       self.size2 = size2
       self.min = min_value
       self.colour_2 = colour_2


   def slider_update(self, screen, colour_change):
       self.slider_box.center = (self.pos2[0] , self.pos2[1] )
       self.rect.center = (self.pos[0] , self.pos[1])
       self.slider_box.size = (self.size2[0],self.size2[1] )
       self.rect.size = (self.size[0], self.size[1] )
       pygame.draw.rect(screen, self.color, self.slider_box)
       pygame.draw.rect(screen,colour_change, (self.slider_box.topleft,(self.rect.centerx - self.slider_box.left - self.rect.width / 2,  self.slider_box.height) ))
       pygame.draw.rect(screen, self.colour_2, self.rect)
       if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
           self.clicked = True
           if self.rect.collidepoint(pygame.mouse.get_pos()):
               self.pos_correct = True
           elif self.slider_box.collidepoint(pygame.mouse.get_pos()):
               self.pos_correct_slider = True


       if self.clicked and self.pos_correct:
           self.pos[0] = pygame.mouse.get_pos()[0]
       if pygame.mouse.get_pressed()[0] == 0:
           if self.slider_box.collidepoint(pygame.mouse.get_pos()):
               if self.pos_correct_slider:
                   self.pos[0] = pygame.mouse.get_pos()[0]
                   self.pos_correct_slider = False
           self.pos_correct = False
           self.clicked = False
       if self.pos[0] > self.pos2[0] - self.size[0] / 2 + self.size2[0] / 2:
           self.pos[0] = self.pos2[0] - self.size[0] / 2 + self.size2[0] / 2
       if self.pos[0] < self.pos2[0] + self.size[0] / 2 - self.size2[0] / 2:
           self.pos[0] = self.pos2[0] + self.size[0] / 2 - self.size2[0] / 2
       return self.min + (self.max - self.min) / (self.slider_box.width - self.rect.width) * (
                   self.rect.centerx - self.slider_box.left - self.rect.width / 2)
