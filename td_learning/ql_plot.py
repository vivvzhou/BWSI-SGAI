import copy
from enum import IntEnum
import numpy as np
import numpy
from td_learning.ql_episode import episode
import os
import matplotlib.pyplot as plt
from numpy import arange, cos, linspace, pi, sin, random
from scipy.interpolate import splprep, splev
import pylab
import pandas as pd


def plot():
    code_dir = os.path.dirname(__file__)
    file_path = os.path.join(code_dir, "total_reward.txt")
    f = open(file_path, "r") #open file in read only
    total_rewards = []
    row = f.readline()
    rowList = row.split(" ")
    for i in range(len(rowList)-1): #read the file and insert the data into the array variable
        total_rewards.append(float(rowList[i]))
    print("plotting...")
    
    x = list(range(0, len(rowList)-1))
    y = total_rewards
    
    xavg = []
    yavg = []
    mean = 0
    counter = 0
    
    for i in range(len(rowList)-1): #make average
        if counter != 1000:
            mean += y[i]
            counter += 1
        else:
            counter = 0
            xavg.append(i)
            yavg.append(mean/1000)
            mean = 0
        
            
    print("plotting...")
    
    df = pd.DataFrame([xavg, yavg])
    
    print(df)
    print(df.iloc[0])
    
    fig, ax = plt.subplots(1,1)
    ax.scatter(x, y, label = 'reward', alpha = 0.1)
    ax.plot(xavg, yavg, c = 'red')
    ax.set_xlabel("runs")
    ax.set_ylabel("score")
    

    
    #z = np.polyfit(x, y, 5)
    #zs = np.polyfit(x, s, 6)

    #p = np.poly1d(z)
    #ps = np.poly1d(zs)

    #fig = plt.figure(figsize=(10, 5))
    #ax = fig.add_subplot(1, 1, 1)

    #ax.set_xlabel('runs')
    #ax.set_ylabel('reward')
    #ax.scatter(x, y, label = 'reward', alpha = 0.1)
    #ax.plot(x, p(x), color= 'r' , linestyle = 'dashed', label = 'reward fit')
    #ax.legend(loc='upper left')

    #fig = plt.figure(figsize = (10, 5))
    #ax1 = fig.add_subplot(1, 1, 1)

    #ax1.set_xlabel('runs')
    #ax1.set_ylabel('score')
    #ax1.scatter(x, s, label = 'score', alpha = 0.1, c = 'orange')
    #ax1.plot(x, ps(x), color= 'r', linestyle = 'dashed', label = 'score fit')
    #ax1.legend(loc='upper left')
    plt.show()

    return total_rewards