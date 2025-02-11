import os

import pygame as pg

utils_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(utils_dir, os.pardir))
data_dir = os.path.join(main_dir, "../assets")
img_dir = os.path.join(data_dir, "img")
font_dir = os.path.join(data_dir, "font")
dogica_path = os.path.join(font_dir, "Dogica_Pixel.ttf")
dogica_bold_path = os.path.join(font_dir, "Dogica_Pixel_Bold.ttf")

dark_green = (1, 50, 32)
NEXT_TURN_EVENT = pg.USEREVENT + 1


def draw_borders(surface, centerx, centery, width, height, thickness, color):
    x = centerx - width / 2
    y = centery - height / 2
    return pg.draw.rect(surface, color, (x, y, width, height), thickness)
