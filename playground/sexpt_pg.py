from sexpdata import loads, dumps

def pythonize_something():
    '''
    (Answer 0 Ack)
    (Answer 0(CoqExn()()(Backtrace())(NoSuchState 0)))
    (Answer 0 Completed)
    '''
    sexp1 = '(Answer 0 Ack)'
    p_sexp1 = loads(sexp1) # [Symbol('Answer'), 0, Symbol('Ack')]
    print(p_sexp1)
    print(p_sexp1[0])
    print(type(p_sexp1[0]))
    ##
    print()
    sexp2 = '(Answer 0(CoqExn()()(Backtrace())(NoSuchState 0)))'
    p_sexp2 = loads(sexp2) # [Symbol('Answer'), 0, [Symbol('CoqExn'), [], [], [Symbol('Backtrace'), []], [Symbol('NoSuchState'), 0]]]
    print(p_sexp2)
    print(p_sexp2[0])
    print(type(p_sexp2[0]))
    #
    answer = p_sexp2[0]
    print(answer)
    print( str(answer) )
    print( str(answer) == 'Answer' )

if __name__ == '__main__':
    pythonize_something()
