import os
import sys

import pygame as pg

from utils.spritesheet import Spritesheet

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "../assets")
img_dir = os.path.join(data_dir, "img")


def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    spritesheet = Spritesheet(os.path.join(img_dir, "spritesheet.png"))

    pg.display.set_caption("Autobattle")

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((1, 50, 32))

    screen.blit(background, (0, 0))
    pg.display.flip()

    player_pos = pg.Vector2(screen.get_width() / 4, screen.get_height() / 2)
    enemy_pos = pg.Vector2(screen.get_width() * 3 / 4, screen.get_height() / 2)

    player = Character(spritesheet, (1, 3), player_pos, 10)
    enemy = Character(spritesheet, (2, 0), enemy_pos, 10)

    allsprites = pg.sprite.RenderPlain((player, enemy))
    clock = pg.time.Clock()

    going = True

    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                sys.exit()

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()


def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


class Character(pg.sprite.Sprite):
    """represents a character in battle"""

    def __init__(self, spritesheet, sprite, position, scale=1):
        pg.sprite.Sprite.__init__(self)

        image, rect = spritesheet.image_at_index(sprite, -1)

        if scale != 1:
            size = image.get_size()
            size = (size[0] * scale, size[1] * scale)
            image = pg.transform.scale(image, size)

        self.image, self.rect = image, image.get_rect()
        self.rect.centerx, self.rect.centery = position

    def update(self):
        pass


if __name__ == "__main__":
    main()
