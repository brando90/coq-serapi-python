import argparse
import gym
import numpy as np
from itertools import count

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

import coq_env
from ai_mathematician import Coq2Vec
from ai_mathematician import AI_REP
from ai_mathematician import Policy_ConvFcSoftmax

from pythonize_goals import Goals

#import plotting as my_plt

from pdb import set_trace as st

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
parser.add_argument('--DEBUG', dest='DEBUG', action='store_true',help='set debugging flag')
parser.add_argument('--D_embedding', type=int, default=10,
                    help='Dimension of the embeddings for the symbols')
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
    '''
    #running_return = 0
    state, reward, done, _ = env.step('Example test_oddb1: Nat.odd 1 = true.')
    print(f'state = {state}')
    for i_episode in range(nb_episodes):
        for t in range(time_steps):  # Don't infinite loop while learning
            action = policy.select_action(state)
            st()
            state, reward, done, _ = env.step(action)
            st()
            if args.render:
                env.render()
            policy.episode_rewards.append(reward)
            ep_return += reward
            # Check whether it’s time to reset the environment again.
            # Most (but not all) tasks are divided up into well-defined episodes, and done being True indicates the episode has terminated.
            if done:
                #TODO for the moment we exit, but it should proceed to prove the next theorem
                return
        finish_episode(policy,optimizer, gamma)
        #prints every logs_interval e.g. every 10 episodes
        if i_episode % args.log_interval == 0:
            print(f'Episode {i_episode}\tLast length: {t}\tep_return = {ep_return}')

if __name__ == '__main__':
    DEBUG = args.DEBUG
    D_embedding = args.D_embedding
    ''' create Env '''
    doc_name = 'foo.v'
    state_embedder = Coq2Vec(D_embedding,ai_coq_embeddings={})
    env = coq_env.CoqEnv(doc_name,DEBUG,state_embedder=state_embedder)
    #env.seed(args.seed)
    #torch.manual_seed(args.seed)
    print(f'doc name = {doc_name} \nenv = {env}')
    ''' params for training '''
    nb_episodes = args.nb_episodes
    gamma = args.gamma
    learning_rate = args.learning_rate
    ema_alpha = args.ema_alpha
    ''' Policy/AI-Mathematician '''
    action_space = env.action_space
    print(f'Action space/tactics: {env.action_space}')
    ## CHW = (C=1,H=D_embedding,W=nb_symbols_in_input)
    #NOTE: filter sizes are limited by the number of symbols in the inpiut check evernote FILTER SIZE CONVAITP
    nb_symbols_in_input = 1
    CHW = (1,D_embedding,nb_symbols_in_input) # C=1 cuz there is not colors channels in embedding, H=D_embedding, W=number of symbols in formula
    ## conv params
    Fs = [34,28]
    nb_symbols_2_process_layer1 = 1
    Ks = [(D_embedding,nb_symbols_2_process_layer1)] # kernel = [H,W]
    nb_symbols_2_process_layer1 = 1
    Ks.append( (1,nb_symbols_2_process_layer1) )
    ## fc params
    FCs = [action_space.n]
    ##
    policy = Policy_ConvFcSoftmax(env,CHW,Fs,Ks,FCs)
    print(f'{policy.print_mdl()}')
    ''' optimizer '''
    optimizer = optim.Adam(policy.parameters(), lr=learning_rate)
    ## Start Training
    print('--- Start Training RL agent')
    train(policy,optimizer,env,gamma,nb_episodes=nb_episodes,ema_alpha=ema_alpha)
    print('--- DONE TRAINING')
    if args.plot:
        my_plt.plot(policy)
