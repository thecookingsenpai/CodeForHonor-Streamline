import os
import pickle
import gamelib

# SECTION Debug methods

# SECTION Players selection menu
def player_menu(players):
    valid = False
    while not valid:
        print("\n")
        counter = 0
        chosable = []
        for player in players:
            counter += 1
            print(str(counter) + ": " + players.get(player).username)
            chosable.append(players.get(player))
        print("\n")
        choice = input("Please select a player: ")
        # NOTE Sanity check
        if choice.isdigit():
            choice = int(choice)
            if choice <= len(players):
                current = chosable[choice - 1]
                valid = True
            else:
                print("Invalid choice!")
        else:
            print("Invalid choice!")
    print("\nYou are playing as " + current.username)
    return current
# !SECTION Players selection menu

# SECTION Character display list
def display_characters(current_player, to_choose=False):
    print("\nAvailable characters:")
    counter = 0
    for character in current_player.characters:
        counter += 1
        print(str(counter) + ": " + character.name)
    print("\n===============================================\n")
    if to_choose:
        valid = False
        while not valid:
            choice = input("Select a character: ")
            if choice.isdigit():
                if choice <= len(current_player.characters):
                    choice = int(choice)
                    valid = True
                else:
                    print("Invalid choice!")
            else:
                print("Invalid choice!")
        return current_player.characters[choice - 1]
# !SECTION Character display list

# !SECTION Debug methods

# SECTION Helper methods
def search_fight():
    # TODO network game search
    pass


def load_fight(match_id):
    fight = game.init_fight(match_id)
    # TODO
# !SECTION Helper methods

# SECTION Main routine

# ANCHOR Global variables
game = None

if __name__ == '__main__':
    game = gamelib.cfo.Game()
    # NOTE Creating a new player or loading an existing one
    if len(game.players) == 0:
        username = input("Chose an username: ")
        game.new_player(username)
        # NOTE Saving the players
        with open("players.pickle", "wb") as f:
            pickle.dump(game.players, f)

    # ANCHOR Debug CLI game instance
    # NOTE This is a debug CLI game instance
    # NOTE Presenting the user with the main menu
    print("Welcome to the CLI game instance")
    print("|===============================================|")
    print("|=============== Code Of Honor =================|")
    print("|===============   Streamline  =================|")
    print("|===============================================|")
    game.current_player = player_menu(game.players)
    display_characters(game.current_player)

    # SECTION Choice menu
    print("1) Load a character")
    print("2) Find a fight")
    print("3) Logout")
    print("4) Exit")
    valid = False
    # NOTE Choice loop
    while not exiting:
        exiting = True
        choice = input("-\nChoose what to do: ")
        if (choice == "1"):
            print("Loading a character")
            game.loaded_character = display_characters(
                game.current_player, True)
            exiting = False
        elif (choice == "2"):
            print("Finding a fight")
            # NOTE Start the server and look for avail
            #      servers abroad
            # TODO match_id determination
            fight = game.init_fight(0)
            game.start_socket()
            # NOTE Here starts the whole while loop managed by
            #      listen_to_socket()
            success, end_result, message = game.listen_to_socket()
            if success:
                if end_result:
                    print("You won the fight!")
                else:
                    print("You lost the fight!")
            else:
                print("ERROR: " + message)
            exiting = False
        elif (choice == "3"):
            print("Logging out")
            game.current_player = None
            player_menu(game.players)
            # Returning to the menu
            exiting = False
        elif (choice == "4"):
            print("Exiting")
            os._exit(0)
        else:
            print("Invalid choice!")
            exiting = False
    # !SECTION Choice menu
    
# !SECTION Main routine