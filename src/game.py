import os
import sys

import pygame as pg

from battle import Battle
from character import Character
from character import Player
from data.data import ItemType
from data.data import character_infos
from inventory import Inventory
from inventory import Item
from inventory import Slot
from utils.spritesheet import Spritesheet
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
    inventory = initialize_inventory(spritesheet, screen)

    player_type = "ARCHER"
    player = create_player(screen, spritesheet, player_type, inventory)
    # the enemies we will have to fight in successive battles
    enemy_types = ("PIG", "WASP", "GHOST")
    # initialize first battle between our player and the first enemy of the list
    battle_index = 0
    current_enemy = create_enemy(screen, spritesheet, enemy_types[battle_index])
    battle = Battle([player, current_enemy])

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
                else:
                    inventory.drag_item(event.pos)
            elif event.type == pg.MOUSEMOTION:
                inventory.move_dragged_item(event.rel)

        battle.character_group.update()

        # draw everything on screen
        draw_layout(background, screen)
        battle.character_group.draw(screen)
        for character in battle.character_list:
            character.draw_health_bar(screen)
        inventory.draw()

        if battle.has_ended():
            battle_index += 1
            is_won = battle.is_won()
            if is_won and battle_index < len(enemy_types):
                # go to next battle
                current_enemy = create_enemy(
                    screen, spritesheet, enemy_types[battle_index]
                )
                battle = Battle([player, current_enemy])
            else:
                # if battle lost or won last battle, end game
                display_end_text(screen, is_won)
                if not ended:
                    ended = True
                    pg.time.set_timer(pg.QUIT, 1000)

        pg.display.flip()

    pg.quit()


def is_on_battle_side(pos, background):
    return pos[0] < background.get_width() / 2


def display_end_text(screen, is_won):
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
    pg.display.flip()
    return background


def initialize_inventory(spritesheet, screen):
    trident = Item(spritesheet, "TRIDENT")
    anvil = Item(spritesheet, "ANVIL")
    slot = Slot(ItemType.WEAPON)
    inventory = Inventory(screen, [slot], trident, anvil)
    return inventory


def create_enemy(screen, spritesheet, character_type):
    enemy_pos = pg.Vector2(screen.get_width() * 3 / 8, screen.get_height() / 2)
    enemy_info = character_infos[character_type]
    return Character(
        spritesheet,
        enemy_info["sprite"],
        enemy_pos,
        False,
        enemy_info["hp"],
        enemy_info["strength"],
    )


def create_player(screen, spritesheet, character_type, inventory):
    player_info = character_infos[character_type]
    player_pos = pg.Vector2(screen.get_width() / 8, screen.get_height() / 2)
    return Player(
        spritesheet,
        player_info["sprite"],
        player_pos,
        True,
        player_info["hp"],
        player_info["strength"],
        inventory,
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


if __name__ == "__main__":
    main()
