import unittest
#from sexpdata import loads, dumps
import argparse

import coq_api
import coq_env

import time

import pdb
from pdb import set_trace as st

print(f'running TOP tests_coq_api SCRIPT')
# TODO: sort of ugly?
DEBUG = True
doc_name = 'foo.v'
env = coq_env.CoqEnv(doc_name,DEBUG)

class TestStringMethods(unittest.TestCase):
    # example test: https://github.com/brando90/eit_proj1/blob/master/main_proj_lib/tests/test_user_implemented.py

    def test_step(self):
        '''
        '''
        action = '(Add () "Example test_oddb1: Nat.odd 1 = true.")'
        state, reward, done, info = env.step(action)
        self.assertEqual(reward,0)

if __name__ == '__main__':
    print('running main in RL ENV TESTS')
    unittest.main()
