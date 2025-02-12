from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    WEAPON = 1
    CAPE = 2
    HAT = 3
    BOOTS = 4


character_infos = {
    "ARCHER": {"name": "Archer", "sprite": (0, 3), "vitality": 100, "strength": 10},
    "PIG": {"name": "Archer", "sprite": (0, 0), "vitality": 100, "strength": 5},
    "WASP": {"name": "Wasp", "sprite": (4, 0), "vitality": 125, "strength": 10},
    "GHOST": {"name": "Ghost", "sprite": (4, 3), "vitality": 150, "strength": 15},
}
item_infos = {
    "TRIDENT": {
        "name": "Trident",
        "sprite": (8, 9),
        "item_type": ItemType.WEAPON,
        "strength": 10,
        "vitality": 0,
    },
    "ANVIL": {
        "name": "Anvil",
        "sprite": (9, 10),
        "item_type": ItemType.WEAPON,
        "strength": 40,
        "vitality": 0,
    },
    "NET_CAPE": {
        "name": "Net cape",
        "sprite": (8, 8),
        "item_type": ItemType.CAPE,
        "strength": 0,
        "vitality": 1000,
    },
    "SPACE_HELMET": {
        "name": "Space helmet",
        "sprite": (8, 10),
        "item_type": ItemType.HAT,
        "strength": 0,
        "vitality": 50,
    },
    "BEE_BOOTS": {
        "name": "Bee boots",
        "sprite": (8, 6),
        "item_type": ItemType.BOOTS,
        "strength": 50,
        "vitality": 1000,
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
