import pygame as pg


class Character(pg.sprite.Sprite):
    """Represents a character in battle."""

    animation_speed = 5
    scale = 5

    def __init__(
        self,
        spritesheet,
        base_sprite,
        position,
        is_ally,
        base_hp,
        base_strength,
    ):
        pg.sprite.Sprite.__init__(self)
        self.base_sprite = base_sprite
        self.spritesheet = spritesheet
        self.is_ally = is_ally
        self.max_hp = base_hp
        self.hp = base_hp
        self.strength = base_strength

        # which sprite to use depending on character facing right or left
        # (allies face right and enemies face left)
        if is_ally:
            use_sprite = (base_sprite[0] + 1, base_sprite[1])
        else:
            use_sprite = (base_sprite[0] + 2, base_sprite[1])

        image_still, rect = spritesheet.image_at_index(use_sprite, colorkey=-1)
        image_moving, _ = spritesheet.image_at_index(
            (use_sprite[0], use_sprite[1] + 1), colorkey=-1
        )

        size = image_still.get_size()
        size = (size[0] * self.scale, size[1] * self.scale)
        self.image_still = pg.transform.scale(image_still, size)
        self.image_moving = pg.transform.scale(image_moving, size)

        self.image, self.rect = self.image_still, self.image_still.get_rect()
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
        """Make character move towards enemy and then return to original position."""
        direction = 1 if self.is_ally else -1

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
            self.image = self.image_moving
            self.rect.centerx += direction * self.animation_speed
        # when reaching limit, start returning to initial position
        else:
            self.image = self.image_still
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

    def add_item(self, item):
        self.max_hp += item.vitality
        self.hp += item.vitality
        self.strength += item.strength

    def remove_item(self, item):
        self.max_hp -= item.vitality
        self.hp -= item.vitality
        self.strength -= item.strength
