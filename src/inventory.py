import pygame as pg

from character import colorkey
from data.data import item_infos
from utils.utils import dogica_path


class Item(pg.sprite.Sprite):
    """Represents a wearable item with its bonuses."""

    scale = 4

    def __init__(self, spritesheet, item_type):
        item_info = item_infos[item_type]
        pg.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.sprite = item_info["sprite"]
        self.item_type = item_info["item_type"]
        self.strength = item_info["strength"]
        self.hp = item_info["hp"]

        image, rect = spritesheet.image_at_index(self.sprite, colorkey)

        size = image.get_size()
        size = (size[0] * self.scale, size[1] * self.scale)
        image = pg.transform.scale(image, size)

        self.image, self.rect = image, image.get_rect()


class Inventory:
    """Represents the inventory and gear slots."""

    def __init__(self, screen, slots, *args):
        self.screen = screen
        self.items = pg.sprite.RenderPlain(args)
        self.slots = slots
        self.dragged_item = None
        self.refresh_item_positions()

    def add_item(self, item):
        self.items.add(item)
        self.refresh_item_positions()

    def remove_item(self, item):
        self.items.remove(item)
        self.refresh_item_positions()

    def draw(self):
        for slot in self.slots:
            slot.draw(self.screen)

        self.items.draw(self.screen)

    def drag_item(self, pos):
        for item in self.items.sprites():
            if item.rect.collidepoint(pos):
                self.dragged_item = item

    def drop_dragged_item(self, pos):
        """Drop a dragged item from the inventory into a gear slot, and vice versa."""
        if self.dragged_item is not None:
            # move from gear slot to inventory
            if slot := self.get_slot(self.dragged_item):
                if is_pos_inside_inventory(pos, self.screen):
                    slot.item = None
                    # move item to end of inventory
                    self.items.remove(self.dragged_item)
                    self.items.add(self.dragged_item)
            else:
                # move from inventory to gear slot
                for slot in self.slots:
                    # slot must be empty and same type as item
                    if (
                        slot.rect.collidepoint(pos)
                        and slot.item_type == self.dragged_item.item_type
                        and slot.item is None
                    ):
                        slot.item = self.dragged_item
                        break
            self.dragged_item = None
            self.refresh_item_positions()

    def move_dragged_item(self, rel):
        if self.dragged_item is not None:
            self.dragged_item.rect.move_ip(rel)

    def get_slot(self, item):
        return next((slot for slot in self.slots if slot.item == item), None)

    def put_item_inside_inventory(self, index, item):
        self.base_x = self.screen.get_width() / 2 + 20 + index * 70
        base_y = self.screen.get_height() / 2 + 70
        image_size = 64
        item.rect = pg.Rect(
            self.base_x,
            base_y,
            image_size,
            image_size,
        )
        return image_size

    def refresh_item_positions(self):
        items_in_slot = (item for item in self.items.sprites() if self.get_slot(item))
        for item in items_in_slot:
            slot = self.get_slot(item)
            slot.put_item_inside_slot(item)

        items_in_inventory = (
            item for item in self.items.sprites() if not self.get_slot(item)
        )
        for i, item in enumerate(items_in_inventory):
            self.put_item_inside_inventory(i, item)


class Slot:
    def __init__(self, item_type):
        self.item_type = item_type
        self.item = None
        self.rect = None
        self.base_x = 0
        self.base_y = 70
        self.size = 76
        self.image_size = 64

    def draw(self, screen):
        self.base_x = screen.get_width() / 2 + 40

        outer_rect = (self.base_x, self.base_y, self.size, self.size)
        # outline
        self.rect = pg.draw.rect(
            screen,
            (100, 100, 100),
            outer_rect,
        )
        # title
        font = pg.font.Font(dogica_path, 16)
        text = font.render(self.item_type.name.capitalize(), True, (255, 255, 255))
        textpos = text.get_rect(
            centerx=self.base_x + self.size / 2, centery=self.base_y - 20
        )
        screen.blit(text, textpos)

    def put_item_inside_slot(self, item):
        item.rect = pg.Rect(
            self.base_x + (self.size - self.image_size) / 2,
            self.base_y + (self.size - self.image_size) / 2,
            self.image_size,
            self.image_size,
        )


def is_pos_inside_inventory(pos, screen):
    return pos[0] > screen.get_width() / 2 and pos[1] > screen.get_height() / 2
