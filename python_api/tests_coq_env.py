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

    # def test_positive_reward(self):
    #     '''
    #
    #     (Add () "Example test_oddb1: Nat.odd 1 = true. reflexivity. Qed.")
    #     '''
    #     action = 'Example test_oddb1: Nat.odd 1 = true. reflexivity. Qed.'
    #     state, reward, done, info = env.step(action)
    #     self.assertEqual(reward,1)
    #
    # def test_negative_reward(self):
    #     '''
    #
    #     (Add () "Example test_oddb1: Nat.odd 1 = true. Qed.")
    #     '''
    #     action = 'Example test_oddb1: Nat.odd 1 = true. Qed.'
    #     state, reward, done, info = env.step(action)
    #     self.assertEqual(reward,-1)
    #
    # def test_neutral_reward(self):
    #     '''
    #
    #     (Add () "Example test_oddb1: Nat.odd 1 = true.")
    #     '''
    #     action = 'Example test_oddb1: Nat.odd 1 = true.'
    #     state, reward, done, info = env.step(action)
    #     self.assertEqual(reward,0)

    def test_get_raw_state(self):
        '''
        Run the test to get raw string rep of coq (Goal,Context)

            Theorem plus_0_n:
            forall n : nat, 0 + n = n.
            Proof.
              intros n.
              simpl.
              reflexiity.
            Qed.
        '''
        print('running test_get_raw_state')
        action = '''
            Theorem plus_0_n:
            forall n : nat, 0 + n = n.
            Proof.
              intros n.
            '''
        expected_state = b'(Answer 5(ObjList((CoqGoal((fg_goals(((name 4)(ty(App(Ind(((Mutind(MPfile(DirPath((Id Logic)(Id Init)(Id Coq))))(DirPath())(Id eq))0)(Instance())))((Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Const((Constant(MPfile(DirPath((Id Nat)(Id Init)(Id Coq))))(DirPath())(Id add))(Instance())))((Construct((((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)1)(Instance())))(Var(Id n))))(Var(Id n)))))(hyp((((Id n))()(Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))))))))(bg_goals())(shelved_goals())(given_up_goals()))))))'
        state, reward, done, info = env.step(action)
        print()
        print(f'expected_state = {expected_state}')
        print()
        print(f'state = {state}')
        #self.assertEqual(state,expected_state)
        # TODO
        print('done running test_get_raw_state')


if __name__ == '__main__':
    print('running main in RL ENV TESTS')
    unittest.main()
    print('Done running tests in coq env tests')
