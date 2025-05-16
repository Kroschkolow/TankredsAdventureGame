from status import Status
from inventory import Inventory
from map import Map
import color
import sys
import random
from world import World
from item import Item, Recipe

#-------------------------------------------------------------------------------------------------------------------
# This class contains the character parent class and all different child classes like the player, enemies and NPC.
#-------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------
# This is the character parent class.
#-------------------------------------------------------------------------------------------------------------------

class Character:

    def __init__(self, name, hp, stamina):
        self.name = name
        self.status = Status(hp, stamina)
        self.inventory = Inventory()

    def display_status(self):
        print(f"\n{self.name}\t\t{self.status.display()}")

    # This is currently unused, as the player class has its own implementation and enemies and NPCs don't use stamina
    # as of now. Will probably be needed once more complex combat will be implemented.

    def action(self, amount):
        self.status.use_stamina(amount)
        if self.status.stamina > 0:
            return True
        else:
            self.take_damage(1)
            return False

    def take_damage(self, amount):
        self.status.reduce_hp(amount)
        if self.status.health <= 0:
            self.status.health = 0

    def heal(self, amount):
        self.status.heal_hp(amount)

    def show_inventory(self):
        print(f"\n*** {self.name}'s inventory:\n")
        self.inventory.print_inventory()
        print()

    def add_item(self, item):
        self.inventory.add(item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def swap_item(self, self_item, other_item):
        self.remove_item(self_item)
        self.add_item(other_item)

#-----------------------------------------------------------------------------------------------------------------------
# This is the player class, where most of the actions happen.
#-----------------------------------------------------------------------------------------------------------------------

class Player(Character):

    def __init__(self, name, hp, stamina):
        super().__init__(name, hp, stamina)
        self.name = color.YELLOW + name + color.END
        self.recipes = Inventory()
        self.tools = Inventory()
        self.position = Map(0, 0)
        self.map = []
        self.map.append(self.position)

    # This method gets called a lot to give players a better overview of their current stats and world time, so they can
    # make informed decisions about how to continue.

    def display_status(self):
        return(f"\n{self.name}\t\t{self.status.display()}\n{World.display_time()}")

    # This method gets called during every action.
    # - it passes world time
    # - it manages player food intake
    # - it decides if the player gets attacked during actions.
    # - it ends the game once they players health reaches zero.

    def update(self, danger_level):
        # passing time
        World.pass_time()
        # managing food intake
        if World.time == 8:
            self.eat()
        elif World.time == 14:
            self.eat()
        elif World.time == 20:
            self.eat()
        # deciding on attacks, creating enemy objects and calling their attack method
        possibility = World.random_attack(danger_level)
        if possibility > 6:
            enemy = Enemy(10, 20, danger_level)
            enemy.attack()
            self.dodge(enemy.adjective, enemy.name, enemy.damage)
        # killing the player if "necessary"
        if self.status.health <= 0:
            Player.you_died()

    # This method lets the player decide if they want to either go through with the chosen action or continue with what
    # they are doing currently.
    # This method also calls the update method above.

    def go_on(self, danger_level):
        print(f"\t{self.display_status()}\n")
        decision = 0
        try:
            decision = bool(int(input("*** Do you want to continue?\n\t 0: No / 1: Yes\n\t ")))
        except ValueError:
            input(f"{color.RED}*** You feel confused and decide to stop.{color.END}")
            return False
        print()
        if decision:
            self.update(danger_level)
            return decision
        else:
            return decision

    # This method gets called by the update method.
    # - it checks if the player has food in their inventory
    # - if true it will delete one unit
    # - if false damages the player

    def eat(self):
        food = Item('food', 1)
        if self.inventory.item_check(food):
            self.remove_item(food)
            print(f"\tNomNomNom!\tYou consumed {food.quantity} {food.name}\n")
        else:
            self.take_damage(1)
            print(f"\tYou take {color.RED}1 damage!{color.END}")

    # Dark Souls inspired death screen
    # This method gets called by the update method once the players health reaches zero and ends the game.

    @staticmethod
    def you_died():
        print()
        print(color.RED + "*** YOU DIED! ***")
        print("\tGET GUD!" + color.END)
        print()
        input()
        sys.exit()


    # ------------------------------------------------------------------------------------------------------------------
    # Basic actions
    #-------------------------------------------------------------------------------------------------------------------

    # This method reduces player stamina according to their actions stamina demand.
    # It is the only method in this section that doesn't get called directly by the player.
    # It doesn't hinder the player from commiting to actions.
    # It damages the player if they lack the necessary stamina and makes sure it doesn't fall below zero.

    def action(self, amount):
        if self.status.stamina - amount < 0:
            print(f"\tYou don't have enough {color.GREEN}stamina{color.END}. You take {color.RED}1 damage{color.END}!\n")
            self.status.stamina = 0
            self.take_damage(1)
            return False
        else:
            self.status.use_stamina(amount)
            return True


    # Resting restores stamina
    # DevNote: fix display formatting

    def rest(self):
        DANGER_LEVEL = 1
        print("\n*** You sit down to rest a while...")
        while self.go_on(DANGER_LEVEL) and World.check_time():
            self.status.recover_stamina(2)
            if self.status.stamina < 9:
                print(f"\tYou recovered {color.GREEN}2 stamina{color.END}")
            elif self.status.stamina == 9:
                print(f"\tYou recovered {color.GREEN}1 stamina{color.END}")
            else:
                options = ['the sounds of nature', 'the fresh air', 'the sunlight', 'watching the clouds', 'observing the animals']
                print(f"\tYou are well rested and enjoy {random.choice(options)}...")

    # Sleeping is currently the only way to restore health, restoring 1 HP per hour.
    # Sleeping also restores 2 stamina per hour.
    # The player can only go to sleep after 22 o'clock and always sleeps for 8 hours.

    def sleep(self):
        DANGER_LEVEL = 2
        if World.time < 22 and World.time > 4:
            print(f"*** {World.time} o'clock is too early to sleep!\n")
            return
        else:
            print("*** You are laying down to sleep...\n")
            for i in range(0, 8):
                print("\tZzZzz! ZzZzz!")
                if self.status.health < 9:
                    self.heal(1)
                    print(f"\tYour wounds healed!\t{color.RED}Health: {self.status.health}{color.END}")
                elif self.status.health == 9:
                    self.heal(1)
                    print(f"\tYour wounds healed completely!\t{color.RED}Health: {self.status.health}{color.END}")
                self.status.recover_stamina(2)
                World.pass_time()
                input("\t")

            adjectives = ['singing', 'howling', 'chewing', 'dancing', 'fornicating', 'snoring', 'crying', 'defecating', 'puking', 'falling', 'arguing']
            names = ['birds', 'deer', 'bears', 'dogs', 'cats', 'mice', 'children', 'politicians', 'wolfs', 'foxes', 'witches']
            print(f"*** You awake to the sound of {random.choice(adjectives)} {random.choice(names)}...")


    #-------------------------------------------------------------------------------------------------------------------
    # Inventory methods
    #-------------------------------------------------------------------------------------------------------------------

    def show_tools(self):
        print(f"\n*** {self.name}'s tools:\n")
        self.tools.print_inventory()

    # This method lets the player trade items with NPCs
    # Currently NPCs will always agree to the trade.
    # As soon as the value system is implemented there will be a check if the player offers enough value in items for
    # the trade to go through. Otherwise, it will be denied.

    def trade(self, other):
        print(f"\n*** You want to trade with {other.name}...")
        other.show_inventory()
        # Creating a new item object from player input to receive from the merchant.
        other_item = Item(input("\tWhich item do you want to trade for?\n\t"), int(input("\tHow many do you want?\n\t")))
        self.show_inventory()
        # Creating a new item object from player input to trade in.
        self_item = Item(input("\tWhich item do you want to trade in?\n\t"), int(input("\tHow many do you want to trade in?\n\t")))
        # Displaying the trade.
        print(f"\n*** {self.name} wants to trade {self_item.quantity} {self_item.name} for {other.name}'s {other_item.quantity} {other_item.name}")
        # Checking both inventories for available item amounts.
        if self.inventory.item_check(self_item) and other.inventory.item_check(other_item):
            # Actual item swap.
            self.swap_item(self_item, other_item)
            other.swap_item(other_item, self_item)
            print("\tTrade successful!")

    # Method for crafting items.
    # This system is currently incomplete.
    # It prints the crafting inventory.
    # It checks the player inventory for necessary items and:
    # - aborts if the player has insufficient amount of items.
    # - removes the required materials, creates a new item object and places it in the tools inventory.
    # different tools will be needed to unlock different actions in the future (e.g. needing a bow to hunt).

    def craft_item(self):
        DURATION = None
        DANGER_LEVEL = 1
        print("\n*** You are preparing to craft something...\n")
        self.recipes.print_inventory()
        decision = int(input("\n\tWhat do you want to craft?\n\t"))
        if decision >= len(self.recipes.items):
            return
        for item in self.recipes.items[decision].required_items:
            if not self.inventory.item_check(item):
                return
        for item in self.recipes.items[decision].required_items:
            self.inventory.remove(item)
        self.tools.add(Item(self.recipes.items[decision].name, 1))


    # ------------------------------------------------------------------------------------------------------------------
    # Actions yielding resources
    # Every action here follows the same pattern:
    # - creating the respective item objects for the player to add to their inventory if successful.
    # - checking if there is enough time in the day and asking if the player wants to go through with the action.
    # - passing time, passing required stamina to action method, passing danger_level to decide random attacks and their
    #   severity.
    # - adding a randomised amount to the respective item object.
    # - adding the item to the player inventory once the action is aborted.
    #-------------------------------------------------------------------------------------------------------------------

    def gather_wood(self):
        STAMINA_COST = 1
        DANGER_LEVEL = 3
        time_spend = 0
        wood_collected = Item('wood', 0)
        print("\n*** You are setting out to gather wood...")
        while World.check_time() and self.go_on(DANGER_LEVEL):
            time_spend += 1
            self.action(STAMINA_COST)
            wood_collected.quantity += random.randint(0,1)
            input(f"\tYou collected {wood_collected.quantity} {wood_collected.name} so far.")
        if (wood_collected.quantity > 0):
            self.add_item(wood_collected)
        input(f"\tYou collected {wood_collected.quantity} {wood_collected.name} in {time_spend} hours and return home.\n\t")


    def forage(self):
        STAMINA_COST = 1
        DANGER_LEVEL = 3
        time_spend = 0
        food_collected = Item('food', 0)
        print("\nYou are heading out to forage...")
        while World.check_time() and self.go_on(DANGER_LEVEL):
            time_spend += 1
            self.action(STAMINA_COST)
            food_collected.quantity += random.randint(0,1)
            input(f"\tYou collected {food_collected.quantity} {food_collected.name} so far.")
        if (food_collected.quantity > 0):
            self.add_item(food_collected)
        input(f"\tYou collected {food_collected.quantity} {food_collected.name} in {time_spend} hours and return home.\n\t")

    # The hunt method implements hunting success as this was part of the original assignment by my python teacher.
    # Hunting success decides the range of the randomized item amount the player receives every hour.
    # DevNote: This mechanic might get replaced by a luck attribute in a possible player stat system.

    def hunt(self):
        STAMINA_COST = 2
        DANGER_LEVEL = 4
        time_spend = 0
        food_collected = Item('food', 0)
        hide_collected = Item('hide', 0)
        hunting_success = random.randint(0, 9)
        print("\nYou are gearing up to hunt...")
        while World.check_time() and self.go_on(DANGER_LEVEL):
            time_spend += 1
            self.action(STAMINA_COST)
            if hunting_success < 3:
                food_collected.quantity += random.randint(0, 1)
            elif hunting_success < 8:
                food_collected.quantity += random.randint(1, 2)
                hide_collected.quantity += random.randint(0, 1)
            else:
                food_collected.quantity += random.randint(1, 3)
                hide_collected.quantity += random.randint(1, 2)
            input(f"\tYou collected {food_collected.quantity} {food_collected.name} and {hide_collected.quantity} {hide_collected.name} so far.")
        if (food_collected.quantity > 0):
            self.add_item(food_collected)
        if (hide_collected):
            self.add_item(hide_collected)
        input(f"\tYou collected {food_collected.quantity} {food_collected.name} and {hide_collected.quantity} {hide_collected.name} in {time_spend} hours and return home.\n\t")

    #-------------------------------------------------------------------------------------------------------------------
    # Exploration and map methods
    # Currently there is no need to go exploring as resources are not (yet) limited.
    # DevNote: Exploration might be the way to win the game in the future (e.g. finding signs leading to civilisation).
    #-------------------------------------------------------------------------------------------------------------------

    def explore(self):
        DANGER_LEVEL = 5
        DURATION = 3
        if World.check_time(DURATION):
            print("*** You are preparing to pack up and venture forth...\n")
            decision = 0
            # Unlike other methods, ValueErrors don't abort the action but chooses the direction for you. So do wrong numbers.
            try:
                decision = int(input("\tWhere do you want to go?\n\t 0: North\n\t 1: East\n\t 2: South\n\t 3: West\n\t "))
            except ValueError:
                print(f"{color.RED}*** You seem confused and wander off aimlessly...{color.END}")
                decision = random.randint(0, 3)
            new_position = None
            if decision < 0 or decision > 3:
                print(f"{color.RED}*** You wander off aimlessly...{color.END}")
                decision = random.randint(0, 3)

            # Creating a map object from the new coordinates.
            if decision == 0:
                new_position = Map(self.position.x + 1, self.position.y)
            elif decision == 1:
                new_position = Map(self.position.x, self.position.y + 1)
            elif decision == 2:
                new_position = Map(self.position.x - 1, self.position.y)
            elif decision == 3:
                new_position = Map(self.position.x, self.position.y - 1)
            # Checking new coordinates against previously explored locations.
            if self.map_explored(new_position):
                # Decision is inverted to keep decision input pattern consistent.
                if not int(input("\tYou have already been there.\n\tDo you want to return?\n\t 0: No / 1: Yes\n\t ")):
                    return

            # Exploring process. Consuming extra food every hour.
            for i in range (0, DURATION):
                if self.go_on(DANGER_LEVEL):
                    self.eat()
                else:
                    print("\tYou decide to return home")
                    return

            self.position = new_position
            print("\n*** You arrived at your destination. ")

    def map_explored(self, new_position):
        for map in self.map:
            if map.x == new_position.x and map.y == new_position.y:
                return True
        return False



    #-------------------------------------------------------------------------------------------------------------------
    # Combat methods
    #-------------------------------------------------------------------------------------------------------------------

    # This method gets called by the update method.
    # The player will automatically try to dodge (3/4 chance).
    # if the action costs more stamina than available the success will be in advantage to the enemy (1/4 chance).
    # This method receives the enemies name and damage from the enemy object which is created by the update method.

    def dodge(self, adjective, name, damage):
        STAMINA_COST = 3
        chance = random.randint(0,3)
        if self.action(STAMINA_COST):
            if chance < 3:
                input(f"\tYou dodged {adjective} {name}.")
                print()
            else:
                self.take_damage(damage)
                input(f"\tYou got hit by {adjective} {name} and took {color.RED}{damage} damage{color.END}!")
        else:
            if chance == 3:
                input(f"\tYou dodged {adjective} {name}.")
                print()
            else:
                self.take_damage(damage)
                input(f"\tYou got hit by {adjective} {name} and took {color.RED}{damage} damage{color.END}!")


#-------------------------------------------------------------------------------------------------------------------
# Enemy class
#-------------------------------------------------------------------------------------------------------------------

class Enemy (Character):

    def __init__(self, hp, stamina, danger_level):

        # Dear visitors, please excuse my humor while exploring these lists.
        adjectives = ['a deadly', 'a morbidly-obese', 'an old', 'a friendly', 'a bald', 'a furry', 'a blood-thirsty', 'nazi-zombie', 'an ugly', 'a baby', 'a smelly', 'zombie', 'a wild', 'a vicious', 'a cute', 'a shy', 'a vegan', 'a radioactive', 'an HIV-positive', 'a diabetic']
        names = ['wolf', 'bear', 'fox', 'gnu', 'rat', 'guineapig', 'parrot', 'cat', 'zombie', 'hedgehog', 'spider', 'flamingo', 'ostrich', 'eagle', 'sloth', 'dodo', 'cannibal', 'clown', 'politician', 'nazi-zombie', 'ferret', 'teenager', 'arrow to the knee', 'toddler']

        name = color.RED + random.choice(names) + color.END
        super().__init__(name, hp, stamina)
        self.adjective = color.RED + random.choice(adjectives) + color.END
        # Damage will be chosen by the danger_level passed into this method by the players update method.
        if danger_level < 3:
            self.damage = random.randint(1,2)
        elif danger_level < 5:
            self.damage = random.randint(1,3)
        else:
            self.damage = random.randint(2,4)

    def attack(self):
        input(f"\n*** You are being attacked by {self.adjective} {self.name}!\n\tYou try to dodge...")


#-------------------------------------------------------------------------------------------------------------------
# NPC class
#-------------------------------------------------------------------------------------------------------------------


class NPC (Character):

    def __init__(self, name, hp, stamina):
        super().__init__(name, hp, stamina)
        self.name = color.GREEN + name + color.END
        self.fill_inventory()

    def fill_inventory(self):
        self.add_item(Item('wood', random.randint(5, 10)))
        self.add_item(Item('food', random.randint(3,10)))
        self.add_item(Item('hide', random.randint(1,3)))
        if random.randint(0,1):
            self.add_item(Item('flint', 1))

# This method will be rewritten once the value system has been implemented.
'''
    def confirm_trade(self):
        agreement = int(input(f"\tDo you agree to the trade, {self.name}?\n\t 0: No / 1: Yes"))
        if agreement == 0:
            print(f"\t{other.name} didn't agree to the trade")
            return False
        elif agreement == 1:
            print(f"\t{self.name} agreed to your trade offer.")
            return True
'''
