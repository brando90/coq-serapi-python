import unittest
#from sexpdata import loads, dumps
import argparse

import coq_api

import time

import pdb
from pdb import set_trace as st

print(f'running TOP tests_coq_api SCRIPT')
# TODO: sort of ugly?
DEBUG = False
coq = coq_api.Coq(DEBUG)

## do new doc test here TODO: fix this horribleness
## in english, we need to create a new doc before tests are ran. But we ALSO
## want to create aunit test for the new create doc. I wanted its own function
## for running the new doc command. But idk what order tests will run so
## this hack guarantees the doc command is run FIRST and then at the end creates
## a global variable to check if the command was successful (which test the new
## doc command)
answer = [
    b'(Answer 0 Ack)\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Prelude /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Prelude.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Notations /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Notations.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Logic /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Logic.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Datatypes /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Datatypes.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Logic_Type /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Logic_Type.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Specif /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Specif.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Decimal /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Decimal.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Nat /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Nat.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Peano /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Peano.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Wf /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Wf.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Tactics /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Tactics.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 0)(route 0)(contents(FileLoaded Coq.Init.Tauto /Users/brandomiranda/.opam/4.06.0/lib/coq/theories/Init/Tauto.vo))))\n',
    b'(Feedback((doc_id 0)(span_id 1)(route 0)(contents(ProcessingIn master))))\n',
    b'(Feedback((doc_id 0)(span_id 1)(route 0)(contents Processed)))\n',
    b'(Answer 0 Completed)\n'
]
result_new_doc = coq.new_doc("foo.v")
doc_test_passed = True
for i, new_doc_line in enumerate(result_new_doc):
    doc_test_passed = doc_test_passed and ( str(new_doc_line) == str(answer[i]) )

class TestStringMethods(unittest.TestCase):
    # example test: https://github.com/brando90/eit_proj1/blob/master/main_proj_lib/tests/test_user_implemented.py

    def test_kill(self):
        '''
        Don't know if I want this test anymore...the instance closes by itself
        when the python script is done. Not sure why I would run more than one
        at a time.

        TODO:
        https://stackoverflow.com/questions/55052055/why-do-i-get-subprocess-resource-warnings-despite-the-process-being-dead
        https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        '''
        #coq.kill()
        self.assertEqual(True,True) # TODO

    def test_new_doc(self):
        ''' Test NewDoc serapi command.

        (NewDoc ((top_name (TopPhysical "foo.v"))))

        TODO: fix that the test depends on code outside the test method
        '''
        ## test
        self.assertEqual(doc_test_passed, True)

    def test_add(self):
        ''' Test Add serapi command.

        (Add () "Example test_oddb1: Nat.odd 1 = true.")
        '''
        result = coq.new_doc("bar.v")
        ## expected answer
        answer = [b'(Answer add_tag Ack)\n',
            b'(Answer add_tag(Added 2((fname ToplevelInput)(line_nb 1)(bol_pos 0)(line_nb_last 1)(bol_pos_last 0)(bp 0)(ep 37))NewTip))\n',
            b'(Answer add_tag Completed)\n']
        ## test
        result = coq.add(text='Example test_oddb1: Nat.odd 1 = true.',tag='add_tag')
        for i, current_result_sexpt in enumerate(result):
            if DEBUG:
                print(current_result_sexpt)
                print(answer[i])
            self.assertEqual(str(current_result_sexpt), str(answer[i]))

    def test_exec(self):
        '''
        TODO
        '''
        self.assertEqual(True,True)

    def test_query(self):
        '''
        TODO
        '''
        self.assertEqual(True,True)

    def test_run_command(self):
        '''
        TODO
        '''
        #coq.run_command()
        self.assertEqual(True,True) # TODO

    def test_catch_exception(self):
        '''
        TODO: make sure it does halt when a wrong proof is given
        '''
        return

if __name__ == '__main__':
    print('running main in TESTS')
    unittest.main()
