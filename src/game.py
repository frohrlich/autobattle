import os
import sys

import pygame as pg

from battle import Battle
from character import Character
from data.data import ItemType
from data.data import get_character_info
from inventory import Inventory
from inventory import Item
from inventory import Slot
from utils.button import Button
from utils.spritesheet import Spritesheet
from utils.utils import NEXT_TURN_EVENT
from utils.utils import dark_green
from utils.utils import dogica_path
from utils.utils import img_dir

if not pg.font:
    print("Warning, fonts disabled")


def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    spritesheet = Spritesheet(os.path.join(img_dir, "spritesheet.png"))
    pg.display.set_caption("Autobattle")

    background = create_background(screen)

    player_type = "ARCHER"
    player_position = (screen.get_width() / 8, screen.get_height() / 2)
    player = create_character(
        screen,
        spritesheet,
        player_type,
        True,
        player_position,
    )
    # the enemies we will have to fight in successive battles
    enemy_types = ("PIG", "WASP", "GHOST")
    # initialize first battle between our player and the first enemy of the list
    battle_index = 0
    enemy_position = (screen.get_width() * 3 / 8, screen.get_height() / 2)
    current_enemy = create_character(
        screen,
        spritesheet,
        enemy_types[battle_index],
        False,
        enemy_position,
    )
    inventory = initialize_inventory(spritesheet, screen, player)
    battle = Battle([player, current_enemy])
    start_battle_button = create_start_battle_button(screen, battle)

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
                if not battle.is_started:
                    start_battle_button.click(event.pos)
                inventory.drop_dragged_item(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not battle.is_started:
                    inventory.drag_item(event.pos)
            elif event.type == pg.MOUSEMOTION:
                if not battle.is_started:
                    inventory.move_dragged_item(event.rel)
            elif event.type == NEXT_TURN_EVENT:
                battle.next_turn()

        battle.character_group.update()

        # draw everything on screen
        draw_layout(background, screen)
        battle.character_group.draw(screen)
        if not battle.is_started and not ended:
            start_battle_button.process()
        for character in battle.character_list:
            character.draw_health_bar(screen)
        inventory.draw()

        if battle.has_ended():
            battle.stop()
            battle_index += 1
            is_won = battle.is_won()
            if is_won and battle_index < len(enemy_types):
                # go to next battle
                current_enemy = create_character(
                    screen,
                    spritesheet,
                    enemy_types[battle_index],
                    False,
                    enemy_position,
                )
                battle = Battle([player, current_enemy])
                start_battle_button.on_click_function = battle.start
            else:
                # if battle lost or won last battle, end game
                display_end_screen(screen, is_won)
                if not ended:
                    ended = True
                    pg.time.set_timer(pg.QUIT, 1000)

        pg.display.flip()

    pg.quit()


def is_on_battle_side(pos, background):
    return pos[0] < background.get_width() / 2


def display_end_screen(screen, is_won):
    # dark overlay
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    background.set_alpha(220)
    screen.blit(background, (0, 0))
    # end text
    font = pg.font.Font(dogica_path, 64)
    text_str = "You Win!" if is_won else "Game Over"
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
    return background


def initialize_inventory(spritesheet, screen, player):
    basic_sword = Item(spritesheet, "BASIC_SWORD")
    rare_sword = Item(spritesheet, "RARE_SWORD")
    epic_sword = Item(spritesheet, "EPIC_SWORD")
    basic_shirt = Item(spritesheet, "BASIC_SHIRT")
    rare_shirt = Item(spritesheet, "RARE_SHIRT")
    epic_shirt = Item(spritesheet, "EPIC_SHIRT")
    basic_hat = Item(spritesheet, "BASIC_HAT")
    rare_hat = Item(spritesheet, "RARE_HAT")
    epic_hat = Item(spritesheet, "EPIC_HAT")
    basic_boots = Item(spritesheet, "BASIC_BOOTS")
    rare_boots = Item(spritesheet, "RARE_BOOTS")
    epic_boots = Item(spritesheet, "EPIC_BOOTS")

    weapon_slot = Slot(screen, ItemType.WEAPON)
    shirt_slot = Slot(screen, ItemType.SHIRT)
    hat_slot = Slot(screen, ItemType.HAT)
    boot_slot = Slot(screen, ItemType.BOOTS)

    inventory = Inventory(
        screen,
        player,
        [weapon_slot, shirt_slot, hat_slot, boot_slot],
        basic_sword,
        rare_sword,
        epic_sword,
        basic_shirt,
        rare_shirt,
        epic_shirt,
        basic_hat,
        rare_hat,
        epic_hat,
        basic_boots,
        rare_boots,
        epic_boots,
    )
    return inventory


def create_character(screen, spritesheet, character_type, is_ally, position):
    character_info = get_character_info(character_type)
    return Character(
        spritesheet,
        character_info.sprite,
        position,
        is_ally,
        character_info.vitality,
        character_info.strength,
    )


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


def create_start_battle_button(screen, battle):
    return Button(
        screen,
        screen.get_width() / 4,
        screen.get_height() * 3 / 4,
        200,
        80,
        "Fight!",
        battle.start,
    )


if __name__ == "__main__":
    main()
