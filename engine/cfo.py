
# INFO
# This library contains the classes and the relative
# methods that will be used in the main code and in game library

# ANCHOR Character class
class Character:

    def __init__(self):
        self.name = ""  # Name of the character
        self.weapons = []
        self.max_ep = 100  # Energy points
        self.max_hp = 100  # Max health points
        self.protection = 0  # Protection points
        self.equipment = {
            "head": None,
            "arms": None,
            "body": None,
            "legs": None,
            "feet": None,
            "weapon_dx": None,
            "weapon_sx": None
        }


# ANCHOR Weapon code class
class WeaponCode:

    def __init__(self):
        self.name = ""  # Name of the weapon
        self.invocation = ""  # Invocation of the weapon
        # True if the weapon is offensive, False if it's defensive or tool
        self.is_offensive = None
        self.is_tool = None  # True if the weapon is a tool
        # If the weapon is a tool, the following attributes are not needed
        self.damage = 0  # Damage of the weapon
        self.accuracy = 0  # Accuracy of the weapon
        self.range = 0  # Range of the weapon
        self.is_ranged = None  # True if the weapon is ranged, False if it's melee
        # Number of ammo rounds (if the weapon is ranged or use energy); -1 means infinite
        self.rounds_max = 0
        self.rounds = 0  # Actual rounds loaded
        self.rounds_per_shoot = 0  # Number of ammo used when shooting
        # The following attributes are generic
        self.resistance = 100  # Resistance of the weapon, -1 means infinite
        self.speed = 0  # Speed of the weapon


# ANCHOR Player class
class Player:

    def __init__(self):
        self.username = ""  # Username
        self.score = 0  # Score of the player
        # NOTE Character prototype
        # [character_object, expiration_time]
        self.characters = []  # List of characters owned by the player
        self.is_banned = False  # True if the player is banned
        self.is_in_match = False  # True if the player is in a match
        self.last_match = 0  # ID of the last match played or playing

