import color

#-----------------------------------------------------------------------------------------------------------------------
# Status class
# This class manages health and stamina of character objects
#-----------------------------------------------------------------------------------------------------------------------

class Status:

    def __init__(self, health, stamina):
        self.health = health
        self.stamina = stamina

    def display(self):
        return f"{color.RED}Health: {self.health}    {color.GREEN}stamina: {self.stamina}{color.END}"

    def use_stamina(self, amount):
        if self.stamina - amount <= 0:
            self.stamina = 0
        else:
            self.stamina -= amount

    def recover_stamina(self, amount):
        if self.stamina + amount >= 10:
            self.stamina = 10
        else:
            self.stamina += amount

    def reduce_hp(self, amount):
        self.health -= amount

    def heal_hp(self, amount):
        if self.health + amount <= 10:
            self.health += amount
        else:
            self.health = 10
