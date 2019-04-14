import unittest
#from sexpdata import loads, dumps
import argparse

from sexpdata import loads, dumps
from sexpdata import Symbol

import time

import coq_api
from pythonize_goals import Goals

import pdb
from pdb import set_trace as st

verbose = False

##

DEBUG = False
doc_name = 'foo.v'
env = coq_env.CoqEnv(doc_name,DEBUG)

class TestStringMethods(unittest.TestCase):

    def pythonize_eq_n_plus_0_n(self):
        '''
        Test to
        '''
        ## human readable version of the thing we are trying to embed
        human_readable_goal = '''
        1 subgoal (ID 10)

          n : nat
          ============================
          0 + n = n
        '''
        ## SeAPIs/Coqs version of the result we are trying to embed
        # sexp = '''
        #     (Answer 2
        #      (ObjList
        #       ((CoqGoal
        #         ((fg_goals
        #           (((name 4)
        #             (ty
        #              (App
        #               (Ind
        #                (((Mutind (MPfile (DirPath ((Id Logic) (Id Init) (Id Coq))))
        #                   (DirPath ()) (Id eq))
        #                  0)
        #                 (Instance ())))
        #               ((Ind
        #                 (((Mutind (MPfile (DirPath ((Id Datatypes) (Id Init) (Id Coq))))
        #                    (DirPath ()) (Id nat))
        #                   0)
        #                  (Instance ())))
        #                (App
        #                 (Const
        #                  ((Constant (MPfile (DirPath ((Id Nat) (Id Init) (Id Coq))))
        #                    (DirPath ()) (Id add))
        #                   (Instance ())))
        #                 ((Construct
        #                   ((((Mutind
        #                       (MPfile (DirPath ((Id Datatypes) (Id Init) (Id Coq))))
        #                       (DirPath ()) (Id nat))
        #                      0)
        #                     1)
        #                    (Instance ())))
        #                  (Var (Id n))))
        #                (Var (Id n)))))
        #             (hyp
        #              ((((Id n)) ()
        #                (Ind
        #                 (((Mutind (MPfile (DirPath ((Id Datatypes) (Id Init) (Id Coq))))
        #                    (DirPath ()) (Id nat))
        #                   0)
        #                  (Instance ())))))))))
        #          (bg_goals ()) (shelved_goals ()) (given_up_goals ()))))))
        # '''
        psexp = loads(sexp)
        if verbose:
            print('parsed s-expression')
            print(f'psexp = {psexp}')
            print()
        all_goals = psexp[2][1][0][1] # [ fg_goals ..., bg_goals ..., shelved_goals ..., given_up_goals ...]
        if verbose:
            print('print all goals')
            print(f'all_goals[0]={all_goals[0]}\nall_goals[1]={all_goals[1]}\nall_goals[2]={all_goals[2]}\nall_goals[3]={all_goals[3]}')
            print()
            print('---> Start decorating the object')
        all_goals = Goals(all_goals)
        if verbose:
            print(f'all_goals = {all_goals}')
            print()
            print('printed parsed ty object inside goal')
            print(f'all_goals.fg_goals.ty = {all_goals.fg_goals[0].ty}')
            print()
            print('---')
            print('print the embeddings for the Coq Term AST')
        embedding = all_goals.fg_goals[0].ty.embedding()
        print(f'embedding = {embedding}')
        ## TODO to pass the test loop through the embeddings and make sure they are
        ## 1) right number of elements 2) torch tensors in the right range
        self.assertEqual(True,True) # TODO

if __name__ == '__main__':
    print('running main in TESTS for Pythonize Coq')
    unittest.main()
