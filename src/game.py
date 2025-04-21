import math
import os
import random
import sys

import pygame as pg

from battle import Battle
from character import Character
from data.data import ItemType
from data.data import Quality
from data.data import get_character_info
from data.data import get_drop_rate_by_quality
from data.data import get_random_item_identifier_by_quality
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
    score = 0
    enemy_position = (screen.get_width() * 3 / 8, screen.get_height() / 2)
    current_enemy = create_character(
        screen,
        spritesheet,
        random.choice(enemy_types),
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
                inventory.shop_button.click(event.pos)
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
            character.draw_health_bar()
        player.draw_stats()
        inventory.draw()

        if battle.has_ended():
            battle.stop()
            if not ended and battle.is_won():
                score += 1
                drop_random_item(spritesheet, inventory)
                current_enemy = create_enemy(
                    screen,
                    spritesheet,
                    random.choice(enemy_types),
                    enemy_position,
                    score,
                )
                battle = Battle([player, current_enemy])
                start_battle_button.on_click_function = battle.start
            else:
                display_end_screen(screen, score)
                if not ended:
                    ended = True
                    pg.time.set_timer(pg.QUIT, 1500)

        pg.display.flip()

    pg.quit()


def is_on_battle_side(pos, background):
    return pos[0] < background.get_width() / 2


def display_end_screen(screen, score):
    # dark overlay
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    background.set_alpha(220)
    screen.blit(background, (0, 0))

    # end text
    font_size = 48
    font = pg.font.Font(dogica_path, font_size)
    font_color = (255, 255, 255)

    text_str = "Game Over"
    text = font.render(text_str, True, font_color)
    textpos = text.get_rect(
        centerx=screen.get_width() / 2,
        centery=screen.get_height() / 2 - font_size / 2 - 10,
    )
    screen.blit(text, textpos)

    text_str = f"You defeated {score} enemies!"
    text = font.render(text_str, True, font_color)
    textpos = text.get_rect(
        centerx=screen.get_width() / 2,
        centery=screen.get_height() / 2 + font_size / 2 + 10,
    )
    screen.blit(text, textpos)


def create_background(screen):
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(dark_green)
    screen.blit(background, (0, 0))
    return background


def initialize_inventory(spritesheet, screen, player):
    potion = Item(spritesheet, "HEALTH_POTION")
    weapon_slot = Slot(screen, ItemType.WEAPON)
    shirt_slot = Slot(screen, ItemType.SHIRT)
    hat_slot = Slot(screen, ItemType.HAT)
    boot_slot = Slot(screen, ItemType.BOOTS)

    inventory = Inventory(
        spritesheet,
        screen,
        player,
        [weapon_slot, shirt_slot, hat_slot, boot_slot],
        potion,
    )
    return inventory


def create_character(screen, spritesheet, character_type, is_ally, position):
    character_info = get_character_info(character_type)
    return Character(
        screen,
        spritesheet,
        character_info.sprite,
        position,
        is_ally,
        character_info.vitality,
        character_info.strength,
    )


def create_enemy(screen, spritesheet, character_type, position, score):
    enemy = create_character(screen, spritesheet, character_type, False, position)

    enemy.max_hp = math.floor(enemy.max_hp * (1 + score * 0.1))
    enemy.hp = enemy.max_hp
    enemy.strength = math.floor(enemy.strength * (1 + score * 0.1))

    return enemy


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
        32,
        "Fight!",
        battle.start,
    )


def drop_random_item(spritesheet, inventory):
    dice_roll = random.uniform(0, 100)

    if dice_roll < get_drop_rate_by_quality(Quality.EPIC):
        identifier = get_random_item_identifier_by_quality(Quality.EPIC)
    elif dice_roll < get_drop_rate_by_quality(Quality.EPIC) + get_drop_rate_by_quality(
        Quality.RARE
    ):
        identifier = get_random_item_identifier_by_quality(Quality.RARE)
    elif dice_roll < get_drop_rate_by_quality(Quality.EPIC) + get_drop_rate_by_quality(
        Quality.RARE
    ) + get_drop_rate_by_quality(Quality.UNCOMMON):
        identifier = get_random_item_identifier_by_quality(Quality.UNCOMMON)
    else:
        identifier = get_random_item_identifier_by_quality(Quality.COMMON)

    inventory.add_item(Item(spritesheet, identifier))


if __name__ == "__main__":
    main()
