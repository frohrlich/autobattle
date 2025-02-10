from enum import Enum


class ItemType(Enum):
    WEAPON = 1


character_infos = {
    "ARCHER": {"name": "Archer", "sprite": (0, 3), "hp": 100, "strength": 1},
    "PIG": {"name": "Archer", "sprite": (0, 0), "hp": 100, "strength": 5},
    "WASP": {"name": "Wasp", "sprite": (4, 0), "hp": 125, "strength": 10},
    "GHOST": {"name": "Ghost", "sprite": (4, 3), "hp": 150, "strength": 15},
}
item_infos = {
    "TRIDENT": {
        "name": "Trident",
        "sprite": (8, 9),
        "item_type": ItemType.WEAPON,
        "strength": 10,
        "hp": 0,
    },
    "ANVIL": {
        "name": "Anvil",
        "sprite": (9, 10),
        "item_type": ItemType.WEAPON,
        "strength": 40,
        "hp": 0,
    },
}
