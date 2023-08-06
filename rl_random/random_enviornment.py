from enum import IntEnum
import numpy as np
import random
import math
import tkinter as tk
from ui_elements.button_menu import ButtonMenu
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.clock import Clock
from endpoints.machine_interface import MachineInterface
from ui_elements.game_viewer import GameViewer
from ui_elements.machine_menu import MachineMenu
from os.path import join


class RandomEnvironment:
    
    
    def __init__(self, data_parser):
        self.time = 0
        self.reward = 0
        self.scram = False
        self.__ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0
        }
        self.__scorekeeper = {
            "killed": 0,
            "saved": 0,
        }
        self.__capacity = 10
        self.remaining_time = int(720)  # minutes
        self.humanoid = data_parser.get_random()
        self.moves = []        
    def step(self, action, data_parser):
        done = self.is_done(data_parser)
        
        info = {}
        if done:
            if self.__ambulance["zombie"] > 0:
                self.reward = 0
            
            return self.remaining_time, self.reward , done, info, self.moves
        
        if action == "Action.Save":
            self.remaining_time -= 30
            
            if self.humanoid.is_zombie():
                self.__ambulance["zombie"] += 1
                self.reward += 0
            elif self.humanoid.is_injured():
                self.__ambulance["injured"] += 1
                self.reward += 10
            else:
                self.__ambulance["healthy"] += 1
                self.reward += 5
        
        elif action == "Action.Squish": #don't keep track of killed or saved because robot does not care, only care about highest score
            self.remaining_time -= 5
            if not self.humanoid.is_zombie():
                self.__scorekeeper["killed"] += 1
            self.reward += 0
            
        if action == "Action.Skip": #don't keep track of killed or saved because robot does not care, only care about highest score
            self.remaining_time -= 15
            if self.humanoid.is_injured():
                self.__scorekeeper["killed"] += 1
            self.reward += 0
            
        if action == "Action.Scram": #notice how robot does not care about scram. Impliment reset
            self.remaining_time -= 120
            if self.__ambulance["zombie"] > 0:
                self.__scorekeeper["killed"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
            else:
                self.__scorekeeper["saved"] += self.__ambulance["injured"] + self.__ambulance["healthy"]

            self.__ambulance["zombie"] = 0
            self.__ambulance["injured"] = 0
            self.__ambulance["healthy"] = 0
            self.reward += 0
        
        tmp = [action, self.humanoid, self.remaining_time]
        self.moves.append(tmp)
        return self.remaining_time, self.reward , done, info, self.moves

    def reset(self, data_parser):
        self.time = 0
        self.reward = 0
        self.scram = False
        self.__ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0
        }
        self.__scorekeeper = {
            "killed": 0,
            "saved": 0,
        }
        self.__capacity = 10
        self.remaining_time = int(720)  # minutes
        self.humanoid = data_parser.get_random()

    def is_done(self, data_parser):
        x = sum(self.__ambulance.values()) >= self.__capacity or len(data_parser.unvisited) == 0 or self.remaining_time <= 0
        print(str(self.remaining_time) + " ", x)
        return x