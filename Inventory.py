#-----------------------------------------------------------------------------------------------------------------------
# Inventory class
#-------------------------------------------------------------------------------------------------------------------
import color


class Inventory:

    def __init__(self):
        self.items = []

    def add(self, item):
        for i in self.items:
            if i.name == item.name:
                i.quantity += item.quantity
                return
        self.items.append(item)

    def remove(self, item):
        for i in self.items:
            if i.name == item.name and i.quantity >= item.quantity:
                i.quantity -= item.quantity

    def print_inventory(self):
        self.clear_inventory()
        if len(self.items) == 0:
            print(f"\tNo {color.blue("items")} in inventory.")
        else:
            for i in range(0, len(self.items)):
                print(f" {i}: " + self.items[i].description())

    def clear_inventory(self):
        for i in self.items:
            if i.quantity <= 0:
                self.items.remove(i)

    # This method checks if an items quantity in an inventory is sufficient (e.g. for a trade or food consumption).
    def item_check(self, item):
        for i in self.items:
            if i.name == item.name and i.quantity >= item.quantity:
                return True
            if i.name == item.name and i.quantity < item.quantity:
                print(f"\tNot enough {item.name} ({i.quantity}/{item.quantity}) in inventory.")
                return False
        print(f"\tNo {item.name} in inventory.")
        return False
