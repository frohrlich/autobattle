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

    player = Character(spritesheet, (0, 3), player_pos, True, 10)
    enemy = Character(spritesheet, (0, 0), enemy_pos, False, 10)
    character_list = (player, enemy)
    battle = Battle(character_list)

    character_group = pg.sprite.RenderPlain(character_list)

    clock = pg.time.Clock()

    going = True
    while going:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                battle.next_turn()

        character_group.update()

        screen.blit(background, (0, 0))
        character_group.draw(screen)
        pg.display.flip()

    pg.quit()


# def load_image(name, colorkey=None, scale=1):
#     fullname = os.path.join(data_dir, name)
#     image = pg.image.load(fullname)

#     size = image.get_size()
#     size = (size[0] * scale, size[1] * scale)
#     image = pg.transform.scale(image, size)

#     image = image.convert()
#     if colorkey is not None:
#         if colorkey == -1:
#             colorkey = image.get_at((0, 0))
#         image.set_colorkey(colorkey, pg.RLEACCEL)
#     return image, image.get_rect()


class Battle:
    def __init__(self, characters):
        self.characters = characters
        self.turn = 0

    def next_turn(self):
        index = self.turn % len(self.characters)
        current_character = self.characters[index]
        current_character.attack()

        self.turn += 1


class Character(pg.sprite.Sprite):
    """represents a character in battle"""

    animation_speed = 5

    def __init__(self, spritesheet, base_sprite, position, face_right, scale=1):
        pg.sprite.Sprite.__init__(self)
        self.base_sprite = base_sprite
        self.spritesheet = spritesheet
        self.face_right = face_right

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

    def attack(self):
        self.attacking = True

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


if __name__ == "__main__":
    main()
