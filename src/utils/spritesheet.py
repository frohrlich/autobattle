# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame


class Spritesheet:
    def __init__(self, filename, sprite_size=16):
        self.sprite_size = sprite_size
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit from e

    def image_at(self, rectangle, colorkey=None):
        """Load image from x,y,x+offset,y+offset."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, rect

    def image_at_index(self, position, colorkey=None):
        """Load image from column i and line j, calculated from sprite_size."""
        i, j = position
        rectangle = (
            i * self.sprite_size,
            j * self.sprite_size,
            self.sprite_size,
            self.sprite_size,
        )
        return self.image_at(rectangle, colorkey)

    def images_at(self, rects, colorkey=None):
        """Load multiple images, supply a list of coordinates."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a strip of images and returns them as a list."""
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, colorkey)
