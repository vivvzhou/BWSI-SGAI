class role_meter:
    def __init__(self, engineer, teacher, mayor
    # , farmer, doctor, criminal
    ):
        self.engineer = engineer #0
        self.teacher = teacher #1
        self.mayor = mayor #2
        # self.farmer = farmer #3
        # # self.doctor = doctor #4
        # # self.criminal = criminal #5
    
    def set_role_state(self, role_num, desired_state):
        if role_num == 0:
            self.engineer = desired_state
        elif role_num == 1:
            self.teacher = desired_state
        elif role_num == 2:
            self.mayor = desired_state
        # elif role_num == 3:
        #     self.farmer = desired_state
        # elif role_num == 4:
        #     self.doctor = desired_state
        # elif role_num == 5:
        #     self.criminal = desired_state
    
    def get_role_state(self, role_num):
        if role_num == 0:
            return self.engineer
        elif role_num == 1:
            return self.teacher
        elif role_num == 2:
            return self.mayor
        # elif role_num == 3:
        #     return self.farmer
        # elif role_num == 4:
        #     return self.doctor
        # elif role_num == 5:
        #     return self.criminal

    def get_role_bonuses(self, role_num):
        if role_num == 0:
            return 8
        if role_num == 1:
            return 2
        if role_num == 2:
            return 3
        # if role_num == 3:
        #     return 4
        # if role_num == 4:
        #     return 5
        # if role_num == 5:
        #     return 1
