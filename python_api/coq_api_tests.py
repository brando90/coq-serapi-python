import unittest

import coq_api

class TestStringMethods(unittest.TestCase):

    def __init__(self):
        self.coq = coq_api.coq()

    def test_add(self):
        '''
        Testing the following:

        (Add () "Example test_oddb1: Nat.odd 1 = true.")

        (Answer 0 Ack)
        (Answer 0(CoqExn()()(Backtrace())(NoSuchState 0)))
        (Answer 0 Completed)
        '''
        self.coq.add("Example test_oddb1: Nat.odd 1 = true.")
        self.assertEqual('foo'.upper(), 'FOO')

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
