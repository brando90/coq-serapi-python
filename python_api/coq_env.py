import gym
from gym import error, spaces, utils
from gym.utils import seeding
from sexpdata import loads, dumps

import coq_api
import utils

from pdb import set_trace as st

class ActionSpace:

    def __init__(self):
        '''
        Stage 1: Proving Easy Goals
        reflexivity
        assumption
        discriminate
        constructor

        Stage 2: Transforming Your Goal
        apply
        subst
        rewrite
        simpl
        cut
        unfold

        Stage 3: Breaking Apart Your Goal
        destruct
        inversion
        induction

        Stage 4: Powerful Automatic Tactics
        auto
        intuition
        omega

        https://pjreddie.com/coq-tactics/
        '''
        ## some tactics https://pjreddie.com/coq-tactics/
        tactics_no_args = ['simpl.','reflexivity','assumption.','intros.','discriminate.','constructor.','subst.','symmetry.']
        #tactics_lazy = ['auto.','intuition.','omega.']
        #tactics_args = ['apply {}.', 'rewrite {} {}.', 'cut {}.', 'unfold {}.', 'destruct {}.','induction {}.']

        tactics = tactics_no_args
        ## set available tactics
        #self.actions = tactics + tactics_lazy
        self.actions = tactics
        self.n = len(self.actions)

    def __repr__(self):
        return str(self.actions)

class CoqEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,doc_name,debug,state_embedder=lambda x: x):
        '''
        instruction for gym:
        https://github.com/openai/gym/tree/master/gym/envs
        example:
        https://github.com/openai/gym-soccer/tree/master/gym_soccer
        '''
        ## start Coq API process and create a document
        self.coq = coq_api.Coq(debug=debug)
        result_new_doc = self.coq.new_doc(doc_name) # the result serapi gives for successful creation of a document
        ## define action space
        self.action_space = ActionSpace()
        ## function that maps States -> Representation, default identity
        self.state_embedder = state_embedder

    def step(self, action):
        ''' Takes an action in the Coq env.

        Receives a tactic to add to the file and executes everything it receives.
        If at any point the proof doesn't type check, it gives a reward of -1,
        if its a Qed. and passes it gives a reward of +1.

        TODO: later we can have cancel and backtracking?

        info (dict): diagnostic information useful for debugging.
        It can sometimes be useful for learning (for example, it might contain
        the raw probabilities behind the environment’s last state change).
        However, official evaluations of your agent are not allowed to use
        this for learning.
        '''
        info = {} #useful for debugging
        ## execute action
        action_result = self.coq.add(action) # array of coq responses
        ## type check every step #TODO is this check better like this or parse it with sexp?
        coq_exceptions = []
        for action_line in action_result:
            ## extract Added number and execute that added statement
            action_line = str(action_line,"utf-8")
            if 'Added' in action_line:
                # extract exec
                sexp_result_line = loads(action_line)
                added_array = sexp_result_line[2]
                exec_nb = added_array[1]
                # execute added line
                exec_result = self.coq.exec(exec_nb)
                ## check if current exec as an CoqExc
                for exec_line in exec_result:
                    if 'CoqExn' in str(exec_line,"utf-8"):
                        coq_exceptions.append(action_line)
                        ## add action that caused exception happened
                        info['CoqExn'] = action_result
        ## evalaute reward
        reward = 0
        if len(coq_exceptions) > 0: # if it didn't type check
            reward = -1
        elif 'Qed.' in action:
            reward = 1
        else:
            reward = 0
        ## get state = (current_goal, context)
        query_result = self.coq.query('Goals')
        state = str(query_result[1]) #only the first index contains the (current_goal, context), rest is useless info about protocol to talk to serapi
        state = self.state_embedder(state)
        #print(f'type(state) = {type(state)}')
        #print(f'query_result[0] = {query_result[0]}') # start of msg
        #print(f'query_result[1] = {query_result[1]}') # real content
        #print(f'query_result[2] = {query_result[2]}') # completed part
        ## TODO: decide when environment is done...when it finishes proving all it wants (what does that mean, per proof?)
        done = False
        return state, reward, done, info

    def reset(self):
        '''
        '''
        return

    def render(self, mode='human', close=False):
        '''
        pretty print like in proof general/CoqIde
        '''
        return

    def seed(self):
        '''
        TODO
        '''
        return

    def _process_coq_response(self,serapi_response):
        '''

        Receives a tactic to add to the file and executes everything it receives.
        If at any point the proof doesn't type check, it gives a reward of -1,
        if its a Qed. and passes it gives a reward of +1.

        pseudocode:
            add command and execute all ADDs #. and check fo CoqExn.
            If CoqExn ever present -1 reward.
            once all ADDs #. have been executed without error, return the current
            goal(s) and context as the state. If the proof typed checked cuz it
            was a successful Qed. return +1 as reward and done = True.

        #TODO: check if there is a reason to distinguish between CoqExn vs not type checking
        '''
        return state, reward, done
