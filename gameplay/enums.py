from enum import Enum


class State(Enum):
    ZOMBIE = "zombie"
    HEALTHY = "healthy"
    INJURED = "injured"
    CORPSE = "corpse"
    
class ActionCost(Enum):
    SAVE = 30
    CURE = 60
    SQUISH = 5
    SKIP = 15
    SCRAM = 120

class Profs(Enum):
    ENGINEER = "Engineer"
    TEACHER = "Teacher"
    MAYOR = "Mayor"
    FARMER = "Farmer"
    DOCTOR = "Doctor"
    VIOLENTCRIMINAL = "Violent Criminal"
    WORKER = "Worker"

class ScoreValues(Enum):
    ENGINEER = 8
    TEACHER = 2
    MAYOR = 3
    FARMER = 4
    DOCTOR = 5
    VIOLENTCRIMINAL = 1
    WORKER = 6