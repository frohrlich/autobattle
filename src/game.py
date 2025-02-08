import os
import sys

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

    player_pos = pg.Vector2(screen.get_width() / 4, screen.get_height() / 2)
    enemy_pos = pg.Vector2(screen.get_width() * 3 / 4, screen.get_height() / 2)

    player = Character(spritesheet, (0, 3), player_pos, True, 100, 25, 10)
    enemy = Character(spritesheet, (0, 0), enemy_pos, False, 100, 5, 10)
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
                if not any(character.attacking for character in battle.character_list):
                    battle.next_turn()
        if any(character.is_dead() for character in battle.character_list):
            if pg.font:
                font = pg.font.Font(None, 64)
                text_str = "Game Over" if player.is_dead() else "You Win!"
                text = font.render(text_str, True, (255, 255, 255))
                textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
                background.blit(text, textpos)
            if not ended:
                ended = True
                pg.time.set_timer(pg.QUIT, 1000)

        character_group.update()

        screen.blit(background, (0, 0))
        character_group.draw(screen)
        for character in character_list:
            pg.draw.rect(
                screen,
                (255, 0, 0),
                (
                    character.rect.left,
                    character.rect.top - 20,
                    character.rect.width,
                    10,
                ),
            )
            pg.draw.rect(
                screen,
                (0, 128, 0),
                (
                    character.rect.left,
                    character.rect.top - 20,
                    character.rect.width
                    * (1 - (character.max_hp - character.hp) / character.max_hp),
                    10,
                ),
            )
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
        self, spritesheet, base_sprite, position, face_right, max_hp, strength, scale=1
    ):
        pg.sprite.Sprite.__init__(self)

        self.base_sprite = base_sprite
        self.spritesheet = spritesheet
        self.face_right = face_right
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength

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

    def is_dead(self):
        return self.hp <= 0


if __name__ == "__main__":
    main()
