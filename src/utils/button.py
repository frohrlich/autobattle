import pygame as pg

from utils.utils import dogica_path
from utils.utils import draw_borders


class Button:
    def __init__(
        self,
        screen,
        centerx,
        centery,
        width,
        height,
        font_size,
        text,
        on_click_function=None,
        fill_colors=None,
    ):
        if fill_colors is None:
            fill_colors = {
                "normal": "#00aa00",
                "hover": "#006600",
                "pressed": "#003300",
            }
        self.screen = screen
        self.centerx = centerx
        self.centery = centery
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.text_str = text

        self.fill_colors = fill_colors

        self.surface = pg.Surface((self.width, self.height))
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (centerx, centery)
        self.font = pg.font.Font(dogica_path, font_size)
        self.text = self.font.render(text, True, (0, 0, 0))

    def process(self):
        mousePos = pg.mouse.get_pos()
        self.surface.fill(self.fill_colors["normal"])
        if self.rect.collidepoint(mousePos):
            self.surface.fill(self.fill_colors["hover"])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.surface.fill(self.fill_colors["pressed"])

        self.surface.blit(
            self.text,
            [
                self.rect.width / 2 - self.text.get_rect().width / 2,
                self.rect.height / 2 - self.text.get_rect().height / 2,
            ],
        )
        self.screen.blit(self.surface, self.rect)
        draw_borders(
            self.screen,
            self.centerx,
            self.centery,
            self.width,
            self.height,
            5,
            (150, 150, 150),
        )

    def click(self, pos):
        if self.on_click_function and self.rect.collidepoint(pos):
            self.on_click_function()

    def change_text(self, text):
        self.text_str = text
        self.text = self.font.render(text, True, (0, 0, 0))

    def change_font_size(self, font_size):
        self.font = pg.font.Font(dogica_path, font_size)
        self.text = self.font.render(self.text_str, True, (0, 0, 0))
