import argparse
import gym
import numpy as np
from itertools import count

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

from ai_mathematician import D_embedding

import plotting as my_plt

import pdb

#EPS = np.finfo(np.float32).eps.item()

''' Arguments '''
parser = argparse.ArgumentParser(description='PyTorch REINFORCE example ala Brando')
parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                    help='discount factor (default: 0.99)')
parser.add_argument('--learning_rate', type=float, default=0.01, metavar='LR',
                    help='learning_rate (default: 0.01)')
parser.add_argument('--nb_episodes', type=int, default=600, metavar='N',
                    help='nb_episodes (default: 600)')
parser.add_argument('--seed', type=int, default=543, metavar='N',
                    help='random seed (default: 543)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='interval between training status logs (default: 10)')
parser.add_argument('--ema_alpha', type=float, default=0.10, metavar='G',
                    help='ema_alpha (default: 0.99)')
#parser.add_argument('--plot', dest='plot', action='store_true')
parser.add_argument('--no-plot', dest='plot', action='store_false')
parser.add_argument('--render', dest='render', action='store_true',help='render the environment')
#parser.add_argument('--no-render', dest='render', action='store_false',help='render the environment')
args = parser.parse_args()

def finish_episode(policy,optimizer, gamma):
    '''
    When an episode is done we do 3 thins:
    1) compute scaled discounted rewards
    2) update model according to SGD
    3) reset the lists holding data per episode (e.g. rewards and log_probs of actions), so that
    the next episode can start fresh.
    '''
    ## 1) compute scaled returns
    eps = np.finfo(np.float32).eps.item()
    dR = 0 # dreturn = discounted returns
    dreturns = [] # dreturns = [dR_0, dR_1, ..., dR_{H-1}]
    for r in policy.episode_rewards[::-1]: #go through reverse list of individual rewards
        dR = r + gamma*dR # dR_t = r_{t+1} + \gamma dR_{t+1}
        dreturns.insert(0, dR) #[R_t, ..., dR_{H-1}]
    dreturns = torch.tensor(dreturns)
    dreturns = (dreturns - dreturns.mean()) / (dreturns.std() + eps)
    ## 2) update model according to SGD
    policy_loss = []
    for log_prob, dreturn_ith in zip(policy.episode_actions_log_prob, dreturns):
        policy_loss.append(-log_prob * dreturn_ith)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
    # store history statistics for plotting purposes
    policy.return_history.append(np.sum(policy.episode_rewards))
    policy.loss_history.append(policy_loss.item())
    ## 3) reset current episode statistics
    del policy.episode_rewards[:]
    del policy.episode_actions_log_prob[:]

def train(policy,optimizer,env,gamma,nb_episodes=1000,time_steps=1000,ema_alpha=0.10):
    '''
    Train the policy agent with optimizer in env with gamma as discount factor.
    Model is trained in episodes. For each episode it train untils a horizon equal to the # of time steps.
    After it's done with an episode using the rewards collected during that episode,
    the model is updated.
    The running return is a way to track if in the recent history of the episodes, the agent has
    balanced the pole long enough. If it has, then the whole training is finished.
    If it has balances the pole for a lot for the past say 100, then the task has been solved.
    This is implemented with an Exponetial Moving Average (EMA) however.
    '''
    running_return = 0
    for i_episode in range(nb_episodes):
    #for i_episode in count(1):
        state, ep_return = env.reset(), 0
        for t in range(time_steps):  # Don't infinite loop while learning
            action = policy.select_action(state)
            state, reward, done, _ = env.step(action)
            st()
            if args.render:
                env.render()
            policy.episode_rewards.append(reward)
            ep_return += reward
            if done: # whether it’s time to reset the environment again. Most (but not all) tasks are divided up into well-defined episodes, and done being True indicates the episode has terminated.
                break
        running_return = ema_alpha * ep_return + (1 - ema_alpha) * running_return
        finish_episode(policy,optimizer, gamma)
        #prints every logs_interval e.g. every 10 episodes
        if i_episode % args.log_interval == 0:
            print(f'Episode {i_episode}\tLast length: {t}\tEpisode reward/length or EMA running_return: {running_return}')
        #check if task has been solved, exit training. Task solved for this env means that the agent has been able to hold the stick up for 475 steps for sufficient number of different episodes
        if running_return > env.spec.reward_threshold:
            print("---> Solved! Running return is now {running_return} and the last episode runs to {t} time steps! \a")
            break
    print(f'Running return = {running_return}\tenv.spec.reward_threshold={env.spec.reward_threshold}')

if __name__ == '__main__':
    ''' create Env '''
    doc_name = 'foo.v'
    env = coq_env.CoqEnv(doc_name,DEBUG)
    #env.seed(args.seed)
    #torch.manual_seed(args.seed)
    print(f'env = {env}')
    ''' params for training '''
    nb_episodes = args.nb_episodes
    gamma = args.gamma
    learning_rate = args.learning_rate
    ema_alpha = args.ema_alpha
    ''' Policy/AI-Mathematician '''
    ## CHW
    CHW = (1,D_embedding,1) # C=1 cuz there is not colors channels in embedding, W=1 cuz each symbol has its own embedding
    ## conv params
    nb_conv_layers=2
    Fs = [34]*nb_conv_layers
    Ks = [5]*nb_conv_layers
    ## fc params
    FCs = [len(classes)]
    ##
    policy = Policy_ConvFcSoftmax(env,nb_filters1,nb_filters2,K1,K2)
    ''' optimizer '''
    print(f'{policy.print_mdl()}')
    optimizer = optim.Adam(policy.parameters(), lr=learning_rate)
    ## Start Training
    print('--- Start Training RL agent')
    train(policy,optimizer,env,gamma,nb_episodes=nb_episodes,ema_alpha=ema_alpha)
    print('--- DONE TRAINING')
    if args.plot:
        my_plt.plot(policy)
