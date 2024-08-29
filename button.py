import pygame


class Button:
    def __init__(self, x, y, width, height, text, color=(208, 25, 32), hover_color=(135, 17, 20), font_size=30):
        self.rect = pygame.Rect(x, y, width+20, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font('Grand9K.ttf', font_size)
        self.text = text
        self.text_surface = self.font.render(text, True, (255,255,255), (0,0,0))
        self.text_surface.set_colorkey((0,0,0))
        self.text_rect = pygame.Rect(0,0, width, height)
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, (255,255,255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
