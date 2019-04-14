import torch
from torch import nn

D_embedding = 3
AI_REP = {}


class Policy_ConvFcSoftmax(nn.Module):
    '''
    Policy agent implement as a # conv layers then # fully connected layers Neural Network (NN).
    '''
    def __init__(self,env,CHW, Fs, Ks, FCs,do_bn=False):
        ## TODO
        state_space = env.observation_space.shape[0] # 4 = |S| = |(cp,cv,pa,pv)| = |(cart_pos,cart_vel, pol_ang,pol_vel)|
        action_space = env.action_space.n # 2 = |A| = |(left,right)|
        super().__init__()
        ''' RL statistics '''
        ## statistics tracked during current episode
        self.episode_actions_log_prob = []
        self.episode_rewards = [] # [r_0, ... , r_{H-1}]
        ## statistics of training history over each episode
        self.return_history = []
        self.loss_history = []
        ''' Make Net'''
        C,H,W = CHW
        self.do_bn = do_bn
        self.nb_conv_layers = len(Fs)
        ''' Initialize Conv layers '''
        layer = 0
        self.convs = []
        self.bns_convs = []
        out = Variable(torch.FloatTensor(1, C,H,W))
        in_channels = C
        for i in range(self.nb_conv_layers):
            F,K = Fs[i], Ks[i]
            ##
            conv = nn.Conv2d(in_channels,F,K) #(in_channels, out_channels, kernel_size)
            setattr(self,f'conv{i}',conv)
            self.convs.append(conv)
            ##
            if self.do_bn:
                bn = nn.BatchNorm2d(F)
                setattr(self,f'bn2D_conv{i}',bn)
                self.bns_convs.append(bn)
            ##
            in_channels = F
            out = conv(out)
            layer+=1
        ''' Initialize FC layers'''
        self.nb_fcs_layers = len(FCs)
        ##
        self.fcs = []
        self.bns_fcs = []
        CHW = out.numel()
        in_features = CHW
        for i in range(self.nb_fcs_layers-1):
            out_features = FCs[i]
            ##
            fc = nn.Linear(in_features, out_features)
            setattr(self,f'fc{i}', fc)
            self.fcs.append(fc)
            ##
            if self.do_bn:
                print('BN_FC')
                bn_fc = nn.BatchNorm1d(out_features)
                setattr(self, f'bn1D_fc{i}', bn_fc)
                self.bns_fcs.append(bn_fc)
            ##
            in_features = out_features
            layer+=1
        ##
        i = self.nb_fcs_layers-1
        out_features = FCs[i]
        bias = self._bias_flag(only_1st_layer_bias, layer)
        fc = nn.Linear(in_features, out_features)
        layer+=1
        ##
        setattr(self,f'fc{i}', fc)
        self.fcs.append(fc)
        self.nb_layers = layer

    def forward(self, x):
        ''' conv layers '''
        for i in range(self.nb_conv_layers):
            conv = self.convs[i]
            ##
            z = conv(x)
            if self.do_bn:
                bn = self.bns_convs[i]
                z = bn(z)
            x = F.relu(z)
        _, C, H, W = x.size()
        ''' FC layers '''
        x = x.view(-1, C * H * W)
        for i in range(self.nb_fcs_layers-1):
            fc = self.fcs[i]
            z = fc(x)
            if self.do_bn:
                bn_fc = self.bns_fcs[i]
                z = bn_fc(z)
            x = F.relu(z)
        # last layer doesn't have a relu
        fc = self.fcs[self.nb_fcs_layers-1]
        x = fc(x)
        return x

    def select_action(self,state):
        '''
        Samples action accoring to policy Pi[A | S].
        '''
        ## create distribution Pi[A | S] to sample actions
        #state = torch.from_numpy(state).float().unsqueeze(0)
        probs_actions = self._policy(state)
        pi = Categorical(probs_actions) # distribution Pi[A | S]
        action = pi.sample() # a ~ Pi[A | S]
        policy.episode_actions_log_prob.append(pi.log_prob(action)) # store log_prob(action) for learning
        return action.item()

    def _policy(self, x):
        return self.forward(x)

    def print_mdl(self):
        '''
        prints the model implemented by the policy.
        '''
        #TODO
        print(f'model = TODO')
