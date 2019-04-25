from sexpdata import loads, dumps

def buffer_encoding_test():
    print('buffer_encoding_test')
    sexp = b'(Answer 3(ObjList((CoqGoal((fg_goals(((name 3)(ty(Prod(Name(Id n))(Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Ind(((Mutind(MPfile(DirPath((Id Logic)(Id Init)(Id Coq))))(DirPath())(Id eq))0)(Instance())))((Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Const((Constant(MPfile(DirPath((Id Nat)(Id Init)(Id Coq))))(DirPath())(Id add))(Instance())))((Construct((((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)1)(Instance())))(Rel 1)))(Rel 1)))))(hyp()))))(bg_goals())(shelved_goals())(given_up_goals()))))))\n'
    sexp = sexp.decode("utf-8")
    print(f'sexp = {sexp}')
    psexp = loads(sexp)

def buffer_test():
    print('buffer_test')
    sexp = ''' b'(Answer 3(ObjList((CoqGoal((fg_goals(((name 3)(ty(Prod(Name(Id n))(Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Ind(((Mutind(MPfile(DirPath((Id Logic)(Id Init)(Id Coq))))(DirPath())(Id eq))0)(Instance())))((Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Const((Constant(MPfile(DirPath((Id Nat)(Id Init)(Id Coq))))(DirPath())(Id add))(Instance())))((Construct((((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)1)(Instance())))(Rel 1)))(Rel 1)))))(hyp()))))(bg_goals())(shelved_goals())(given_up_goals()))))))\n'
    '''
    print(f'sexp = {sexp}')
    psexp = loads(sexp)

def buffer_str_test():
    print('buffer_str_test')
    sexp = str(''' b'(Answer 3(ObjList((CoqGoal((fg_goals(((name 3)(ty(Prod(Name(Id n))(Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Ind(((Mutind(MPfile(DirPath((Id Logic)(Id Init)(Id Coq))))(DirPath())(Id eq))0)(Instance())))((Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Const((Constant(MPfile(DirPath((Id Nat)(Id Init)(Id Coq))))(DirPath())(Id add))(Instance())))((Construct((((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)1)(Instance())))(Rel 1)))(Rel 1)))))(hyp()))))(bg_goals())(shelved_goals())(given_up_goals()))))))\n'
    ''')
    print(f'sexp = {sexp}')
    psexp = loads(sexp)

def str_str_test():
    print('str_str_test')
    sexp = str(''' (Answer 3(ObjList((CoqGoal((fg_goals(((name 3)(ty(Prod(Name(Id n))(Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Ind(((Mutind(MPfile(DirPath((Id Logic)(Id Init)(Id Coq))))(DirPath())(Id eq))0)(Instance())))((Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Const((Constant(MPfile(DirPath((Id Nat)(Id Init)(Id Coq))))(DirPath())(Id add))(Instance())))((Construct((((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)1)(Instance())))(Rel 1)))(Rel 1)))))(hyp()))))(bg_goals())(shelved_goals())(given_up_goals()))))))\n'
    ''')
    print(f'sexp = {sexp}')
    psexp = loads(sexp)

def str_test():
    print('str_test')
    sexp = ''' (Answer 3(ObjList((CoqGoal((fg_goals(((name 3)(ty(Prod(Name(Id n))(Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Ind(((Mutind(MPfile(DirPath((Id Logic)(Id Init)(Id Coq))))(DirPath())(Id eq))0)(Instance())))((Ind(((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)(Instance())))(App(Const((Constant(MPfile(DirPath((Id Nat)(Id Init)(Id Coq))))(DirPath())(Id add))(Instance())))((Construct((((Mutind(MPfile(DirPath((Id Datatypes)(Id Init)(Id Coq))))(DirPath())(Id nat))0)1)(Instance())))(Rel 1)))(Rel 1)))))(hyp()))))(bg_goals())(shelved_goals())(given_up_goals()))))))'
    '''
    print(f'sexp = {sexp}')
    psexp = loads(sexp)

if __name__ == '__main__':
    print('running main')
    buffer_encoding_test()
    #buffer_test()
    #buffer_str_test()
    #str_str_test()
    #str_test()
    print('sucessful main')
