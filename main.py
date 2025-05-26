import sys
import color
from Item import Item, Recipe
from Characters import Player
import time

class Main:

    #-------------------------------------------------------------------------------------------------------------------
    # This class contains the main game and the menus.
    # Currently, there are also some crafting recipes in here.
    # Crafting isn't properly implemented as of now.
    #-------------------------------------------------------------------------------------------------------------------


    #-------------------------------------------------------------------------------------------------------------------
    # Menu methods
    #-------------------------------------------------------------------------------------------------------------------

    # Main menu: This is where the game starts. You basically only navigate though menus and call (mainly player class)
    # methods for different actions. Once you are done you will always return to the main menu.

    @staticmethod
    def main_menu():
        player.display_status()
        print(f"\nWhat do you want to do, {player.name}?\n")
        time.sleep(1)
        print(f"  0: {player.name}")
        time.sleep(0.1)
        print(f"  1: gather wood")
        time.sleep(0.1)
        print(f"  2: forage")
        time.sleep(0.1)
        print(f"  3: hunt")
        time.sleep(0.1)
        print(f"  4: craft")
        time.sleep(0.1)
        print(f"  5: rest")
        time.sleep(0.1)
        print(f"  6: sleep")
        time.sleep(0.1)
        print(f"  7: explore")
        time.sleep(0.1)
        print(f" 10: info")
        time.sleep(0.1)
        print(f" 23: {color.red("Exit")}")
        time.sleep(0.1)
        next_action = 0
        try:
            next_action = int(input(" "))
        except ValueError:
            print(color.red("*** You feel confused..."))
            Main.main_menu()
        print()
        if next_action == 0:
            Main.player_menu()
        elif next_action == 1:
            player.gather_wood()
        elif next_action == 2:
            player.forage()
        elif next_action == 3:
            player.hunt()
        elif next_action == 4:
            player.craft_item()
        elif next_action == 5:
            player.rest()
        elif next_action == 6:
            player.sleep()
        elif next_action == 7:
            player.explore()

        elif next_action == 10:
            Main.display_info()

        elif next_action == 23:
            if int(input("Are you sure? 0: No / 1: Yes\n")):
                sys.exit()

        Main.main_menu()

    # Player menu: This is where you get all infos about your player like your inventories or your coordinates.

    @staticmethod
    def player_menu():
        print(f"\nWhat do you want to do, {player.name}?\n")
        next_action = 0
        try:
            # This is the actual player_menu being displayed, making the player choose an option at the same time.
            next_action = int(input(f"  0: return \n  1: show inventory \n  2: show tools \n  3: show coordinates \n  4: {color.red("show map")} \n  5: rename \n "))
        except ValueError:
            print(color.red("*** You feel confused..."))
            Main.player_menu()
        print()
        if next_action == 0:
            Main.main_menu()
        elif next_action == 1:
            player.show_inventory()
        elif next_action == 2:
            player.show_tools()
        elif next_action == 3:
            player.position.display_coordinates()
        elif next_action == 4:
            print(color.red("*** Not yet available!"))
        elif next_action == 5:
            player.name = color.yellow(color.yellow(input("\tEnter your new name:\n\t")))
        Main.player_menu()

    # Info menu: This where you get all your information about game mechanics.

    @staticmethod
    def display_info():
        print(f"\nWhat do you want to know about, {player.name}?\n")
        next_action = 0
        try:
            # This is the actual info_menu being displayed, making the player choose an option at the same time.
            next_action = int(input(f"  0: return \n  1: gather wood \n  2: forage \n  3: hunt \n  4: craft \n  5: rest \n  6: sleep \n  7: explore \n  9: random attacks \n 10: actions \n "))
        except ValueError:
            print(color.red("*** You feel confused..."))
            Main.display_info()
        print()
        if next_action == 0:
            Main.main_menu()
        elif next_action == 1:
            print("*** Gathering wood:")
            print(f"\t{color.green("Stamina")} use: 1")
            print(f"\t{color.red("Danger level")}: 3")
            print(f"\tYou have a chance to find 0 to 1 {color.blue("wood")} per hour.")
            print()
        elif next_action == 2:
            print("*** Foraging:")
            print(f"\t{color.green("Stamina")} use: 1")
            print(f"\t{color.red("Danger level")}: 3")
            print(f"\tYou have a chance to find 0 to 1 {color.blue("food")} per hour.")
            print(f"\tIn the future you will have a chance to find {color.blue("special items")} while foraging.")
            print()
        elif next_action == 3:
            print("*** Hunting:")
            print(f"\tHunting requires a {color.blue("bow")}!")
            print(f"\t{color.green("Stamina")} use: 2")
            print(f"\t{color.red("Danger level")}: 4")
            print(f"\tIn addition to {color.blue("food")} you have a chance to collect {color.blue("hide")} while hunting.")
            print(f"\tYou have a chance to find 0 to 5 {color.blue("food")} and 0 to 2 {color.blue("hide")} per hour.")
            print(f"\tEvery time you set out to hunt your success will be determined.")
            print(f"\tHigher success yields potentially more {color.blue("resources")} and even guarantees drops on higher levels.")
            print()
        elif next_action == 4:
            Main.main_menu()
        elif next_action == 5:
            Main.main_menu()
        elif next_action == 6:
            Main.main_menu()
        elif next_action == 7:
            Main.main_menu()
        elif next_action == 9:
            print("*** Random attacks:")
            print(f"\tRandom attacks may occur during actions.")
            print(f"\tOnce you get attacked there is (currently) nothing you can do but hope.")
            print(f"\tWhen encountering an enemy you will automatically try to dodge.")
            print(f"\tDodging costs 3 {color.green("Stamina")}.")
            print(f"\tIf you have enough stamina, you have a 3 in 4 chance to dodge.")
            print(f"\tIf not you will still attempt to dodge and take 1 {color.red("damage")} for the lack of {color.green("Stamina")}.")
            print(f"\tWhile out of stamina, your chance to dodge is only 1 in 4.")
            print()

        elif next_action == 10:
            print("*** Actions:")
            print(f"\tEvery action has a {color.green("Stamina")} requirement.")
            print(f"\tPerforming an action for one hour reduces your {color.green("Stamina")} by that amount.")
            print(f"\tIf you collect resources you will receive a randomized amount of the respective {color.blue("item/s")}.")
            print(f"\tPerforming actions in the wilderness is {color.red("dangerous")} though!")
            print(f"\tEvery hour you perform an action there is a chance of being attacked by a random enemy.")
            print(f"\tThe chance and severity of the attack depends on the actions {color.red("Danger level")}")
            print()
            print(f"\tAlways keep an eye on your {color.red("health")} and {color.green("Stamina")} stats!")
            print(f"\tIf your {color.red("health")} and/or {color.green("Stamina")} gets low you should consider aborting and returning home.")
            print()
        Main.display_info()

    # This method shows the intro screen
    @staticmethod
    def display_intro():
        #print(f"\n\n\t\t*** {color.red("WELCOME TO {color.yellow("TANKRED'S {color.green("ADVENTURE {color.blue("GAME")} ***\n\n")
        print("\n\n\t\t*", end='')
        time.sleep(0.3)
        print("*", end='')
        time.sleep(0.3)
        print("*", end='')
        time.sleep(0.3)
        print(f" {color.RED}WELCOME ", end='')
        time.sleep(0.7)
        print("TO ", end='')
        time.sleep(0.7)
        print(f"{color.YELLOW}TANKRED'S ", end='')
        time.sleep(0.7)
        print(f"{color.GREEN}ADVENTURE ", end='')
        time.sleep(0.7)
        print(f"{color.BLUE}GAME{color.END} ", end='')
        time.sleep(0.7)
        print("*", end='')
        time.sleep(0.3)
        print("*", end='')
        time.sleep(0.3)
        print("*")
        time.sleep(2)
        print(f"\n\t\t\tby {color.yellow("Kroschkolow")}\n\n")
        time.sleep(3)

    # This method:
    # - creates the player
    # - fills their inventory with starting food
    # - adds crafting recipes (Crafting is incomplete as of now).
    @staticmethod
    def create_player():
        player = Player(input(f"What is your {color.yellow("name")}?\n"), 10, 10)
        player.add_item(Item('food', 3))
        player.recipes.add(Recipe('bow', [Item('wood', 5), Item('paracord', 1)]))
        player.recipes.add(Recipe('tent', [Item('wood', 20), Item('hide', 10)]))
        player.recipes.add(Recipe('backpack', [Item('hide', 20)]))
        return player

# This is where the game starts
# Currently there is no way to win / reach win = true.
# The only way to end the game is dying or ending it through the main menu.
win = False
Main.display_intro()
player = Main.create_player()
while not win:
    Main.main_menu()