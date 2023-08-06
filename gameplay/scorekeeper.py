from gameplay.enums import ActionCost, ScoreValues
import random

class ScoreKeeper(object):
    def __init__(self, shift_len, capacity, hp):
        self.__ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0,
            "corpse": 0
        }
        self.__scorekeeper = {
            "killed": 0,
            "saved": 0,
            "score": 0,
            "max-score": 0,
        }
        self.__totalExperience = 0
        self.__capacity = capacity
        self.totalKilled = 0
        self.totalSaved = 0
        self.remaining_time = int(shift_len)  # minutes
        self.remaining_roles = []
        self.professions = [False, False, False, False, False, False] #In order of how they are presented on the UI, keep track of what you have and what you don't have
        self.remaining_hp = hp
        self.score_before_scram = 0

    def save(self, humanoid, cure): #basically the inventory of the ambulence (how many of each humanoid)
        if not sum(self.__ambulance.values()) >= self.__capacity: #you can only save if you are NOT at capacity
            self.remaining_time -= ActionCost.SAVE.value
            self.remaining_roles.append(humanoid.which_profession())
            #update ambulence inventory
            if humanoid.is_zombie() and not cure:
                if self.__ambulance["zombie"] == 0: #check if this is the first zombie to be added to van b/c any more added zombies added won't count towards anything
                    self.totalKilled = self.totalKilled + self.__ambulance["injured"] + self.__ambulance["healthy"] #add all humanoids ON the van currently to the tally
                    self.totalSaved = self.totalSaved - (self.__ambulance["injured"] + self.__ambulance["healthy"]) #subtract ^^
                self.__ambulance["zombie"] += 1 + self.__ambulance["injured"] + self.__ambulance["healthy"]
                self.__ambulance["injured"] = 0
                self.__ambulance["healthy"] = 0
                self.__scorekeeper["saved"] = 0
                self.__totalExperience = self.score_before_scram #set score back to what it was during the most recent scram
                self.__scorekeeper["score"] = 0
            else: #if we add a non-zombie
                if self.__ambulance["zombie"] > 0 and (not humanoid.is_corpse()): #if a zombie is present in the van, simply add to total number killed (can't be a corpse)
                    self.totalKilled += 1
                    self.__ambulance["zombie"] += 1
                else: #if no zombies, count towards people saved
                    if humanoid.is_injured():
                        self.__totalExperience += 4 #default value for saving people (slightly less for injured ppl, cuz they can't provide immediate help and need to recover)
                        self.__ambulance["injured"] += 1
                        self.totalSaved += 1
                    elif humanoid.is_corpse(): #corpses don't count towards anything
                        self.__ambulance["corpse"] += 1
                    else: 
                        self.__totalExperience += 5 #default value for saving people
                        self.__ambulance["healthy"] += 1
                        self.totalSaved += 1

                    if not humanoid.is_corpse(): #add point bonuses for getting a profession you don't ALREADY have
                        if humanoid.profession == "Engineer" and self.professions[1] == False:
                            self.__totalExperience += ScoreValues.ENGINEER.value
                            self.professions[1] == True
                        elif humanoid.profession == "Teacher" and self.professions[3] == False:
                            self.__totalExperience += ScoreValues.TEACHER.value
                            self.professions[3] = True
                        elif humanoid.profession == "Mayor" and self.professions[0] == False:
                            self.__totalExperience += ScoreValues.MAYOR.value
                            self.professions[0] = True
                        elif humanoid.profession == "Farmer" and self.professions[5] == False:
                            self.__totalExperience += ScoreValues.FARMER.value
                            self.professions[5] = True
                        elif humanoid.profession == "Doctor" and self.professions[2] == False:
                            self.__totalExperience += ScoreValues.DOCTOR.value
                            self.professions[2] = True
                        elif humanoid.profession == "Violent Criminal":
                            criminalBonus = ScoreValues.VIOLENTCRIMINAL.value
                            x = random.randint(0, 10)
                            if x <= 3 and self.professions[4] == False:
                                criminalBonus = -3
                                self.professions[4] = True
                                self.__totalExperience += criminalBonus
                    # if(self.totalSaved > 0): #calculate score
                    #     self.__scorekeeper["score"] = round((self.__totalExperience / self.totalSaved) * self.remaining_hp, 2)   
        print("Killed: " + str(self.totalKilled) + " | Saved: " + str(self.totalSaved))
        print("Score: " + str(self.__totalExperience))

    def squish(self, humanoid): 
        #take off health of the vehicle (check ideas slide)
        if self.remaining_hp > 150: # you can only squish if hp is greater than 150
            self.remaining_time -= ActionCost.SQUISH.value
            self.remaining_hp -= random.randint(100,150) # hp lost subject to change
            if humanoid.is_injured() and humanoid.did_not_convert: #Punishment for squishing someone who won't convert
                print("WAS NOT GOING CONVERT")
                self.totalKilled += 1
                self.__scorekeeper["killed"] += 1
                self.__totalExperience -= 6
            elif humanoid.is_injured() and not humanoid.did_not_convert: #bonus for squsihing someone who was going to convert
                print("WAS GOING TO CONVERT")
                self.__totalExperience += 8
            elif humanoid.is_healthy():
                self.__scorekeeper["killed"] += 1
                self.totalKilled += 1
                self.__totalExperience -= 10 #big punishment for squishing an already healthy person
        print("Killed: " + str(self.totalKilled) + " | Saved: " + str(self.totalSaved))
        print("Score: " + str(self.__totalExperience))

    def skip(self, humanoid):
        self.remaining_time -= ActionCost.SKIP.value
        if humanoid.is_injured() or humanoid.is_healthy(): #if you skip injured or healthy, the person is assumed dead
            self.__scorekeeper["killed"] += 1
            self.totalKilled += 1
        print("Killed: " + str(self.totalKilled) + " | Saved: " + str(self.totalSaved))
        print("Score: " + str(self.__totalExperience))

    def scram(self): #Return to hopspital and empty the ambulance (can get rid of zombies, so you can continue saving people)
        print("EMPTIED AMBULANCE")
        self.score_before_scram = self.__totalExperience
        self.remaining_time -= ActionCost.SCRAM.value
        if self.__ambulance["zombie"] > 0:
            self.__scorekeeper["killed"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
        else:
            self.__scorekeeper["saved"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
        self.__ambulance["zombie"] = 0
        self.__ambulance["injured"] = 0
        self.__ambulance["healthy"] = 0
        self.__ambulance["corpse"] = 0
        print("Killed: " + str(self.totalKilled) + " | Saved: " + str(self.totalSaved))
        print("Score: " + str(self.__totalExperience))

    def get_current_capacity(self):
        return sum(self.__ambulance.values())

    def at_capacity(self):
        return sum(self.__ambulance.values()) >= self.__capacity

    def get_score(self):
        self.scram()
        return self.__totalExperience
    
    def get_hp(self):
        return self.remaining_hp

    def get_killed(self):
        return self.totalKilled
    
    def get_saved(self):
        return self.totalSaved