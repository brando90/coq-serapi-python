import unittest

import coq_api

# TODO: sort of ugly?
debug = False
coq = coq_api.Coq(debug)

class TestStringMethods(unittest.TestCase):
    # example test: https://github.com/brando90/eit_proj1/blob/master/main_proj_lib/tests/test_user_implemented.py

    def test_add(self):
        '''
        Testing the following:

        (Add () "Example test_oddb1: Nat.odd 1 = true.")

        (Answer 0 Ack)
        (Answer 0(CoqExn()()(Backtrace())(NoSuchState 0)))
        (Answer 0 Completed)
        '''
        answer = [b'(Answer 0 Ack)\n',
            b'(Answer 0(CoqExn()()(Backtrace())(NoSuchState 0)))\n',
            b'(Answer 0 Completed)\n']
        result = coq.add("Example test_oddb1: Nat.odd 1 = true.")
        for i, current_result_sexpt in enumerate(result):
            print(current_result_sexpt)
            print(answer[i])
            self.assertEqual(str(current_result_sexpt), str(answer[i]))
            #self.assertEqual(current_result_sexpt, answer[i])

    def test_tagged_add(self):
        '''
        ( tag1 (Add () "Example test_oddb1: Nat.odd 1 = true.") )

        (Answer tag1 Ack)
        (Answer tag1(CoqExn()()(Backtrace())(NoSuchState 0)))
        (Answer tag1 Completed)
        '''
        self.assertEqual(True,True) #TODO

if __name__ == '__main__':
    unittest.main()
