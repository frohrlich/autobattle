import pygame as pg

from data.data import ItemType
from data.data import Quality
from data.data import get_item_info
from data.data import get_sell_price_by_quality
from utils.button import Button
from utils.utils import dogica_bold_path
from utils.utils import dogica_path
from utils.utils import draw_borders


class Item(pg.sprite.Sprite):
    """Represents a wearable item with its bonuses."""

    scale = 4

    def __init__(self, spritesheet, identifier):
        self.item_info = get_item_info(identifier)
        pg.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.sprite = self.item_info.sprite
        self.item_type = self.item_info.item_type
        self.quality = self.item_info.quality
        self.strength = self.item_info.strength
        self.vitality = self.item_info.vitality
        self.health_bonus = self.item_info.health_bonus
        self.name = self.item_info.name

        image, rect = spritesheet.image_at_index(self.sprite)

        size = image.get_size()
        size = (size[0] * self.scale, size[1] * self.scale)
        image = pg.transform.scale(image, size)

        self.image, self.rect = image, image.get_rect()

    def process(self, screen):
        mousePos = pg.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.draw_infobox(screen)

    def draw_infobox(self, screen):
        font = pg.font.Font(dogica_path, 16)
        font_bold = pg.font.Font(dogica_bold_path, 16)
        font_small = pg.font.Font(dogica_path, 12)
        text_color = (25, 25, 25)
        text_small_color = (50, 50, 50)
        text_name_color = self.get_quality_color()
        margin_y = 8
        margin_x = 8
        border_width = 3
        height = margin_y
        width = margin_x
        # health bonus
        if self.item_info.health_bonus:
            text_hp_bonus = font.render(
                f"+{self.item_info.health_bonus} HP", True, text_color
            )
            text_hp_bonus_rect = text_hp_bonus.get_rect()
            width = max(width, text_hp_bonus_rect.width)
            height += text_hp_bonus_rect.height + margin_y
            text_hp_bonus_rect.bottom = self.rect.top - margin_y
            text_hp_bonus_rect.left = self.rect.right + margin_x
        # strength
        if self.item_info.strength:
            text_str = font.render(
                f"strength: {self.item_info.strength}", True, text_color
            )
            text_str_rect = text_str.get_rect()
            width = max(width, text_str_rect.width)
            height += text_str_rect.height + margin_y
            text_str_rect.bottom = self.rect.top - margin_y
            text_str_rect.left = self.rect.right + margin_x
        # vitality
        if self.item_info.vitality:
            text_hp = font.render(
                f"vitality: {self.item_info.vitality}", True, text_color
            )
            text_hp_rect = text_hp.get_rect()
            width = max(width, text_hp_rect.width)
            text_hp_rect.bottom = self.rect.top - height
            text_hp_rect.left = self.rect.right + margin_x
            height += text_hp_rect.height + margin_y
        # item type
        text_type = font_small.render(
            self.item_type.name.capitalize(), True, text_small_color
        )
        text_type_rect = text_type.get_rect()
        width = max(width, text_type_rect.width)
        text_type_rect.bottom = self.rect.top - height
        text_type_rect.left = self.rect.right + margin_x
        height += text_type_rect.height + margin_y
        # name
        text_name = font_bold.render(self.name, True, text_name_color)
        text_name_rect = text_name.get_rect()
        width = max(width, text_name_rect.width)
        text_name_rect.bottom = self.rect.top - height
        text_name_rect.left = self.rect.right + margin_x
        height += text_name_rect.height + margin_y

        width += margin_x * 2

        rect = pg.Rect(
            self.rect.right,
            self.rect.top - height,
            width,
            height,
        )

        if rect.right >= screen.get_width():
            rect.right = self.rect.left
            left = self.rect.left - width + margin_x
            text_name_rect.left = left
            text_type_rect.left = left
            if self.item_info.vitality:
                text_hp_rect.left = left
            if self.item_info.strength:
                text_str_rect.left = left
            if self.item_info.health_bonus:
                text_hp_bonus_rect.left = left

        if rect.top <= 0:
            offset = self.rect.bottom - rect.top
            rect.top = self.rect.bottom
            text_name_rect.y += offset
            text_type_rect.y += offset
            if self.item_info.vitality:
                text_hp_rect.y += offset
            if self.item_info.strength:
                text_str_rect.y += offset
            if self.item_info.health_bonus:
                text_hp_bonus_rect.y = offset

        rect = pg.draw.rect(screen, "#00aa00", rect)

        draw_borders(
            screen,
            rect.centerx,
            rect.centery,
            rect.width,
            rect.height + 1,
            border_width,
            (100, 100, 100),
        )
        screen.blit(text_type, text_type_rect)
        screen.blit(text_name, text_name_rect)
        if self.item_info.strength:
            screen.blit(text_str, text_str_rect)
        if self.item_info.vitality:
            screen.blit(text_hp, text_hp_rect)
        if self.item_info.health_bonus:
            screen.blit(text_hp_bonus, text_hp_bonus_rect)

    def get_quality_color(self):
        match self.quality:
            case Quality.COMMON:
                return "#FFFFFF"
            case Quality.UNCOMMON:
                return "#1eff00"
            case Quality.RARE:
                return "#0070dd"
            case Quality.EPIC:
                return "#a335ee"
            case _:
                raise RuntimeError("Invalid item quality")


