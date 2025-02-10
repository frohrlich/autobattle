import pygame as pg

colorkey = (255, 0, 220)


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
        self._strength = base_strength

        # which sprite to use depending on character facing right or left
        # (allies face right and enemies face left)
        if is_ally:
            use_sprite = (base_sprite[0] + 1, base_sprite[1])
        else:
            use_sprite = (base_sprite[0] + 2, base_sprite[1])

        image, rect = spritesheet.image_at_index(use_sprite, colorkey)

        size = image.get_size()
        size = (size[0] * self.scale, size[1] * self.scale)
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
        is_ally,
        base_hp,
        base_strength,
        inventory,
    ):
        Character.__init__(
            self,
            spritesheet,
            base_sprite,
            position,
            is_ally,
            base_hp,
            base_strength,
        )
        self.inventory = inventory

        self.max_hp = self.max_hp + sum(item.hp for item in self.get_items())
        self.hp = self.max_hp

    @property
    def strength(self):
        return self._strength + sum(item.strength for item in self.get_items())

    def get_items(self):
        return (slot.item for slot in self.inventory.slots if slot.item is not None)
