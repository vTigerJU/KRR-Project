import pygame
import config as c

class Button:
    def __init__(self, text, x, y, w, h, callback, screen):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.hover = False
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)


    def draw(self):
        color = c.BUTTON_HOVER if self.hover else c.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.rect, border_radius=6)

        label = self.font.render(self.text, True, c.TEXT_COLOR)
        label_rect = label.get_rect(center=self.rect.center)
        self.screen.blit(label, label_rect)

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.callback()