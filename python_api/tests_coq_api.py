import unittest

import coq_api

# TODO: sort of ugly?
DEBUG = False

class TestStringMethods(unittest.TestCase):
    # example test: https://github.com/brando90/eit_proj1/blob/master/main_proj_lib/tests/test_user_implemented.py

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
        '''
        coq = coq_api.Coq(DEBUG)
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
        ## test
        result = coq.new_doc("foo.v")
        for i, current_result_sexpt in enumerate(result):
            self.assertEqual(str(current_result_sexpt), str(answer[i]))
        ##
        coq.kill()


    # def test_add(self):
    #     ''' Test Add serapi command.
    #
    #     (Add () "Example test_oddb1: Nat.odd 1 = true.")
    #
    #     (Answer 1 Ack)
    #     (Answer 1(Added 2((fname ToplevelInput)(line_nb 1)(bol_pos 0)(line_nb_last 1)(bol_pos_last 0)(bp 0)(ep 37))NewTip))
    #     (Answer 1 Completed)
    #     '''
    #     coq = coq_api.Coq(DEBUG)
    #     ## expected answer
    #     answer = [b'(Answer 0 Ack)\n',
    #         b'(Answer 1(Added 2((fname ToplevelInput)(line_nb 1)(bol_pos 0)(line_nb_last 1)(bol_pos_last 0)(bp 0)(ep 37))NewTip))\n',
    #         b'(Answer 0 Completed)\n']
    #     ## test
    #     result = coq.add("Example test_oddb1: Nat.odd 1 = true.")
    #     for i, current_result_sexpt in enumerate(result):
    #         self.assertEqual(str(current_result_sexpt), str(answer[i]))
    #     ##
    #     coq.kill()

if __name__ == '__main__':
    unittest.main()
