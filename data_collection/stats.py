import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

class Stats():
    
    def __init__(self):
        data = pd.read_csv(os.path.join('data_collection', 'AlephNullGameDataSAVED.txt'))
        print("human stats: ")
        print(data)
        print(data.describe())

        fig = plt.figure(figsize=(10, 5))
        data['Score'].plot.hist(grid=False, bins=20, rwidth=0.9, )
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel("score")
        plt.title('Human Score Distribution')

        fig1 = plt.figure(figsize=(10, 5))
        data.boxplot(column=['Score', 'Saved', 'Killed'])
        plt.title('Human Performance Boxplots')

        ai_data = pd.read_csv(os.path.join('data_collection', 'rl_game_data.txt'))
        
        print("ai stats: ")
        print(ai_data)
        print(ai_data.describe())

        ai_data.plot.hist(grid=False, bins=20, rwidth=0.9, )
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel("score")
        plt.title('AI Score Distribution')

        plt.rcParams["figure.autolayout"] = True
        boxdata = pd.DataFrame({"AI": ai_data['Score'], "Human": data['Score']})
        ax = boxdata[['AI', 'Human']].plot(kind='box', title='AI vs. Human Performance')
        plt.ylim(bottom=0)
        plt.ylabel("Score")

        s, p = stats.ttest_ind(ai_data, data['Score'])
        print("test statistic: " + str(s) + " P-value: " + str(p))

        plt.show()