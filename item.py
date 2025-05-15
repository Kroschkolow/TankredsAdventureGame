import color

#-----------------------------------------------------------------------------------------------------------------------
# Basic Items
#-----------------------------------------------------------------------------------------------------------------------

class Item:
    def __init__(self, name, quantity):
        self.name = color.BLUE + name + color.END
        self.quantity = quantity
        # The value is currently being set to zero. A value system will be implemented through a dictionary.
        self.value = 0

    def description(self):
        return f"\t{self.name}: {self.quantity}"

#-----------------------------------------------------------------------------------------------------------------------
# Recipes for creating tools or special items
#-----------------------------------------------------------------------------------------------------------------------

class Recipe(Item):

    def __init__(self, name, required_items):
        super().__init__(name, 1)
        self.required_items = required_items

    def print_recipe(self):
        output = ''
        for i in self.required_items:
            output += f"\n\t {i.name}: {i.quantity}"
        return output

    # DevNote: Probably redundant.
    '''
    def description(self):
        output = f"\t{self.name}:" + self.print_recipe()
        return output
    '''



# ------------------------------    RECIPE   ------------------------------#

'''
class Special_Item(Recipe):

    def __init__(self, name, required_items):
        super().__init__(name, 1, required)
        self.required_items = required_items

    def get_special_item(self):
        return items.pop()

    #items = [Special_Item('paracord', 1)]
'''