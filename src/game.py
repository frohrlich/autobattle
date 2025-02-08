import os
import sys
from enum import Enum

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

    trident = Item(spritesheet, (8, 9), ItemType.WEAPON, strength=5, hp=12)
    anvil = Item(spritesheet, (9, 10), ItemType.WEAPON, strength=5, hp=4)
    inventory = Inventory(trident, anvil)

    player_pos = pg.Vector2(screen.get_width() / 8, screen.get_height() / 2)
    enemy_pos = pg.Vector2(screen.get_width() * 3 / 8, screen.get_height() / 2)
    player = Player(spritesheet, (0, 3), player_pos, True, 100, 5, 5, inventory)
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
                # check if previous turn is properly finished
                if not ended and not any(
                    character.attacking for character in battle.character_list
                ):
                    battle.next_turn()
        if any(character.is_dead() for character in battle.character_list):
            if pg.font:
                font = pg.font.Font(None, 64)
                text_str = "Game Over" if player.is_dead() else "You Win!"
                text = font.render(text_str, True, (255, 255, 255))
                textpos = text.get_rect(centerx=background.get_width() / 4, y=10)
                background.blit(text, textpos)
            if not ended:
                ended = True
                pg.time.set_timer(pg.QUIT, 1000)

        character_group.update()

        if pg.font:
            font = pg.font.Font(None, 64)
            text = font.render("Inventory", True, (200, 200, 200))
            textpos = text.get_rect(centerx=background.get_width() * 3 / 4, y=10)
            background.blit(text, textpos)

        screen.blit(background, (0, 0))
        inventory.draw(screen)
        pg.draw.line(
            screen,
            (200, 200, 200),
            (screen.get_width() / 2, 0),
            (screen.get_width() / 2, screen.get_height()),
            5,
        )
        character_group.draw(screen)
        for character in character_list:
            character.draw_health_bar(screen)
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

        image, rect = spritesheet.image_at_index(use_sprite, -1)

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
        inventory=None,
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
        self.inventory = inventory
        if inventory:
            self.max_hp = self.max_hp + sum((item.hp for item in self.inventory.items))
            self.hp = self.max_hp

    @property
    def strength(self):
        return self._strength + sum((item.strength for item in self.inventory.items))


class Item:
    """represents a wearable item with its bonuses"""

    def __init__(self, spritesheet, sprite, item_type, strength=0, hp=0):
        self.spritesheet = spritesheet
        self.sprite = sprite
        self.item_type = item_type
        self.strength = strength
        self.hp = hp

    def get_image(self):
        return self.spritesheet.image_at_index(self.sprite, -1)


class ItemType(Enum):
    WEAPON = 1


class Inventory:
    def __init__(self, *args):
        self.items = list(args)

    def add_item(self, item):
        self.items.append(item)

    def draw(self, screen):
        for i, item in enumerate(self.items):
            base_x = screen.get_width() / 2 + 20 + i * 70
            base_y = 80
            size = 60
            image_size = 64
            outer_rect = (base_x, base_y, size, size)
            inner_rect = (
                base_x + (size - image_size) / 2,
                base_y + (size - image_size) / 2,
                size - image_size,
                size - image_size,
            )
            # outline
            pg.draw.rect(
                screen,
                (100, 100, 100),
                outer_rect,
            )
            # item image
            image, rect = item.get_image()
            size = image.get_size()
            size = (size[0] * 4, size[1] * 4)
            image = pg.transform.scale(image, size)
            screen.blit(image, inner_rect)


if __name__ == "__main__":
    main()
