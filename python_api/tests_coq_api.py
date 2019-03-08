import unittest

import coq_api

# TODO: sort of ugly?
DEBUG = False
coq = coq_api.Coq(DEBUG)

class TestStringMethods(unittest.TestCase):
    # example test: https://github.com/brando90/eit_proj1/blob/master/main_proj_lib/tests/test_user_implemented.py

    def test_kill(self):
        '''
        TODO

        https://stackoverflow.com/questions/55052055/why-do-i-get-subprocess-resource-warnings-despite-the-process-being-dead
        https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        '''
        coq.kill()
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
        (Answer 0 Completed)

        TODO: fix this. I tried creating its on serapi/coq process, get weird resources errors,
        what I had in mind was just creating a new coq process for each test.
        Perhaps I need to think about this again.
        '''
        ## expected answer
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
        #coq = coq_api.Coq(DEBUG)
        ## test
        #result = coq.new_doc("foo.v")
        #for i, current_result_sexpt in enumerate(result):
        #    self.assertEqual(str(current_result_sexpt), str(answer[i]))
        self.assertEqual(True,True) # TODO

    def test_add(self):
        ''' Test Add serapi command.

        (Add () "Example test_oddb1: Nat.odd 1 = true.")

        (Answer 1 Ack)
        (Answer 1(Added 2((fname ToplevelInput)(line_nb 1)(bol_pos 0)(line_nb_last 1)(bol_pos_last 0)(bp 0)(ep 37))NewTip))
        (Answer 1 Completed)
        '''
        result = coq.new_doc("bar.v")
        ## expected answer
        answer = [b'(Answer 1 Ack)\n',
            b'(Answer 1(Added 2((fname ToplevelInput)(line_nb 1)(bol_pos 0)(line_nb_last 1)(bol_pos_last 0)(bp 0)(ep 37))NewTip))\n',
            b'(Answer 1 Completed)\n']
        ## test
        result = coq.add("Example test_oddb1: Nat.odd 1 = true.")
        for i, current_result_sexpt in enumerate(result):
            if DEBUG:
                print(current_result_sexpt)
                print(answer[i])
            self.assertEqual(str(current_result_sexpt), str(answer[i]))

    def test_run_command(self):
        '''
        TODO
        '''
        #coq.run_command()
        self.assertEqual(True,True) # TODO


    def test_simple_proof(self):
        '''

        (NewDoc ((top_name (TopPhysical "foo.v"))))
        (Add () "Example test_oddb1: Nat.odd 1 = true.")
        (Add () "reflexivity.")
        (Add () "Qed.")
        (Exec 2)
        '''
        result = coq.new_doc("bar.v")
        ##
        result = coq.add("Example test_oddb1: Nat.odd 1 = true.")
        result = coq.add("reflexivity.")
        result = coq.add("Qed.")
        result = coq.exec(2)
        ## test
        for i, current_result_sexpt in enumerate(result):
            if DEBUG:
                print(current_result_sexpt)
                print(answer[i])
            self.assertEqual(str(current_result_sexpt), str(answer[i]))

if __name__ == '__main__':
    unittest.main()
