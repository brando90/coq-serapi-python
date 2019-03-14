import gym
from gym import error, spaces, utils
from gym.utils import seeding
from sexpdata import loads, dumps

import coq_api
import utils

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
        action_result = self.coq.add(action) # array of coq responses
        ## type check every step #TODO is this check better like this or parse it with sexp?
        coq_exceptions = []
        for current_result_line in action_result:
            ## extract Added number and execute that added statement
            current_result_line = str(current_result_line,"utf-8")
            if 'Added' in current_result_line:
                # extrac exec
                sexp_result_line = loads(current_result_line)
                added_array = sexp_result_line[2]
                exec_nb = added_array[1]
                # execute added line
                exec_result = self.coq.exec(exec_nb)
                ## check if current exec as an CoqExc
                for exec_line in exec_result:
                    print(current_result_line)
                    print(exec_line)
                    print(str(exec_line))
                    st()
                    print(str(current_result_line,"utf-8"))
                    if 'CoqExn' in str(current_result_line,"utf-8"):
                        coq_exceptions.append(current_result_line)
        print(len(coq_exceptions))
        ## evalaute reward
        reward = 0
        if len(coq_exceptions) > 0: # if it didn't type check
            reward = -1
        elif 'Qed.' in action:
            reward = 1
        else:
            reward = 0
        ## get state = (current_goal, context)
        state = 0
        ## TODO: decide when environment is done...when it finishes proving all it wants (what does that mean, per proof?)
        done = False
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
