import gym
from gym import error, spaces, utils
from gym.utils import seeding

class CoqEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    '''
    instruction for gym:
        https://github.com/openai/gym/tree/master/gym/envs
    example:
        https://github.com/openai/gym-soccer/tree/master/gym_soccer

    #TODO: check with Emilio if this is a good way to do thus
    1) run a serapi instance in the background
    2) send Coq commands to the runnign instance of serapi
    3) get responses and do stuff

    #TODO think about how to deal with the branching in proofs, since it seems
    that the implict assumption is that we can't go back in "time" in MDPs
    to continue with the proof process.
    '''
    return

  def step(self, action):
    '''
    '''
    return

  def reset(self):
    return

  def render(self, mode='human', close=False):
    '''
    pretty print like in proof general/CoqIde
    '''
    return
