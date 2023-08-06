import numpy as np
from rl_policy_evaluation.policy_enviornment import PolicyEnvironment

class PolicyAgent:
    """
    A random-policy agent.
    """

    def __init__(self, env):
        self.env = env
        self.v = np.zeros(len(env.state_space))

    def update(self, data_parser):
        """
        Update agent's state values based on random policy.
        """
        remaining_time = 720
        new_v = np.zeros(len(self.env.state_space))
        for state in self.env.state_space:
            for action in self.env.action_space:
                curr_humanoid = data_parser.get_random()
                next_humanoid = data_parser.get_random()
                remaining_time, reward = self.env.peek(remaining_time, curr_humanoid, action)
                # change to key value pair eventually but I don't know enums well
                new_v[curr_humanoid.is_what()] += (reward + self.v[next_humanoid.is_what()])
        self.v = new_v
        
        