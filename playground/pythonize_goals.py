from sexpdata import loads, dumps
from sexpdata import Symbol

from pdb import set_trace as st

import torch

D = 3
AI_REP = {}

# From names.mli
class Id(object):
    def __init__(self, sexp):
        self.value = sexp

    def __repr__(self):
        return self.value.__repr__()

    def embedding(self):
        embedding = AI_REP[self.sexp]
        return embedding

class Constant(object):
    def __init__(self, sexp):
        self.value = sexp # TODO: fixme

    def __repr__(self):
        return self.value.__repr__()

    def embedding(self):
        embedding = AI_REP[self.value]
        return embedding

class Inductive(object):
    def __init__(self, sexp):
        self.mutind = KerPair(sexp[0])
        self.idx = sexp[1] #int

    def __repr__(self):
        return "Inductive " + self.idx.__repr__()

def KerPair(object):
    def __init__(self, sexp):
        super().__init__(sexp)
        self.name = sexp[1]
        #self.universes = sexp[2]

    def __repr__(self):
        return "Inductive " + self.idx.__repr__()

# From constr.mli
class Constr(object):
    def __init__(self, sexp):
        self.sexp = sexp

    def __repr__(self):
        return self.sexp.__repr__()

    def embedding(self):
        print(f'\nself.sexp = {self.sexp}')
        if self.sexp not in AI_REP:
            embedding = torch.rand(D,1)
            AI_REP[self.sexp] = embedding
        else:
            embedding = AI_REP[self.sexp]
        return embedding

class Ind(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        #print(f'---> sexp = {sexp}')
        self.inductive = Inductive(sexp[1][0])
        self.universes = sexp[1][1]

    def __repr__(self):
        return "Ind " + self.inductive.__repr__()

class Rel(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        self.idx = int(sexp[1])

    def __repr__(self):
        return "Rel " + self.idx.__repr__()

class Var(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        self.var = Id(sexp[1])

    def __repr__(self):
        return "Var " + self.var.__repr__()

    def embedding(self):
        embedding = self.var.embedding()
        return embedding

class Prod(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        # Todo
        # self.binder = list(map(...,sexp[0]))
        self.binder_type = build_obj(sexp[1])
        self.body = build_obj(sexp[2])

    def __repr__(self):
        return "Prod "

class Lambda(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        # Todo
        # self.binder = list(map(...,sexp[0]))
        self.binder_type = build_obj(sexp[1])
        self.body = build_obj(sexp[2])

    def __repr__(self):
        return "Lambda "

class App(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        self.head = build_obj(sexp[1])
        self.args = list(map(build_obj, sexp[2]))

    def __repr__(self):
        return "App " + self.head.__repr__() + "@" + self.args.__repr__()

    def embedding(self):
        embedding_head = self.head.embedding() # [0.3, ...., 1.8]
        args_embeddings = []
        for arg in self.args:
            arg_embedding = arg.embedding()
            args_embeddings.append( arg_embedding )
        return args_embeddings

class Const(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        self.constant = Constant(sexp[1])
        self.univs = []

    def __repr__(self):
        return "Const "

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

    def __repr__(self):
        str_repr = ''
        for name_id in self.names:
            str_repr = str_repr + f'NAME_ID: {str(name_id)} \n'
        str_repr = str_repr + f'BODY: {str(self.body)} \n'
        str_repr = str_repr + f'TYPE: {str(self.type)} \n'
        return str_repr

class Goal:
    def __init__(self,sexp):
        ## store name
        self.name = sexp[0][1]
        ## store type
        ty_array = sexp[1] # [Symbol('ty'), [...type...] ]
        ty = ty_array[1] # [...type...] e.g. [Symbol('App'), ... ]
        self.ty = build_obj(ty)
        ## store hypothsis/local proof
        hyp_array = sexp[2] # [Symbol('hyp') , [...hyp...] ]
        hyps = hyp_array[1] # [...hyp...] e.g. [[[Symbol('Id'), Symbol('n') ]], ...]
        self.hyp = []
        for hyp in hyps:
            hyp = Hyp(hyp)
            self.hyp.append( hyp )

    def __repr__(self):
        str_repr = f'NAME: {str(self.name)} \n'
        str_repr = str_repr + f'TY: {str(self.ty)} \n'
        for hyp in self.hyp:
            str_repr = str_repr + f'HYP: {str(hyp)} \n'
        return str_repr

class Goals:
    def __init__(self,sexp):
        ''' Create Goals object with all information about goals.

        Assumes it receives all_goals = [ fg_goals ..., bg_goals ..., shelved_goals ..., given_up_goals ...]
        '''
        ## process fg_goals
        fg_goals = sexp[0] # [ fg_goals ...]
        self.fg_goals = []
        fg_goals = fg_goals[1] # list of fg_goals
        for goal in fg_goals:
            self.fg_goals.append( Goal(goal) )
        #TODO bg_goals ..., shelved_goals ..., given_up_goals
        bg_goals = sexp[1]
        shelved_goals = sexp[2]
        given_up_goals = sexp[3]

    def __repr__(self):
        str_repr = ''
        for goal in self.fg_goals:
            str_repr = str_repr + '\n' + str(goal)
        return str_repr

def build_obj_old(sexp):
    if isinstance(sexp, str):
        return Constr(sexp)
    term_key = sexp[0]
    if term_key in globals():
        return (globals()[term_key](sexp))
    else:
        return Constr(sexp)

def build_obj(sexp):
    if isinstance(sexp, str):
        return Constr(sexp)
    term_key = sexp[0]
    term_key = term_key._val if type(term_key) == Symbol else term_key
    ## create appropriate Constr/Coq term
    if term_key in globals():
        constructor = globals()[term_key]
        coq_term = constructor(sexp)
        return coq_term
    else:
        return Constr(sexp)
####

def pythonize_something():
    '''

    '''
    ##
    '''
    1 subgoal (ID 10)

      n : nat
      ============================
      0 + n = n
    '''
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
    psexp = loads(sexp)
    print(psexp)
    print()
    all_goals = psexp[2][1][0][1] # [ fg_goals ..., bg_goals ..., shelved_goals ..., given_up_goals ...]
    print(f'all_goals[0]={all_goals[0]}\nall_goals[1]={all_goals[1]}\nall_goals[2]={all_goals[2]}\nall_goals[3]={all_goals[3]}\n')
    print('----')
    all_goals = Goals(all_goals)
    print(f'all_goals = {all_goals}')
    print('\n\n\n----')
    print(f'all_goals.fg_goals.ty = {all_goals.fg_goals[0].ty}')
    embedding = all_goals.fg_goals[0].ty.embedding()
    print(f'embedding = {embedding}')

if __name__ == '__main__':
    print('Running MAIN')
    pythonize_something()
