import torch
from torch import nn
import torch.nn.functional as F

from sexpdata import loads

from pythonize_goals import Goals

from pdb import set_trace as st

###

AI_REP = {}

class Coq2Vec:

    def __init__(self,D_embedding,ai_coq_embeddings={}):
        super().__init__()
        ''' '''
        self.ai_coq_embeddings = ai_coq_embeddings
        self.D_embedding = D_embedding
        ai_coq_embeddings['D_embedding'] = D_embedding
        ## make sure that D_embedding matches the dimension of the embeddings already in the
        # if ai_coq_embeddings != {}:
        #     # TODO extract anything that isn't D_embedding
        #     any_dict_key = ai_coq_embeddings.keys()[0]
        #     D = self.ai_coq_embeddings[any_dict_key].size()
        #     if D != D_embedding:
        #         raise ValueError(f'Dimensions of embeddings already in dictionary and given set embedding dont match: (D,D_embedding) -> {D} != {D_embedding}.')

    def __call__(self,sexp):
        '''

        '''
        # make into pythonized s-expression
        #sexp = sexp.decode('utf-8')
        psexp = loads(sexp)
        all_goals = psexp[2][1][0][1] # [ fg_goals ..., bg_goals ..., shelved_goals ..., given_up_goals ...]
        # parse into a python object rep of the coq AST
        all_goals = Goals(all_goals)
        # print(f'all_goals = {all_goals}')
        # # gets embeddings if they exist, otherwise, it adds it to the ai_coq_embeddings dictionary/database.
        # print('--calling ty.embedding()')
        # print(f'all_goals.fg_goals[0].ty = {all_goals.fg_goals[0].ty}')
        # print(f'all_goals.fg_goals[0].ty.embedding = {all_goals.fg_goals[0].ty.embedding}')
        embedding = all_goals.fg_goals[0].ty.embedding(self.ai_coq_embeddings)
        D_embedding,nb_terms = embedding.size()
        embedding = embedding.view( (1,1,D_embedding,nb_terms) ) # dims = (N,C,H,W)
        return embedding

class Policy_ConvFcSoftmax(nn.Module):
    '''
    Policy agent implement as a # conv layers then # fully connected layers Neural Network (NN).
    '''
    def __init__(self,env,CHW, Fs, Ks, FCs,do_bn=False):
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
        out = torch.FloatTensor(1, C,H,W)
        print(f'out.size() = {out.size()}')
        in_channels = C
        print()
        for i in range(self.nb_conv_layers):
            print(f'-> i = {i}')
            F,K = Fs[i], Ks[i]
            print(f'F[{i}],K[{i}] = {F,K}')
            print(f'out.size() = {out.size()}')
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
