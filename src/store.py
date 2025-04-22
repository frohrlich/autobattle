import math

import pygame as pg

from data.data import get_buy_price_by_quality
from data.data import get_random_item_identifier
from inventory import Item
from utils.button import Button
from utils.utils import dark_green
from utils.utils import dogica_path


class Store:
    item_count = 3
    gold_image_sprite = (10, 3)

    def __init__(self, screen, spritesheet, inventory):
        self.screen = screen
        self.spritesheet = spritesheet
        self.inventory = inventory
        self.items = pg.sprite.RenderPlain()
        self.draw_store_outline()
        self.create_buy_button()
        self.gold_icon, _ = self.spritesheet.image_at_index(
            self.gold_image_sprite, colorkey=-1
        )
        self.dragged_item = None

    def draw_store_outline(self):
        margin = 30
        title_margin = 10
        outline_thickness = 5
        outline_color = (255, 255, 255)
        vertical_offset = 69
        # inside
        pg.draw.rect(
            self.screen,
            dark_green,
            (
                margin,
                margin,
                self.screen.get_width() - margin * 2,
                self.screen.get_height() - vertical_offset - margin * 2,
            ),
        )
        # border
        pg.draw.rect(
            self.screen,
            outline_color,
            (
                margin - outline_thickness,
                margin - outline_thickness,
                self.screen.get_width() - margin * 2 + outline_thickness,
                self.screen.get_height()
                - vertical_offset
                - margin * 2
                + outline_thickness,
            ),
            outline_thickness,
        )
        # title
        font = pg.font.Font(dogica_path, 32)
        text = font.render("Store", True, (200, 200, 200))
        textpos = text.get_rect(
            centerx=self.screen.get_width() / 2, y=margin + title_margin
        )
        self.screen.blit(text, textpos)

    def draw_item_prices(self):
        font_size = 16
        margin = 5
        x_offset = 10
        for item in self.items.sprites():
            font = pg.font.Font(dogica_path, font_size)
            text = font.render(
                str(get_buy_price_by_quality(item.quality)), True, (200, 200, 200)
            )
            textpos = text.get_rect(
                centerx=item.rect.centerx - x_offset,
                y=item.rect.top - font_size - margin,
            )
            self.screen.blit(text, textpos)

            gold_rect = self.gold_icon.get_rect()
            gold_rect.left = textpos.right + margin
            gold_rect.centery = textpos.centery
            self.screen.blit(self.gold_icon, gold_rect)

    def draw(self):
        self.draw_store_outline()
        self.items.draw(self.screen)
        self.buy_button.process()

        self.draw_item_prices()

        if self.dragged_item:
            self.buy_button.change_text("Buy!")
            self.buy_button.change_font_size(32)
            self.screen.blit(self.dragged_item.image, self.dragged_item.rect)
        else:
            self.buy_button.change_text("Drag here to buy")
            self.buy_button.change_font_size(16)

        # show infobox
        if self.dragged_item is None:
            for item in self.items:
                item.process(self.screen)

    def drag_item(self, pos):
        for item in self.items.sprites():
            if item.rect.collidepoint(pos):
                self.dragged_item = item
                self.buy_button.on_click_function = self.buy_item

    def drop_dragged_item(self):
        if self.dragged_item is not None:
            self.dragged_item = None
            self.buy_button.on_click_function = None
            self.refresh_item_positions()

    def move_dragged_item(self, rel):
        if self.dragged_item is not None:
            self.dragged_item.rect.move_ip(rel)

    def refurnish(self):
        self.items.empty()
        for _ in range(self.item_count):
            item = Item(self.spritesheet, get_random_item_identifier())
            self.items.add(item)
        self.refresh_item_positions()

    def create_buy_button(self):
        height = 80
        width = 220
        self.buy_button = Button(
            self.screen,
            self.screen.get_width() / 2,
            self.screen.get_height() / 2 + 30,
            width,
            height,
            16,
            "Drag here to buy",
            None,
            {
                "normal": "#aaa200",
                "hover": "#666400",
                "pressed": "#333100",
            },
        )

    def buy_item(self):
        if self.dragged_item:
            price = get_buy_price_by_quality(self.dragged_item.quality)
            if self.inventory.gold >= price:
                self.inventory.gold -= price
                self.inventory.add_item(self.dragged_item)
                self.items.remove(self.dragged_item)
                self.refresh_item_positions()
            self.dragged_item = None
            self.buy_button.on_click_function = None
            self.refresh_item_positions()

    def refresh_item_positions(self):
        image_size = 64
        margin = 80
        box_size = image_size + margin

        for i, item in enumerate(self.items.sprites()):
            base_x = (
                self.screen.get_width() / 2
                + box_size * (i - math.floor(self.item_count / 2))
                - image_size / 2
            )
            base_y = self.screen.get_height() / 4
            item.rect = pg.Rect(
                base_x,
                base_y,
                image_size,
                image_size,
            )
