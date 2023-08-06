import copy
from enum import IntEnum
import numpy as np
from td_learning.ql_role_meter import role_meter



def episode(env, time, hp, capacity, agent):
    """
    Run one episode with given environment and agent and return total reward.
    """
    env.reset(time, hp, capacity)
    done = False
    total_reward = 0
    total_score = 0
    state, role = agent.get_state_role()
    base_capacity = capacity
    roleMeter = role_meter(False, False, False
    # , False, False, False
    )

    while not done:
        
        action = agent.get_action(state, time, hp, capacity, role, roleMeter)
        next_state, next_time, next_hp, next_capacity, next_role, next_roleMeter, reward, score, done = env.step(action, state, role, roleMeter, base_capacity)
        agent.update_q(state, time, hp, capacity, role, roleMeter, action, reward, next_state, next_time, next_hp, next_capacity, next_role, next_roleMeter, done)
        capacity = next_capacity
        state = next_state
        role = next_role
        time = next_time
        hp = next_hp
        total_reward += reward
        total_score += score
        roleMeter = copy.copy (next_roleMeter)
        #print(" ")
    return total_reward, total_score