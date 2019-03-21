from sexpdata import loads, dumps
from sexpdata import Symbol

## https://github.com/coq/coq/blob/96c9b16f03ef6898b575a0cc78470f0fa86fd2e4/kernel/constr.mli#L207

class Constr:
    # just a Coq term

    def __init__(self,sexp):
        self.sexp = sexp
        if sexp[0] == Symbol('App'):
            print(len((sexp[1],sexp[2])))
            #print(App.__init__(sexp[1],sexp[2]))
            #print( App(sexp[1],sexp[2]) )
            #self = App.__init__(sexp[1],sexp[2])

    def print(self):
        print(f'self.sexp = {self.sexp}')

    def __repr__(self):
        return f'self.sexp = {self.sexp}'

    def constants(self):
        return []

def App(Constr):

    def __init__(self,head,args):
        self.head = Constr(head)
        self.args = [ Constr(arg) for arg in args]

    def __repr__(self):
        str_repr = str(self.head)
        for arg in args:
            str_repr = str_repr + ' , '+ str(arg)
        return str_repr

    def constants(self):
        # concatenation of head constants
        constants = self.head.constants()
        for arg in self.args:
            constants = constants + arg.constant()
        return constants

class Hyp:

    def __init__(self,sexp):
        ##
        '''
        nested arrays, [ name hypothesis (list identifiers),
            optional element empty list or list with 1 element constr,
             mandatory constr]
        '''
        self.names = [ Id(name) for name in sexp[0] ] # list of Ids
        if len(sexp[1]) == 0:
            self.body =  None
        else:
            self.body = Constr(sexp[1][0])
        self.type = Constr(sexp[2])

    def print(self):
        print('Hyp')
        print(f'self.names = {self.names}')
        self.type.print()

class Id:

    def __init__(self,symbol):
        self.symbol = symbol # its string

    def __repr__(self):
        return str(self.symbol)

class Goal:

    def __init__(self,sexp):
        #print(f'sexp = {sexp}')
        #sexp = sexp[0]
        #print(f'sexp[0][1] = {sexp[0]}')
        self.name = sexp[0][1]
        self.ty = Constr(sexp[1][1])
        #print(f'sexp[2] = {sexp[2]}')
        self.hyp = [ Hyp(hyp) for hyp in sexp[2][1] ]

    def print(self):
        print('INSIDE PRINT GOAL')
        print(f'self.name = {self.name}')
        #print(f'self.ty = {self.ty}')
        print('self.ty')
        self.ty.print()
        print('self.hyp')
        #print(f'self.hyp = {self.hyp}')
        for hyp in self.hyp:
            hyp.print()
        print('DONE PRINT GOAL')

class Goals:

    def __init__(self,sexp):
        print(sexp[0][1])
        self.fg_goals = [ Goal(goal) for goal in sexp[0][1] ]
        print(f'self.fg_goals[0] = {self.fg_goals[0].name}')
        #TODO other goals later

    def print(self):
        print('INSIDE GOALS')
        #print(self.fg_goals)
        for fg_goal in self.fg_goals:
            print(f'current fg_goal = {fg_goal}')
            fg_goal.print()
        print('DONE GOALS')

####

def pythonize_something():
    '''

    '''
    ##
    sexp = '''
        (Answer 2
         (ObjList
          ((CoqGoal
            ((fg_goals
              (((name 4)
                (ty
                 (App
                  (Ind
                   (((Mutind (MPfile (DirPath ((Id Logic) (Id Init) (Id Coq))))
                      (DirPath ()) (Id eq))
                     0)
                    (Instance ())))
                  ((Ind
                    (((Mutind (MPfile (DirPath ((Id Datatypes) (Id Init) (Id Coq))))
                       (DirPath ()) (Id nat))
                      0)
                     (Instance ())))
                   (App
                    (Const
                     ((Constant (MPfile (DirPath ((Id Nat) (Id Init) (Id Coq))))
                       (DirPath ()) (Id add))
                      (Instance ())))
                    ((Construct
                      ((((Mutind
                          (MPfile (DirPath ((Id Datatypes) (Id Init) (Id Coq))))
                          (DirPath ()) (Id nat))
                         0)
                        1)
                       (Instance ())))
                     (Var (Id n))))
                   (Var (Id n)))))
                (hyp
                 ((((Id n)) ()
                   (Ind
                    (((Mutind (MPfile (DirPath ((Id Datatypes) (Id Init) (Id Coq))))
                       (DirPath ()) (Id nat))
                      0)
                     (Instance ())))))))))
             (bg_goals ()) (shelved_goals ()) (given_up_goals ()))))))
    '''
    print(sexp)
    #print(sexp)
    psexp = loads(sexp)
    fg_goals = psexp[2][1][0][1]
    fg_goals = Goals(fg_goals)
    # we can probably get to ty using BFS, how to traverse hyp?
    # this reaches `ty`, the current goal
    fg_goals.print()

if __name__ == '__main__':
    pythonize_something()
