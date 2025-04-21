import random
from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    WEAPON = 1
    SHIRT = 2
    HAT = 3
    BOOTS = 4
    POTION = 5


class Quality(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4


drop_rates = {
    "COMMON": 65,
    "UNCOMMON": 20,
    "RARE": 10,
    "EPIC": 5,
}
prices = {
    "COMMON": 2,
    "UNCOMMON": 10,
    "RARE": 30,
    "EPIC": 100,
}
character_infos = {
    "ARCHER": {"name": "Archer", "sprite": (0, 3), "vitality": 150, "strength": 20},
    "PIG": {"name": "Archer", "sprite": (0, 0), "vitality": 50, "strength": 2},
    "WASP": {"name": "Wasp", "sprite": (4, 0), "vitality": 60, "strength": 5},
    "GHOST": {"name": "Ghost", "sprite": (4, 3), "vitality": 100, "strength": 10},
}
item_infos = {
    "HEALTH_POTION": {
        "name": "Health potion",
        "sprite": (11, 3),
        "item_type": ItemType.POTION,
        "health_bonus": 50,
        "quality": Quality.COMMON,
    },
    "COMMON_SWORD": {
        "name": "Common sword",
        "sprite": (11, 9),
        "item_type": ItemType.WEAPON,
        "strength": 4,
        "vitality": 0,
        "quality": Quality.COMMON,
    },
    "UNCOMMON_SWORD": {
        "name": "Uncommon sword",
        "sprite": (11, 10),
        "item_type": ItemType.WEAPON,
        "strength": 10,
        "vitality": 0,
        "quality": Quality.UNCOMMON,
    },
    "RARE_SWORD": {
        "name": "Rare sword",
        "sprite": (11, 11),
        "item_type": ItemType.WEAPON,
        "strength": 20,
        "vitality": 0,
        "quality": Quality.RARE,
    },
    "EPIC_SWORD": {
        "name": "Epic sword",
        "sprite": (11, 12),
        "item_type": ItemType.WEAPON,
        "strength": 50,
        "vitality": 0,
        "quality": Quality.EPIC,
    },
    "COMMON_SHIRT": {
        "name": "Common shirt",
        "sprite": (10, 5),
        "item_type": ItemType.SHIRT,
        "strength": 0,
        "vitality": 5,
        "quality": Quality.COMMON,
    },
    "UNCOMMON_SHIRT": {
        "name": "Uncommon shirt",
        "sprite": (10, 6),
        "item_type": ItemType.SHIRT,
        "strength": 0,
        "vitality": 15,
        "quality": Quality.UNCOMMON,
    },
    "RARE_SHIRT": {
        "name": "Rare shirt",
        "sprite": (10, 7),
        "item_type": ItemType.SHIRT,
        "strength": 0,
        "vitality": 30,
        "quality": Quality.RARE,
    },
    "EPIC_SHIRT": {
        "name": "Epic shirt",
        "sprite": (10, 8),
        "item_type": ItemType.SHIRT,
        "strength": 0,
        "vitality": 100,
        "quality": Quality.EPIC,
    },
    "COMMON_HAT": {
        "name": "Common hat",
        "sprite": (10, 9),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 2,
        "quality": Quality.COMMON,
    },
    "UNCOMMON_HAT": {
        "name": "Uncommon hat",
        "sprite": (10, 10),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 10,
        "quality": Quality.UNCOMMON,
    },
    "RARE_HAT": {
        "name": "Rare hat",
        "sprite": (10, 11),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 20,
        "quality": Quality.RARE,
    },
    "EPIC_HAT": {
        "name": "Epic hat",
        "sprite": (10, 12),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 60,
        "quality": Quality.EPIC,
    },
    "COMMON_BOOTS": {
        "name": "Common boots",
        "sprite": (11, 5),
        "item_type": ItemType.BOOTS,
        "strength": 0,
        "vitality": 1,
        "quality": Quality.COMMON,
    },
    "UNCOMMON_BOOTS": {
        "name": "Uncommon boots",
        "sprite": (11, 6),
        "item_type": ItemType.BOOTS,
        "strength": 0,
        "vitality": 5,
        "quality": Quality.UNCOMMON,
    },
    "RARE_BOOTS": {
        "name": "Rare boots",
        "sprite": (11, 7),
        "item_type": ItemType.BOOTS,
        "strength": 0,
        "vitality": 10,
        "quality": Quality.RARE,
    },
    "EPIC_BOOTS": {
        "name": "Epic boots",
        "sprite": (11, 8),
        "item_type": ItemType.BOOTS,
        "strength": 0,
        "vitality": 40,
        "quality": Quality.EPIC,
    },
}


@dataclass
class CharacterInfo:
    name: str
    sprite: tuple
    vitality: int
    strength: int


@dataclass
class ItemInfo:
    name: str
    sprite: tuple
    item_type: ItemType
    quality: Quality
    vitality: int | None = None
    strength: int | None = None
    health_bonus: int | None = None


def get_item_info(identifier):
    info = item_infos[identifier]
    if info["item_type"] == ItemType.POTION:
        return ItemInfo(
            name=info["name"],
            sprite=info["sprite"],
            item_type=info["item_type"],
            quality=info["quality"],
            health_bonus=info["health_bonus"],
        )
    return ItemInfo(
        name=info["name"],
        sprite=info["sprite"],
        item_type=info["item_type"],
        quality=info["quality"],
        strength=info["strength"],
        vitality=info["vitality"],
    )


def get_character_info(identifier):
    info = character_infos[identifier]
    return CharacterInfo(
        name=info["name"],
        sprite=info["sprite"],
        strength=info["strength"],
        vitality=info["vitality"],
    )


def get_random_item_identifier_by_quality(quality):
    identifiers = []
    for key, value in item_infos.items():
        if value["quality"] == quality:
            identifiers.append(key)
    if identifiers:
        return random.choice(identifiers)
    return None


def get_drop_rate_by_quality(quality):
    for key, value in drop_rates.items():
        if key == quality.name:
            return value
    return None


def get_price_by_quality(quality):
    for key, value in prices.items():
        if key == quality.name:
            return value
    return None
