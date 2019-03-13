import unittest
#from sexpdata import loads, dumps
import argparse

import coq_api

import time

import pdb
from pdb import set_trace as st

print(f'running TOP tests_coq_api SCRIPT')
# TODO: sort of ugly?
DEBUG = True
coq = coq_api.Coq(DEBUG)

#CoqExn

class TestStringMethods(unittest.TestCase):
    # example test: https://github.com/brando90/eit_proj1/blob/master/main_proj_lib/tests/test_user_implemented.py

    def test_kill(self):
        '''
        TODO:
        https://stackoverflow.com/questions/55052055/why-do-i-get-subprocess-resource-warnings-despite-the-process-being-dead
        https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        '''
        #coq.kill()
        self.assertEqual(True,True) # TODO

    def test_new_doc(self):
        ''' Test NewDoc serapi command.

        (NewDoc ((top_name (TopPhysical "foo.v"))))

        (Answer 0 Ack)
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Prelude /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Prelude.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Notations /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Notations.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Logic /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Logic.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Datatypes /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Datatypes.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Logic_Type /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Logic_Type.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Specif /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Specif.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Decimal /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Decimal.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Nat /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Nat.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Peano /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Peano.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Wf /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Wf.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Tactics /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Tactics.vo))))
        (Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Tauto /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Tauto.vo))))
        (Feedback((doc_id 0)(span_id 1)(route 0)(contents(ProcessingIn master))))
        (Feedback((doc_id 0)(span_id 1)(route 0)(contents Processed)))
    #     (Answer 0 Completed)


if __name__ == '__main__':
    print('running main in TESTS')
    unittest.main()
