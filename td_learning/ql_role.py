from enum import IntEnum

class QLRole(IntEnum):
    """
    Enum of possible actions in the Cliff environment.
    """
    ENGINEER = "Engineer"
    TEACHER = "Teacher"
    MAYOR = "Mayor"
    FARMER = "Farmer"
    DOCTOR = "Doctor"
    CRIMINAL = "Criminal"

