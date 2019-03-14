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
DEBUG = False
doc_name = 'foo.v'
env = coq_env.CoqEnv(doc_name,DEBUG)

class TestStringMethods(unittest.TestCase):
    # example test: https://github.com/brando90/eit_proj1/blob/master/main_proj_lib/tests/test_user_implemented.py

    def test_positive_reward(self):
        '''

        (Add () "Example test_oddb1: Nat.odd 1 = true. reflexivity. Qed.")
        '''
        action = 'Example test_oddb1: Nat.odd 1 = true. reflexivity. Qed.'
        state, reward, done, info = env.step(action)
        self.assertEqual(reward,1)

    def test_negative_reward(self):
        '''

        (Add () "Example test_oddb1: Nat.odd 1 = true. Qed.")
        '''
        action = 'Example test_oddb1: Nat.odd 1 = true. Qed.'
        state, reward, done, info = env.step(action)
        self.assertEqual(reward,-1)

    def test_neutral_reward(self):
        '''

        (Add () "Example test_oddb1: Nat.odd 1 = true.")
        '''
        action = 'Example test_oddb1: Nat.odd 1 = true.'
        state, reward, done, info = env.step(action)
        self.assertEqual(reward,0)

if __name__ == '__main__':
    print('running main in RL ENV TESTS')
    unittest.main()
