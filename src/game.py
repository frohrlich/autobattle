import os
import sys

import pygame as pg

from character import Character, Player
from inventory import (
    Inventory,
    Item,
    ItemType,
    Slot,
)
from utils.spritesheet import Spritesheet
from utils.utils import dark_green, dogica_path, img_dir

if not pg.font:
    print("Warning, fonts disabled")


def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    spritesheet = Spritesheet(os.path.join(img_dir, "spritesheet.png"))
    pg.display.set_caption("Autobattle")

    background = create_background(screen)
    inventory = initialize_inventory(spritesheet, screen)

    character_list, character_group = create_characters(screen, spritesheet, inventory)
    battle = Battle(character_list)

    # start main game loop
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
                inventory.drop_dragged_item(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN:
                # if click on battle side of screen, go to next turn
                if is_on_battle_side(event.pos, background):
                    if not ended and battle.is_previous_turn_finished():
                        battle.next_turn()
                inventory.drag_item(event.pos)
            elif event.type == pg.MOUSEMOTION:
                inventory.move_dragged_item(event.rel)

        character_group.update()

        # draw everything on screen
        draw_layout(background, screen)
        character_group.draw(screen)
        for character in character_list:
            character.draw_health_bar(screen)
        inventory.draw()

        if battle.has_ended():
            display_end_text(screen)
            if not ended:
                ended = True
                pg.time.set_timer(pg.QUIT, 1000)

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

    def is_previous_turn_finished(self):
        return not any(character.attacking for character in self.character_list)

    def has_ended(self):
        return any(character.is_dead() for character in self.character_list)


def is_on_battle_side(pos, background):
    return pos[0] < background.get_width() / 2


def display_end_text(screen):
    font = pg.font.Font(dogica_path, 64)
    text_str = "Game Over"
    text = font.render(text_str, True, (255, 255, 255))
    textpos = text.get_rect(
        centerx=screen.get_width() / 2, centery=screen.get_height() / 2
    )
    screen.blit(text, textpos)


def create_background(screen):
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(dark_green)
    screen.blit(background, (0, 0))
    pg.display.flip()
    return background


def initialize_inventory(spritesheet, screen):
    trident = Item(spritesheet, (8, 9), ItemType.WEAPON, strength=10, hp=12)
    anvil = Item(spritesheet, (9, 10), ItemType.WEAPON, strength=40, hp=4)
    slot = Slot("Weapon")
    inventory = Inventory(screen, [slot], trident, anvil)
    return inventory


def create_characters(screen, spritesheet, inventory):
    player_pos = pg.Vector2(screen.get_width() / 8, screen.get_height() / 2)
    enemy_pos = pg.Vector2(screen.get_width() * 3 / 8, screen.get_height() / 2)
    player = Player(spritesheet, (0, 3), player_pos, True, 100, 1, inventory)
    enemy = Character(spritesheet, (0, 0), enemy_pos, False, 100, 5)
    character_list = (player, enemy)
    character_group = pg.sprite.RenderPlain(character_list)
    return character_list, character_group


def draw_layout(background, screen):
    font = pg.font.Font(dogica_path, 32)

    text = font.render("Battle", True, (200, 200, 200))
    textpos = text.get_rect(centerx=background.get_width() / 4, y=10)
    background.blit(text, textpos)

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
    # line between battle and inventory
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


if __name__ == "__main__":
    main()
