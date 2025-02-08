import os
import sys
from enum import Enum

import pygame as pg

from utils.spritesheet import Spritesheet

if not pg.font:
    print("Warning, fonts disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "../assets")
img_dir = os.path.join(data_dir, "img")
font_dir = os.path.join(data_dir, "font")
dogica_path = os.path.join(font_dir, "Dogica_Pixel.ttf")

colorkey = (255, 0, 220)
dark_green = (1, 50, 32)


def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    spritesheet = Spritesheet(os.path.join(img_dir, "spritesheet.png"))

    pg.display.set_caption("Autobattle")

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(dark_green)

    screen.blit(background, (0, 0))
    pg.display.flip()

    trident = Item(spritesheet, (8, 9), ItemType.WEAPON, strength=10, hp=12)
    anvil = Item(spritesheet, (9, 10), ItemType.WEAPON, strength=40, hp=4)
    inventory = Inventory(trident, anvil)

    slot = Slot("Weapon")
    gear = Gear(slot)

    player_pos = pg.Vector2(screen.get_width() / 8, screen.get_height() / 2)
    enemy_pos = pg.Vector2(screen.get_width() * 3 / 8, screen.get_height() / 2)
    player = Player(spritesheet, (0, 3), player_pos, True, 100, 1, 5, gear)
    enemy = Character(spritesheet, (0, 0), enemy_pos, False, 100, 5, 5)
    character_list = (player, enemy)
    battle = Battle(character_list)

    character_group = pg.sprite.RenderPlain(character_list)

    clock = pg.time.Clock()

    going = True
    ended = False
    while going:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                # release items in inventory
                if inventory.dragged_item is not None:
                    for slot in gear.slots:
                        if slot.rect.collidepoint(event.pos):
                            dragged_item = inventory.items.sprites()[
                                inventory.dragged_item
                            ]
                            slot.item = dragged_item
                            inventory.remove_item(dragged_item)
                    inventory.dragged_item = None
                if gear.dragged_item is not None:
                    if (
                        event.pos[0] > background.get_width() / 2
                        and event.pos[1] > background.get_height() / 2
                    ):
                        inventory.add_item(gear.dragged_item)
                        gear.remove_item(gear.dragged_item)
                    gear.dragged_item = None
            elif event.type == pg.MOUSEBUTTONDOWN:
                # if click on battle side of screen, go to next turn
                if event.pos[0] < background.get_width() / 2:
                    # check if previous turn is properly finished
                    if not ended and not any(
                        character.attacking for character in battle.character_list
                    ):
                        battle.next_turn()
                for i, item in enumerate(inventory.items.sprites()):
                    if item.rect.collidepoint(event.pos):
                        inventory.dragged_item = i
                for i, item in enumerate(
                    (slot.item for slot in gear.slots if slot.item is not None)
                ):
                    if item.rect.collidepoint(event.pos):
                        gear.dragged_item = item
            elif event.type == pg.MOUSEMOTION:
                if inventory.dragged_item is not None:
                    inventory.items.sprites()[inventory.dragged_item].rect.move_ip(
                        event.rel
                    )

        if any(character.is_dead() for character in battle.character_list):
            font = pg.font.Font(dogica_path, 48)
            text_str = "Game Over" if player.is_dead() else "You Win!"
            text = font.render(text_str, True, (255, 255, 255))
            textpos = text.get_rect(centerx=background.get_width() / 4, y=10)
            background.blit(text, textpos)
            if not ended:
                ended = True
                pg.time.set_timer(pg.QUIT, 1000)

        character_group.update()

        # titles
        font = pg.font.Font(dogica_path, 32)
        text = font.render("Gear", True, (200, 200, 200))
        textpos = text.get_rect(centerx=background.get_width() * 3 / 4, y=15)
        background.blit(text, textpos)
        text = font.render("Inventory", True, (200, 200, 200))
        textpos = text.get_rect(
            centerx=background.get_width() * 3 / 4,
            y=background.get_height() / 2 + 15,
        )
        background.blit(text, textpos)

        screen.blit(background, (0, 0))
        # line between battle and gear/inventory
        pg.draw.line(
            screen,
            (200, 200, 200),
            (screen.get_width() / 2, 0),
            (screen.get_width() / 2, screen.get_height()),
            5,
        )
        # line between gear and inventory
        pg.draw.line(
            screen,
            (200, 200, 200),
            (screen.get_width() / 2, screen.get_height() / 2),
            (screen.get_width(), screen.get_height() / 2),
            5,
        )
        character_group.draw(screen)
        for character in character_list:
            character.draw_health_bar(screen)
        gear.draw(screen)
        inventory.draw(screen)
        pg.display.flip()

    pg.quit()


class Battle:
    def __init__(self, character_list):
        self.character_list = character_list
        self.turn = 0

    def next_turn(self):
        index = self.turn % len(self.character_list)
        next_index = (self.turn + 1) % len(self.character_list)
        current_character = self.character_list[index]
        target = self.character_list[next_index]

        current_character.attack(target)

        self.turn += 1


class Character(pg.sprite.Sprite):
    """represents a character in battle"""

    animation_speed = 5

    def __init__(
        self,
        spritesheet,
        base_sprite,
        position,
        face_right,
        base_hp,
        base_strength,
        scale=1,
    ):
        pg.sprite.Sprite.__init__(self)

        self.base_sprite = base_sprite
        self.spritesheet = spritesheet
        self.face_right = face_right
        self.max_hp = base_hp
        self.hp = base_hp
        self._strength = base_strength

        # which sprite to use depending on character facing right or left
        if face_right:
            use_sprite = (base_sprite[0] + 1, base_sprite[1])
        else:
            use_sprite = (base_sprite[0] + 2, base_sprite[1])

        image, rect = spritesheet.image_at_index(use_sprite, colorkey)

        if scale != 1:
            size = image.get_size()
            size = (size[0] * scale, size[1] * scale)
            image = pg.transform.scale(image, size)

        self.image, self.rect = image, image.get_rect()
        self.rect.centerx, self.rect.centery = position
        self.initial_position = position

        self.attacking = False
        self.returning = False

    def update(self):
        if self.attacking:
            self.animate_attack()

    def attack(self, target):
        self.attacking = True
        target.hp -= self.strength

    @property
    def strength(self):
        return self._strength

    def animate_attack(self):
        """make character move towards enemy and then return to original position"""

        direction = 1 if self.face_right else -1

        target_position = (
            self.initial_position[0] + direction * 50,
            self.initial_position[1],
        )
        dx = target_position[0] - self.rect.centerx
        dx_initial = self.initial_position[0] - self.rect.centerx

        # when returned close to initial position, stop
        if self.returning and abs(dx_initial) <= self.animation_speed:
            self.attacking = False
            self.returning = False
            self.rect.centerx, self.rect.centery = self.initial_position
            return
        # move towards enemy
        elif not self.returning and abs(dx) > 3:
            self.rect.centerx += direction * self.animation_speed
        # when reaching limit, start returning to initial position
        else:
            self.returning = True
            self.rect.centerx -= direction * self.animation_speed

    def draw_health_bar(self, screen):
        pg.draw.rect(
            screen,
            (255, 0, 0),
            (
                self.rect.left,
                self.rect.top - 20,
                self.rect.width,
                10,
            ),
        )
        pg.draw.rect(
            screen,
            (0, 128, 0),
            (
                self.rect.left,
                self.rect.top - 20,
                self.rect.width * (1 - (self.max_hp - self.hp) / self.max_hp),
                10,
            ),
        )

    def is_dead(self):
        return self.hp <= 0


class Player(Character):
    def __init__(
        self,
        spritesheet,
        base_sprite,
        position,
        face_right,
        base_hp,
        base_strength,
        scale=1,
        gear=None,
    ):
        Character.__init__(
            self,
            spritesheet,
            base_sprite,
            position,
            face_right,
            base_hp,
            base_strength,
            scale,
        )
        self.items = []
        self.gear = gear
        if gear:
            self.max_hp = self.max_hp + sum((item.hp for item in self.get_items()))
            self.hp = self.max_hp

    @property
    def strength(self):
        return self._strength + sum((item.strength for item in self.get_items()))

    def get_items(self):
        return (slot.item for slot in self.gear.slots if slot.item is not None)


class Item(pg.sprite.Sprite):
    """represents a wearable item with its bonuses"""

    scale = 4

    def __init__(self, spritesheet, sprite, item_type, strength=0, hp=0):
        pg.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.sprite = sprite
        self.item_type = item_type
        self.strength = strength
        self.hp = hp

        image, rect = spritesheet.image_at_index(sprite, colorkey)

        size = image.get_size()
        size = (size[0] * self.scale, size[1] * self.scale)
        image = pg.transform.scale(image, size)

        self.image, self.rect = image, image.get_rect()


class ItemType(Enum):
    WEAPON = 1


class Inventory:
    def __init__(self, *args):
        self.items = pg.sprite.RenderPlain(args)
        self.dragged_item = None

    def add_item(self, item):
        self.items.add(item)

    def remove_item(self, item):
        self.items.remove(item)

    def draw(self, screen):
        for i, item in enumerate(self.items.sprites()):
            base_x = screen.get_width() / 2 + 20 + i * 70
            base_y = screen.get_height() / 2 + 70
            image_size = 64
            if self.dragged_item != i:
                item.rect = pg.Rect(
                    base_x,
                    base_y,
                    image_size,
                    image_size,
                )

        self.items.draw(screen)


class Gear:
    """currently equiped items"""

    def __init__(self, *args):
        self.slots = list(args)
        self.dragged_item = None

    def remove_item(self, item):
        for slot in self.slots:
            if slot.item == item:
                slot.item = None

    def draw(self, screen):
        for slot in self.slots:
            slot.draw(screen, self.dragged_item)


class Slot:
    """item slot in gear"""

    def __init__(self, item_type):
        self.item_type = item_type
        self.item = None
        self.rect = None

    def draw(self, screen, dragged_item):
        base_x = screen.get_width() / 2 + 40
        base_y = 70
        size = 76
        image_size = 64
        outer_rect = (base_x, base_y, size, size)
        # outline
        self.rect = pg.draw.rect(
            screen,
            (100, 100, 100),
            outer_rect,
        )
        # title
        font = pg.font.Font(dogica_path, 16)
        text = font.render(self.item_type, True, (255, 255, 255))
        textpos = text.get_rect(centerx=base_x + size / 2, centery=base_y - 20)
        screen.blit(text, textpos)

        if self.item:
            if dragged_item == self.item:
                screen.blit(self.item.image, pg.mouse.get_pos())
            else:
                screen.blit(
                    self.item.image,
                    (
                        base_x + (size - image_size) / 2,
                        base_y + (size - image_size) / 2,
                    ),
                )


if __name__ == "__main__":
    main()
