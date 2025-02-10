import random

import pygame as pg

from utils.utils import NEXT_TURN_EVENT


class Battle:
    turn_duration = 500

    def __init__(self, character_list):
        self.character_group = pg.sprite.RenderPlain(character_list)
        self.allies = [character for character in character_list if character.is_ally]
        self.enemies = [
            character for character in character_list if not character.is_ally
        ]
        self.turn = 0
        self.is_started = False

    def start(self):
        self.next_turn()
        pg.time.set_timer(NEXT_TURN_EVENT, self.turn_duration)
        self.is_started = True

    def stop(self):
        pg.time.set_timer(NEXT_TURN_EVENT, 0)
        self.is_started = False

    def next_turn(self):
        index = self.turn % len(self.character_list)
        current_character = self.character_list[index]
        adversary_list = self.enemies if current_character.is_ally else self.allies
        target = random.choice(adversary_list)

        current_character.attack(target)

        self.turn += 1

    def is_previous_turn_finished(self):
        return not any(character.attacking for character in self.character_list)

    def has_ended(self):
        return self.is_won() or self.is_lost()

    def is_won(self):
        return all(character.is_dead() for character in self.enemies)

    def is_lost(self):
        return all(character.is_dead() for character in self.allies)

    @property
    def character_list(self):
        return self.character_group.sprites()
