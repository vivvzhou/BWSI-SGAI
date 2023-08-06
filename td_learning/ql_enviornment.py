import copy
from enum import IntEnum
import numpy as np
from td_learning.ql_action import QLAction
from td_learning.ql_role_meter import role_meter
import copy


class QLEnvironment:
    """
    The Cliff environment shown in Example 6.6.
    """
    action_space = list(map(int, QLAction))

    def __init__(self, time, hp, capacity):
        self.state_space = [0, 1, 2, 3] #["zombie", "healthy", "injured", "corpse"]
        self.time_space = [i for i in range((time//5) + 1)]
        self.hp_space = [i for i in range(hp + 1)]
        self.capacity_space = [i for i in range(capacity + 1)]
        self.role_space = [0, 1, 2]
        self.scoreLastScram = 0
        # , 3, 4, 5
        #["engineer", "teacher", "mayor", "farmer", "doctor", "criminal"]

        master_role_meter = role_meter(False, False, False
        # , False, False, False
        ) #define the "master" role meter

        self.roleMeter_space = []
        self.generate_role_meter(0, master_role_meter) #populate roleMeter_Space
        self.capacity_left = capacity
        self.hp_left = hp
        self.time_left = time
        self.zombie = 0
        self.healthy = 0
        self.injured = 0
        self.corpse = 0
        self.roles = [False] * 6
        
    def generate_role_meter(self, iterationNum, roleMeter_master):
        # if iterationNum == 6: #stop condition and add to the array
        #     roleMeterCopy = copy.copy(roleMeter_master) #make a SHALLOW copy of the master role meter and append it to the roleMeter space
        #     self.roleMeter_space.append(roleMeterCopy)
        #     return

        if iterationNum == 3: #stop condition and add to the array
            roleMeterCopy = copy.copy(roleMeter_master) #make a SHALLOW copy of the master role meter and append it to the roleMeter space
            self.roleMeter_space.append(roleMeterCopy)
            return
        
        roleMeter_master.set_role_state(iterationNum, True)
        self.generate_role_meter(iterationNum + 1, roleMeter_master)

        roleMeter_master.set_role_state(iterationNum, False)
        self.generate_role_meter(iterationNum + 1, roleMeter_master)
    
    def _is_goal(self):
        """
        Checks if current state is the goal state.
        """
        return self.time_left <= 0

    def reset(self, time, hp, capacity):
        """
        Resets environment and returns initial state.
        """
        self.time_left = time
        self.hp_left = hp
        self.capacity_left = capacity
        #self.roles = [False] * 6
        self.roles = [False] * 3
        return self.time_left

    def step(self, action, state, role, roleMeter, base_capacity):
        """
        Performs given action and returns next_state, reward, done.
        """
        next_roleMeter = copy.copy(roleMeter)
        reward = 0
        score = 0
        if action == QLAction.SKIP:
            #print("SKIP")
            self.time_left -= 15  #make skipping injured and healthy same bad for now
            if state == 1:
                reward -= 10
                score -= 1
            elif state == 2:
                reward -= 6
                score -= 1
            # else:
            #     reward -= 1
        elif action == QLAction.SQUISH:
            #print("SQUISH")
            self.time_left -= 5
            self.hp_left -= 1
            # if state == 0:
            #     reward -= 1
            if state == 1:
                reward -= 10
                score -= 10
            if state == 2:
                reward -= 6
                score -= 6
            # if state == 3:
            #     reward -= 50
        elif action == QLAction.SAVE:
            #print("SAVE")
            next_roleMeter.set_role_state(role, True) #set a picked up role to be True
            self.capacity_left -= 1
            self.time_left -= 30
            if state == 0:
                reward -= 20
                self.zombie += 1
                score = self.scoreLastScram
            if state == 1:
                reward += 10
                score += 5
                self.healthy += 1
                if next_roleMeter.get_role_state(role) == True and roleMeter.get_role_state(role) == False: #if you got a NEW profession, you get a bonus!!
                    reward += roleMeter.get_role_bonuses(role)
            if state == 2:
                reward += 5
                score += 4
                self.injured += 1
                if next_roleMeter.get_role_state(role) == True and roleMeter.get_role_state(role) == False: #if you got a NEW profession, you get a bonus!!
                    reward += roleMeter.get_role_bonuses(role)
            if state == 3:
                reward -=10
                self.corpse += 1
        elif action == QLAction.CURE:
            #print("CURE")
            next_roleMeter.set_role_state(role, True)
            self.capacity_left -= 1
            self.time_left -= 60
            if state == 0:
                reward += 10
                score += 5
                self.healthy += 1
            if state == 1:
                reward -= 10
                score += 5
                self.healthy += 1
            if state == 2:
                reward -= 10
                score += 4
                self.injured += 1
            if state == 3:
                reward -=10
                self.corpse += 1
            if state == 0 or state == 1 or state == 2:
                if next_roleMeter.get_role_state(role) == True and roleMeter.get_role_state(role) == False: #if you got a NEW profession, you get a bonus!!
                    reward += roleMeter.get_role_bonuses(role)
        elif action == QLAction.SCRAM:
            #print("SCRAM")
            self.capacity_left = base_capacity
            self.time_left -= 120

            self.scoreLastScram = score
            #The more people you get, the bigger the rewards, hence the square
            if self.healthy + self.injured - 4 >= 0:
                reward += (self.healthy + self.injured - 4) ** 2 #can only make net profit if you save a decent amount of people; disincentivises unecessariy scramming unless you can get something good out of it
            else:
                reward -= 5
                
            self.zombie = 0
            self.healthy = 0
            self.injured = 0
            self.corpse = 0
            self.roles = [False] * 6
            
        done = self._is_goal()

        return np.random.choice(self.state_space), self.time_left, self.hp_left, self.capacity_left, np.random.choice(self.role_space), next_roleMeter, reward, score, done

        