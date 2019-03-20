from sexpdata import loads, dumps

def pythonize_something():
    '''

    '''
    sexp1 = '(Answer 0 Ack)'
    p_sexp1 = loads(sexp1) # [Symbol('Answer'), 0, Symbol('Ack')]
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
        (Answer 2 Completed)
    '''
    #print(sexp)
    psexp = loads(sexp)
    print(psexp)
    print()
    fg_goals = psexp[2][1][0][1][0][1][0][1]
    # we can probably get to ty using BFS, how to traverse hyp?
    # this reaches `ty`, the current goal
    print(fg_goals)

if __name__ == '__main__':
    pythonize_something()
