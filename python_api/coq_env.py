import gym
from gym import error, spaces, utils
from gym.utils import seeding

import coq_api

from pdb import set_trace as st

class CoqEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,doc_name,debug):
        '''
        instruction for gym:
        https://github.com/openai/gym/tree/master/gym/envs
        example:
        https://github.com/openai/gym-soccer/tree/master/gym_soccer
        '''
        self.coq = coq_api.Coq(debug=debug)
        result_new_doc = self.coq.new_doc(doc_name)

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
        print('doing action')
        result = self.coq.add(action) # array of coq responses
        print('getting results')
        ## type check every step
        for current_result_line in result:
            #self.coq.exe()
            print(current_result_line)

        return state, reward, done, info

    def reset(self):
        return

    def render(self, mode='human', close=False):
        '''
        pretty print like in proof general/CoqIde
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
