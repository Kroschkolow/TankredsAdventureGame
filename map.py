#-----------------------------------------------------------------------------------------------------------------------
# Map class
#-----------------------------------------------------------------------------------------------------------------------

# DevNote: implement resource limits for each map.

class Map:

    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def display_coordinates(self):
        print(f"\tYour current position is ({self.x}/{self.y})\n")

    # The referenced map_list is being managed by the player class
    def find_adjacent_maps(self, map_list):
        for map in map_list:
            if map.x == self.x + 1:
                self.east = map
            elif map.x == self.x - 1:
                self.west = map
            elif map.y == self.y + 1:
                self.north = map
            elif map.y == self.y - 1:
                self.south = map