class Inventory:
    """Represents the inventory and gear slots."""

    gold_image_sprite = (10, 3)

    def __init__(self, spritesheet, screen, player, slots, *args):
        self.spritesheet = spritesheet
        self.screen = screen
        self.player = player
        self.gold = 0
        self.is_store_activated = False
        self.items = pg.sprite.RenderPlain(args)
        self.slots = slots
        self.dragged_item = None
        self.create_store_button()
        self.refresh_item_positions()

    def add_item(self, item):
        self.items.add(item)
        self.refresh_item_positions()

    def remove_item(self, item):
        self.items.remove(item)
        if slot := next((slot for slot in self.slots if slot.item == item), None):
            slot.item = None
        self.refresh_item_positions()

    def draw(self):
        for slot in self.slots:
            slot.draw(self.screen)

        self.items.draw(self.screen)

        self.store_button.process()

        if self.dragged_item:
            self.store_button.change_text("Sell!")
            self.screen.blit(self.dragged_item.image, self.dragged_item.rect)
        elif not self.is_store_activated:
            self.store_button.change_text("Store")

        self.draw_gold()

        # show infobox
        if self.dragged_item is None:
            for item in self.items:
                item.process(self.screen)

    def drag_item(self, pos):
        for item in self.items.sprites():
            if item.rect.collidepoint(pos):
                self.dragged_item = item
                self.store_button.on_click_function = self.sell_item

    def drop_dragged_item(self, pos):
        """Drop a dragged item.

        Into a gear slot, the inventory, or the player (for potions).
        """
        if self.dragged_item is not None:
            if (
                self.dragged_item.item_type == ItemType.POTION
                and self.player.rect.collidepoint(pos)
            ):
                if self.player.hp < self.player.max_hp:
                    self.player.consume_potion(self.dragged_item)
                    self.remove_item(self.dragged_item)
            elif slot := self.get_slot(self.dragged_item):
                if is_pos_inside_inventory(pos, self.screen):
                    self.move_item_from_slot_to_inventory(slot)
            else:
                for slot in self.slots:
                    if (
                        slot.item_type == self.dragged_item.item_type
                        and slot.rect.collidepoint(pos)
                    ):
                        if slot.item is not None:
                            self.move_item_from_slot_to_inventory(slot)
                        self.move_item_from_inventory_to_slot(slot, self.dragged_item)
                        break
            self.dragged_item = None
            self.refresh_item_positions()
            self.store_button.on_click_function = self.open_store

    def move_dragged_item(self, rel):
        if self.dragged_item is not None:
            self.dragged_item.rect.move_ip(rel)

    def get_slot(self, item):
        return next((slot for slot in self.slots if slot.item == item), None)

    def put_item_inside_inventory(self, index, item):
        image_size = 64
        margin = 10

        box_size = image_size + margin
        base_x = self.screen.get_width() / 2 + 20 + (index % 8) * box_size
        base_y = self.screen.get_height() / 2 + (index // 8 + 1) * box_size
        item.rect = pg.Rect(
            base_x,
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

    def move_item_from_slot_to_inventory(self, slot):
        self.player.remove_item(slot.item)
        # move item to end of inventory
        self.items.remove(slot.item)
        self.items.add(slot.item)

        slot.item = None

    def move_item_from_inventory_to_slot(self, slot, item):
        self.player.add_item(item)
        slot.item = item

    def create_store_button(self):
        margin = 10
        height = 80
        width = 115
        self.store_button = Button(
            self.screen,
            self.screen.get_width() - width / 2 - margin,
            self.screen.get_height() - height / 2 - margin,
            width,
            height,
            24,
            "Store",
            self.open_store,
            {
                "normal": "#aaa200",
                "hover": "#666400",
                "pressed": "#333100",
            },
        )

    def sell_item(self):
        if self.dragged_item:
            self.gold += get_sell_price_by_quality(self.dragged_item.quality)
            self.remove_item(self.dragged_item)
            self.dragged_item = None
            self.store_button.on_click_function = self.open_store

    def draw_gold(self):
        margin = 8
        icon_scale = 2

        gold_image, _ = self.spritesheet.image_at_index(
            self.gold_image_sprite, colorkey=-1
        )
        size = gold_image.get_size()
        size = (size[0] * icon_scale, size[1] * icon_scale)
        gold_image = pg.transform.scale(gold_image, size)
        gold_rect = gold_image.get_rect()

        gold_rect.right = self.store_button.rect.left - margin
        gold_rect.centery = self.store_button.centery
        self.screen.blit(gold_image, gold_rect)

        font = pg.font.Font(dogica_path, 24)
        text = font.render(str(self.gold), True, (255, 255, 255))
        textpos = text.get_rect(
            right=gold_rect.left - margin,
            centery=gold_rect.centery,
        )
        self.screen.blit(text, textpos)

    def open_store(self):
        self.is_store_activated = True
        self.store_button.change_text("Exit")
        self.store_button.on_click_function = self.close_store

    def close_store(self):
        self.is_store_activated = False
        self.store_button.change_text("Store")
        self.store_button.on_click_function = self.open_store


class Slot:
    def __init__(self, screen, item_type):
        self.screen = screen
        self.item_type = item_type
        self.item = None
        self.rect = None
        self.size = 76
        self.image_size = 64
        self.position_slot()

    def draw(self, screen):
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

    def position_slot(self):
        border_x = 40
        border_y = 70
        match self.item_type:
            case ItemType.WEAPON:
                self.base_x = self.screen.get_width() / 2 + border_x
                self.base_y = border_y
            case ItemType.SHIRT:
                self.base_x = self.screen.get_width() - self.size - border_x
                self.base_y = border_y
            case ItemType.HAT:
                self.base_x = self.screen.get_width() - self.size - border_x * 2
                self.base_y = border_y * 2 + self.size
            case ItemType.BOOTS:
                self.base_x = self.screen.get_width() / 2 + border_x * 2
                self.base_y = border_y * 2 + self.size
            case _:
                raise RuntimeError("Invalid item type for slot")


def is_pos_inside_inventory(pos, screen):
    return pos[0] > screen.get_width() / 2 and pos[1] > screen.get_height() / 2
