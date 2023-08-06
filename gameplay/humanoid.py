from gameplay.enums import State
from gameplay.enums import Profs 

class Humanoid(object):
    """
    Are they a human or a zombie???
    """
    def __init__(self, fp, state, value, profession, convert_chance, age, did_not_convert):
        self.fp = fp
        self.state = state
        self.value = value
        self.profession = profession
        self.convert_chance = convert_chance
        self.age = age
        self.did_not_convert = did_not_convert 

    def is_zombie(self):
        return self.state == State.ZOMBIE.value

    def is_injured(self):
        #random chance 10-30% convert  to zombie (Check ideas slides)
        return self.state == State.INJURED.value

    def is_healthy(self):
        return self.state == State.HEALTHY.value
    
    def is_corpse(self):
        return self.state == State.CORPSE.value

    def which_profession(self):
        return self.profession