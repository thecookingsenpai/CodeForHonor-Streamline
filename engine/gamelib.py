# INFO 
# This library defines the methods used to manage
# and work with game sessions and fights
import os
import sys
import json
import pickle
import time
import socket
import fcntl
import errno
from requests import get
import cfo

# ANCHOR Game class
class Game:

    def __init__(self):
        # NOTE Fight server status
        self.busy = False  # True if the player is in a fight
        self.connected_ip = None  # IP of the connected player
        self.connected_port = None  # Port of the connected player
        # NOTE Network communication variables
        self.socket = None
        self.ip = get('https://api.ipify.org').content.decode('utf8')
        self.port = 9999
        # NOTE Load the default values for new players and
        # ensure that the folders are created
        self.default_character = None
        self.loaded_characters = []  # List of loaded characters
        self.default_weapon = None
        self.loaded_weapons = []  # List of loaded weapons
        self.initialize()
        # NOTE Loads players if any or creates a new dictionary
        if os.path.exists("players.pickle"):
            with open("players.pickle", "rb") as f:
                self.players = pickle.load(f)
        else:
            self.players = {}
        # NOTE Current state
        self.current_player = None
        self.loaded_character = None
        # NOTE Match dictionary
        # {
        #    "match_id" {
        #       "players": [player1, player2],
        #       "characters": [character1, character2],
        #       "turn": 0, # 0 = player1, 1 = player2
        #       "round": 0,
        #       "winner": None
        #       "starting_time": starting_time,
        #       "ending_time": ending_time,
        #       "scores": [score1, score2]
        #    }
        # }
        self.matches = {}

    # ANCHOR First time initalization / loading of defaults
    # NOTE This method is called at every restart and creates or loads
    # the default starting values
    def initialize(self):
        # NOE IP and Port initialization
        self.ip = "127.0.0.1"
        self.port = 9999
        # NOTE Folders creation
        if not (os.path.exists("data")):
            os.mkdir("data")
        if not (os.path.exists("data/weapons")):
            os.mkdir("data/weapons")
        if not (os.path.exists("data/characters")):
            os.mkdir("data/characters")
        if not (os.path.exists("data/players")):
            os.mkdir("data/players")
        if not (os.path.exists("data/characters/default")):
            os.mkdir("data/characters/default")
        # NOTE Database of objects loading
        if not (os.path.exists("data/weapons/db.cfo")):
            with open("data/weapons/db.cfo", "wb") as f:
                pickle.dump([basic_weapon], f)
        else:
            with open("data/weapons/db.cfo", "rb") as f:
                self.loaded_weapons = pickle.load(f)
        if not (os.path.exists("data/characters/db.cfo")):
            with open("data/characters/db.cfo", "wb") as f:
                pickle.dump([basic_character], f)
        else:
            with open("data/characters/db.cfo", "rb") as f:
                self.loaded_characters = pickle.load(f)
        # NOTE Default weapon creation
        if not (os.path.exists("data/characters/default/weapon")):
            basic_weapon = cfo.WeaponCode()
            basic_weapon.name = "fist"
            basic_weapon.invocation = "punch(TARGET)"
            basic_weapon.is_offensive = True
            basic_weapon.is_tool = False
            basic_weapon.resistance = -1
            basic_weapon.damage = 1
            basic_weapon.accuracy = 50
            basic_weapon.is_ranged = False
            basic_weapon.rounds_max = -1
            basic_weapon.speed = 1
            with open("data/characters/default/weapon", "wb") as f:
                pickle.dump(basic_weapon, f)
        else:
            with open("data/characters/default/weapon", "rb") as f:
                basic_weapon = pickle.load(f)
        # NOTE Default character creation or loading
        if not (os.path.exists("data/characters/default/character.cfo")):
            basic_character = cfo.Character()
            basic_character.name = "Eddie"
            basic_character.weapons = [basic_weapon]
            basic_character.equipment["weapon_dx"] = basic_weapon
            with open("data/characters/default/character.cfo", "wb") as f:
                pickle.dump(basic_character, f)
        else:
            with open("data/characters/default/character.cfo", "rb") as f:
                basic_character = pickle.load(f)

        # NOTE Setting the default character and the default weapon
        self.default_character = basic_character
        self.default_weapon = basic_weapon

    # ANCHOR Player creation
    # NOTE A new player has the default character and the default weapon
    def new_player(self, username):
        player = cfo.Player()
        player.username = username
        player.score = 0
        player.characters = [self.default_character]
        player.is_banned = False
        self.players[username] = player

    # SECTION Utils
    def execute_function(self, method_name, *args):
        method = getattr(self, method_name)
        return method(*args)
    # !SECTION Utils

    # SECTION Fights
    def init_fight(self, match_id):
        # NOTE Environment
        self.fight_id = match_id
        # NOTE Match dictionary so we have both
        # players, both characters and their properties
        # NOTE Actions dictionary
        self.actions = {
            "punch": ["take_damage", 2],  # weapon, damage
            "shield": ["increase_protection", 2],  # tool, quantity
            "shoot": ["take_damage", 2],  # weapon, damage
            "reload": ["reload_weapon", 1],  # weapon
            "heal": ["increase_health", 2],  # tool, quantity
        }

    # SECTION Base events

    def take_damage(self, damage):
        # NOTE Calculate protection and damage
        protection = self.current_player.characters[self.loaded_character].protection
        real_damage = damage - (protection/10)
        self.current_player.characters[self.loaded_character].hp -= real_damage

    def cure(self, cure):
        self.current_player.characters[self.loaded_character].hp += cure

    def increase_protection(self, quantity):
        self.current_player.characters[self.loaded_character].protection += quantity

    def reload_weapon(self, weapon):
        max_load = self.current_player.characters[self.loaded_character].weapons[weapon].rounds_max
        # NOTE If the weapon is infinite, we don't reload
        if max_load == -1:
            return True
        # NOTE If the weapon is not infinite, we reload
        self.current_player.characters[self.loaded_character].weapons[weapon].rounds = max_load

    def increase_health(self, quantity):
        current_health = self.current_player.characters[self.loaded_character].hp
        new_health = current_health + quantity
        max_health = self.current_player.characters[self.loaded_character].max_hp
        # NOTE If the new health is higher than the max health, we set it to the max health
        if new_health > max_health:
            new_health = max_health
        self.current_player.characters[self.loaded_character].hp = new_health

    # !SECTION Base events

    # TODO Code sender and receiver
    def send_action(self, action):
        pass

    def reply_action(self, action):
        pass

    # NOTE The order of the actions is important
    # check the below example, receive_action takes
    # its parameter from listen_to_socket in main cycle
    def receive_action(self, action):
        # NOTE Dividing action
        # REVIEW Ensure that the action is valid
        is_valid = (
            action.endswith(")") and
            "(" in action and not
            action.startswith("(")
        )
        if not is_valid:
            return False
        # Actions are composed of a word and two round brackets
        action = action.split("(")[0]
        try:
            arguments = action.split("(")[1].split(")")[0].split(",")
            if len(arguments) == 0:
                raise Exception
        except:
            arguments = []
        # Normalizing arguments
        counter = 0
        for argument in arguments:
            argument = argument.strip()
            arguments[counter] = argument
        # REVIEW How actions work
        # Actions are evalued as:
        # dictionary.get(action)
        # has [0] = callback, [...]
        # callback will be then called with arguments
        # using call-string as a function
        # TODO To ensure integrity all the items are checked
        # against our database to get the correct item properties
        if not action in self.actions:
            return False
        result = self.execute_function(self.actions[action][0], *arguments)
        self.send_to_socket(result)

    # NOTE ip and port are specified in the messages sent
    def send_to_socket(self, data):
        if not self.connected_ip or not self.connected_port:
            return False, "No IP or port specified for the connected player"
        data = "[" + self.ip + ":" + self.port + "]> " + data
        sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendsocket.connect((self.connected_ip, self.connected_port))
        sendsocket.send(data.encode())

    # NOTE This method is called on streamline main file and manages
    #      the whole listen, action and repeat for the duration of
    #      the fight
    def listen_to_socket(self):
        while True:
            try:
                msg = self.socket.recv(4096)
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    time.sleep(1)
                    # Returns with no data
                    return False, ""
                else:
                    # a "real" error occurred
                    print(e)
                    sys.exit(1)
            else:
                decoded = msg.decode()
                # REVIEW Ensure we can receive one connection per time (same ip)
                # NOTE You can do this by locking the IP and refusing anything
                #      that is not from that IP
                #
                # NOTE Returning this method means the fight is over
                if not self.busy:
                    self.connected_ip = decoded.split(">")[0].split("[")[
                        1].split(":")[0]
                    self.connected_port = decoded.split(
                        ">")[0].split("[")[1].split(":")[1]
                    self.busy = True
                else:
                    if not self.connected_ip in decoded:
                        # Ignore the message if it's not from the connected player
                        continue
                # NOTE Decoding the message
                msg = decoded.split("> ")[1]
                # Basic actions
                # REVIEW Implement a method to disconnect clean and not clean to free the slot
                if msg == "disconnect":
                    self.busy = False
                    self.connected_ip = ""
                    self.connected_port = ""
                    # FIXME the second parameter is to be real
                    return True, 0, "Disconnected"
                # Execute complex actions
                self.receive_action(msg)

    def start_socket(self):
        # Non blocking socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ip, self.port)
        fcntl.fcntl(self.socket, fcntl.F_SETFL, os.O_NONBLOCK)
        self.listen_to_socket()

    # Example to run and listen in a main cycle
    #
    #   sock = self.start_socket()
    #   while True:
    #       is_data, data = self.listen_to_socket(sock)
    #       if is_data:
    #           self.receive_action(data)
    #       else:
    #           continue
    #
    #   # do game stuff

    # SECTION Utils
    def execute_function(self, method_name, *args):
        method = getattr(self, method_name)
        return method(*args)
    # !SECTION Utils

    # !SECTION Fights