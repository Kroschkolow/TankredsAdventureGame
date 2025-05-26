import random
#-----------------------------------------------------------------------------------------------------------------------
# World class
# This class manages time and random events
#-----------------------------------------------------------------------------------------------------------------------

class World:

    time = 6
    day = 1

    #-------------------------------------------------------------------------------------------------------------------
    # Time methods
    #-----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def display_time():
        return f"{World.time} o'clock\tday {World.day}"

    # Gets called by player class to check if there is enough time in the day for their actions
    @staticmethod
    def check_time(duration = 1):
        if World.time + duration > 24 or World.time + duration < 6:
            print("*** You are getting tired... You have to sleep!\n")
            return False
        elif World.time + duration > 21:
            print("*** You are getting tired... You should sleep soon.\n")
            return True
        else:
            return True

    @staticmethod
    def pass_time(duration = 1):
        for i in range(0, duration):
            if World.time == 23:
                World.time = 0
                World.day += 1
                print(f"\tOne hour passed... {World.display_time()}")
                print(f"\n*** DAY {World.day}!\n")
            else:
                World.time += 1
                print(f"\tOne hour passed... {World.display_time()}")


    #-------------------------------------------------------------------------------------------------------------------
    # Event methods
    # The only implemented events are currently random attacks.
    # Once a map resource system, and thereby reasons to go exploring the world, will be implemented,
    # more of the random events below will be implemented into the game. Maybe even in resource gathering.
    #-----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def random_attack(danger_level):
        #type = random.randint(0)
        possibility = 0
        if danger_level == 0:
            return
        elif danger_level == 1:
            possibility = random.randint(0, 7)
        elif danger_level == 2:
            possibility = random.randint(1, 8)
        elif danger_level == 3:
            possibility = random.randint(1, 9)
        elif danger_level == 4:
            possibility = random.randint(5, 8)
        elif danger_level == 5:
            possibility = random.randint(6, 9)
        return possibility

'''
    @staticmethod
    def choose_event(danger_level):
        event = random.randint(0, 10)
        if event < 5:
            World.random_attack(danger_level)
        elif event == 1:
            merchant = NPC.NPC('merchant', 20, 10)
            merchant.fill_inventory()
            print(f"*** You encountered a {merchant.name}")
            decision = int(input(f"\tDo you wish to trade with {random.choice(['him', 'her'])}?"))
            if decision:
                Player.player.trade(merchant)
            else:
                print("\tThe merchant wandered into the woods...")
        elif event == 2:
            print("Thorny thicket")

    @staticmethod
    def explore_event(event = random.randint(0,2)):
        # RIVER
        if event == 0:
            STAMINA_COST = 3
            print("*** You emerge from the woods and find yourself at a river.")
            decision = int(input("\tDo you want to cross it?\n\t 0: No / 1: Yes\n\t "))
            if decision:
                for i in range(0, STAMINA_COST):
                    Player.player.action(1)
                print("\tYou successfully crossed the river and venture forth...\n")
            else:
                print("\tYou chose not to take the risk and return home...\n")
                return

        # MERCHANT
        elif event == 1:
            merchant = NPC.NPC('merchant', 20, 10)
            print(f"*** You encountered a {merchant.name}")
            decision = int(input(f"\tDo you wish to trade with {random.choice(["him", "her"])}?\n\t 0: No / 1: Yes\n\t "))
            if decision:
                Player.player.trade(merchant)
            else:
                print("\tThe merchant vanishes into the woods...")

        # THORNY_THICKET
        elif event == 2:
            STAMINA_COST = 3
            print("Thorny thicket")
'''