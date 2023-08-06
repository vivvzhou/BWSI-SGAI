import argparse
import os
import tkinter as Tk
from tkinter import simpledialog
import tkinter.messagebox as tK
import sys
from endpoints.data_parser import DataParser
from endpoints.data_parser_300 import DataParser300
from endpoints.machine_interface import MachineInterface
from gameplay.scorekeeper import ScoreKeeper
from gameplay.ui import UI
from rl_random.random_action import Action
from rl_random.random_enviornment import RandomEnvironment
from rl_random.random_agent import RandomAgent
from rl_policy_evaluation.policy_enviornment import PolicyEnvironment
from rl_policy_evaluation.policy_agent import PolicyAgent
from rl_policy_evaluation.policy_gui import PolicyGUI
from td_learning.ql_agent import QLAgent
from td_learning.ql_enviornment import QLEnvironment
from td_learning.ql_runs import runs
from td_learning.ql_train import train
from td_learning.ql_episode import episode
from td_learning.ql_evaluate import evaluate
from td_learning.ql_plot import plot
from td_learning.ql_optimize import optimize
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from game_menu_ui.game_menu import GameMenu
from csv import writer
import csv
from data_collection.stats import Stats

class Main(object):
    """
    Base class for the SGAI 2023 game
    """
    def __init__(self, is_automode, is_disable, is_random, is_super, is_training, is_plotting, is_evaluating, is_optimizing, is_stats):
        self.data_fp = os.getenv("SGAI_DATA", default=os.path.join('data', 'default_dataset'))
        self.data_parser = DataParser(self.data_fp)

        self.scorekeeper = ScoreKeeper(self.data_parser.shift_length, self.data_parser.capacity, self.data_parser.hp)

        if is_random:
            basic_env = RandomEnvironment(self.data_parser)
            rl_agent = RandomAgent('Random')
            total_reward = 0
            for _ in range(1):
                basic_env.reset(self.data_parser)
                episode_reward = 0
                done = False
                while not done:
                    action = rl_agent.get_action()
                    
                    time, reward, done, info, moves = basic_env.step(action, self.data_parser)
                    if done:
                        print('Episode Reward: {}'.format(reward))
                        print('Episode Reward: {}'.format(moves))
            
        elif is_training: #train the model
            print("Training...")
            time = 720
            hp = 10
            capacity = 10
            env = QLEnvironment(time, hp, capacity)
            agent = QLAgent(env.state_space, env.time_space, env.hp_space, env.capacity_space, env.role_space, env.roleMeter_space, env.action_space, 0.6, 0.1, 1, True)
            train(env, time, hp, capacity, agent, 100000, False)
            
        elif is_plotting: #plot the latest training data
            print("Plotting...")
            plot()
        
        elif is_evaluating: #Run it multiple times, currently set to 500 runs, and find the average reward and score
            print("Evaluating...")
            time = 720
            hp = 10
            capacity = 10
            env = QLEnvironment(time, hp, capacity)
            agent = QLAgent(env.state_space, env.time_space, env.hp_space, env.capacity_space, env.role_space, env.roleMeter_space, env.action_space, 0.6, 0.1, 1, False) 
            num_runs = 1000
            avgReward, avgScore, all_rewards, all_scores = evaluate(env, time, hp, capacity, agent, num_runs, False)
            
            count = 0
            file_path = os.path.join("data_collection", "rl_game_data.txt")
            f = open(file_path, "w")
            f.write("Score\n")
            while count < num_runs:
                AiData = str(all_scores[count])
                f.write(AiData)
                f.write("\n")
                count += 1
            f.close()

        elif is_optimizing: #find the optimal epsilon value and plot a graph of epsilon vs. score
            print("Finding optimal epsilon...")
            optimize(0.05, 0.0, 1.0)

        elif is_super: #Run it once and get the reward and score from that one game run
            print("running RL...")
            #env = PolicyEnvironment()
            #agent = PolicyAgent(env)
            #game = PolicyGUI(env, agent, self.data_parser)
            #game.mainloop()
            time = 720
            hp = 10
            capacity = 10
            env = QLEnvironment(time, hp, capacity)
            agent = QLAgent(env.state_space, env.time_space, env.hp_space, env.capacity_space, env.role_space, env.roleMeter_space, env.action_space, 0.6, 0.1, 1, False)
            totalReward, totalScore = runs(env, time, hp, capacity, agent, False)
            AiData = [totalReward, totalScore]
            #with open('data_collection\AlephNullRlData.csv', 'a') as f_object:
            #    writer_object = writer(f_object)
            #    writer_object.writerow(AiData)
            #    f_object.close() 
           
                
        elif is_stats:
            stats = Stats()

        elif not is_automode:  # Launch UI gameplay
            self.game_menu = GameMenu(self.data_parser, self.scorekeeper, self.data_fp, is_disable)
            z = Tk.messagebox.askyesno(title='Restart?', message='Do you want to restart?',)
            Name = simpledialog.askstring("Input", "What is your first name?")
            if Name == None:
                Name = "None"
            self.TotalScore = self.scorekeeper.get_score()
            self.TotalSaved = self.scorekeeper.get_saved()
            self.TotalKilled = self.scorekeeper.get_killed()
            GameData = [Name, self.TotalScore, self.TotalSaved, self.TotalKilled]
            with open('data_collection\AlephNullGameData.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(GameData)
                f_object.close()
            with open('data_collection\AlephNullGameData.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                score_avg = 0
                saved_avg = 0
                killed_avg = 0
                rowz = 0.0
                for row in csv_reader:
                    if row['Score'] != None and row['Score'].isnumeric():
                        score_avg += int(row['Score'])
                        rowz += 1
                    if row['Saved'] != None and row['Saved'].isnumeric():
                        saved_avg += int(row['Saved'])
                    if row['Killed'] != None and row['Killed'].isnumeric():
                        killed_avg += int(row['Killed'])
                score_avg = score_avg / rowz
                score_avg = "{:.2f}".format(score_avg)
                saved_avg = saved_avg / rowz
                saved_avg = "{:.2f}".format(saved_avg)
                killed_avg = killed_avg / rowz 
                killed_avg = "{:.2f}".format(killed_avg)
                csv_file.close() 
            if z:
                 os.execl(sys.executable, sys.executable, *sys.argv)
        else:  # Run in background until all humanoids are processed
            simon = MachineInterface(None, None, None, is_automode)
            while len(self.data_parser.unvisited) > 0:
                if self.scorekeeper.remaining_time <= 0:
                    pass
                else:
                    humanoid = self.data_parser.get_random()
                    simon.suggest(humanoid)
                    simon.act(self.scorekeeper, humanoid)
            print(self.scorekeeper.get_score())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='python3 main.py',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('-a', '--automode', action='store_true', help='No UI, run autonomously with model suggestions')
    parser.add_argument('-d', '--disable', action='store_true', help='Disable model help')
    parser.add_argument('-r', '--random', action='store_true', help='Enable Super Random Mode')
    parser.add_argument('-s', '--super', action='store_true', help='Enable Super AUTO Mode')
    parser.add_argument('-t', '--train', action='store_true', help='Train the RL model')
    parser.add_argument('-p', '--plot', action='store_true', help='Plot the graph')
    parser.add_argument('-e', '--evaluate', action='store_true', help = 'Evaluate the RL model' )
    parser.add_argument('-o', '--optimize', action='store_true', help = 'Optimize epsilon' )
    parser.add_argument('-S', '--stats', action='store_true', help = 'Display statistics' )

    args = parser.parse_args()
    Main(args.automode, args.disable, args.random, args.super, args.train, args.plot, args.evaluate, args.optimize, args.stats)