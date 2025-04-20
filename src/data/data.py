from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    WEAPON = 1
    SHIRT = 2
    HAT = 3
    BOOTS = 4


character_infos = {
    "ARCHER": {"name": "Archer", "sprite": (0, 3), "vitality": 100, "strength": 10},
    "PIG": {"name": "Archer", "sprite": (0, 0), "vitality": 100, "strength": 5},
    "WASP": {"name": "Wasp", "sprite": (4, 0), "vitality": 125, "strength": 10},
    "GHOST": {"name": "Ghost", "sprite": (4, 3), "vitality": 150, "strength": 15},
}
item_infos = {
    "BASIC_SWORD": {
        "name": "Basic sword",
        "sprite": (11, 8),
        "item_type": ItemType.WEAPON,
        "strength": 10,
        "vitality": 0,
    },
    "RARE_SWORD": {
        "name": "Rare sword",
        "sprite": (11, 9),
        "item_type": ItemType.WEAPON,
        "strength": 20,
        "vitality": 0,
    },
    "EPIC_SWORD": {
        "name": "Epic sword",
        "sprite": (11, 10),
        "item_type": ItemType.WEAPON,
        "strength": 50,
        "vitality": 0,
    },
    "BASIC_SHIRT": {
        "name": "Basic shirt",
        "sprite": (10, 5),
        "item_type": ItemType.SHIRT,
        "strength": 0,
        "vitality": 15,
    },
    "RARE_SHIRT": {
        "name": "Rare shirt",
        "sprite": (10, 6),
        "item_type": ItemType.SHIRT,
        "strength": 0,
        "vitality": 30,
    },
    "EPIC_SHIRT": {
        "name": "Epic shirt",
        "sprite": (10, 7),
        "item_type": ItemType.SHIRT,
        "strength": 0,
        "vitality": 100,
    },
    "BASIC_HAT": {
        "name": "Basic hat",
        "sprite": (10, 8),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 10,
    },
    "RARE_HAT": {
        "name": "Rare hat",
        "sprite": (10, 9),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 20,
    },
    "EPIC_HAT": {
        "name": "Epic hat",
        "sprite": (10, 10),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 60,
    },
    "BASIC_BOOTS": {
        "name": "Basic boots",
        "sprite": (11, 5),
        "item_type": ItemType.BOOTS,
        "strength": 0,
        "vitality": 5,
    },
    "RARE_BOOTS": {
        "name": "Rare boots",
        "sprite": (11, 6),
        "item_type": ItemType.BOOTS,
        "strength": 0,
        "vitality": 10,
    },
    "EPIC_BOOTS": {
        "name": "Basic boots",
        "sprite": (11, 7),
        "item_type": ItemType.BOOTS,
        "strength": 0,
        "vitality": 40,
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
    vitality: int
    strength: int


def get_item_info(identifier):
    info = item_infos[identifier]
    return ItemInfo(
        name=info["name"],
        sprite=info["sprite"],
        item_type=info["item_type"],
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
