import matplotlib.pyplot as plt  

import pandas as pd

import pdb

def plot(policy,window=50):
    # number of episodes for rolling average

    fig, ((ax1), (ax2)) = plt.subplots(2, 1, sharey=True, figsize=[9, 9])
    ## plot smooth version
    rolling_mean = pd.Series(policy.return_history).rolling(window).mean()
    std = pd.Series(policy.return_history).rolling(window).std()
    ax1.plot(rolling_mean)
    # x-axis = episode step
    # y-axis = return
    ax1.fill_between(x=range(len(policy.return_history)),
                    y1=rolling_mean-std,
                    y2=rolling_mean+std,
                    color='orange', alpha=0.2)
    ax1.set_title(f'Returns Moving Average ({window}-episode window) vs Episode #')
    ax1.set_xlabel('Episode #')
    ax1.set_ylabel('Return, G')

    ##
    ax2.plot(policy.return_history)
    ax2.set_title('Returns vs Episode #')
    ax2.set_xlabel('Episode #')
    ax2.set_ylabel('Return, G')

    fig.tight_layout(pad=2)
    plt.show()
