
import argparse
import gym
import numpy as np
from itertools import count

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

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

''' RL Agent (Neural Net Policy model) '''

class Policy(nn.Module):
    '''
    Policy agent implemented as a Neural Network.
    '''
    def __init__(self,env,nb_hidden=128,p_drop_out=0.5):
        super(Policy, self).__init__()
        ##
        state_space = env.observation_space.shape[0] # 4 = |S| = |(cp,cv,pa,pv)| = |(cart_pos,cart_vel, pol_ang,pol_vel)|
        action_space = env.action_space.n # 2 = |A| = |(left,right)|

        ## affine/linear layers
        self.affine1 = nn.Linear(state_space, nb_hidden)
        self.affine2 = nn.Linear(nb_hidden, action_space)
        self.p_drop_out = p_drop_out

        ## statistics tracked during current episode
        self.episode_actions_log_prob = []
        self.episode_rewards = [] # [r_0, ... , r_{H-1}]
        ## statistics of training history over each episode
        self.return_history = []
        self.loss_history = []
        ## model
        self.model = torch.nn.Sequential(
                    self.affine1,
                    nn.Dropout(p=self.p_drop_out),
                    nn.ReLU(),
                    self.affine2,
                    nn.Softmax(dim=-1)
                )

    def forward(self, x):
        '''
        Predict distribution over actions according to NNs + softmax layer.
        '''
        #original_mdl = torch.nn.Sequential(self.affine1,nn.ReLu(),self.affine2)
        return self.model(x)

    def print_mdl(self):
        '''
        prints the model implemented by the policy.
        '''
        print(f'model = {self.model}')

    def _policy(self, x):
        return self.forward(x)

    def select_action(self,state):
        '''
        Samples action accoring to policy Pi[A | S].
        '''
        ## create distribution Pi[A | S] to sample actions
        state = torch.from_numpy(state).float().unsqueeze(0)
        probs_actions = self._policy(state)
        pi = Categorical(probs_actions) # distribution Pi[A | S]
        action = pi.sample() # a ~ Pi[A | S]
        policy.episode_actions_log_prob.append(pi.log_prob(action)) # store log_prob(action) for learning
        return action.item()

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
            if args.render:
                env.render()
            policy.episode_rewards.append(reward)
            ep_return += reward
            if done:
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
    ## create Env
    env = gym.make('CartPole-v1')
    env.seed(args.seed)
    torch.manual_seed(args.seed)
    print(f'env = {env}')
    print(f'env.spec.reward_threshold = {env.spec.reward_threshold}')
    ## params for training
    nb_episodes = args.nb_episodes
    gamma = args.gamma
    learning_rate = args.learning_rate
    ema_alpha = args.ema_alpha
    ## ML stuff
    policy = Policy(env)
    print(f'{policy.print_mdl()}')
    optimizer = optim.Adam(policy.parameters(), lr=learning_rate)
    ## Start Training
    print('--- Start Training RL agent')
    train(policy,optimizer,env,gamma,nb_episodes=nb_episodes,ema_alpha=ema_alpha)
    print('--- DONE TRAINING')
    if args.plot:
        my_plt.plot(policy)

