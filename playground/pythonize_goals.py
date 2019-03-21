# From names.mli
class Id(object):
    def __init__(self, sexp):
        self.value = sexp

    def __repr__(self):
        return self.value.__repr__()

# XXX: fixme
class Constant(object):
    def __init__(self, sexp):
        self.value = sexp

    def __repr__(self):
        return self.value.__repr__()

# From constr.mli
class Constr(object):
    def __init__(self, sexp):
        self.sexp = sexp

    def __repr__(self):
        return self.sexp.__repr__()

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

class Const(Constr):
    def __init__(self, sexp):
        super().__init__(sexp)
        self.constant = Constant(sexp[1])
        self.univs = []

    def __repr__(self):
        return "Const "

def build_obj(sexp):

    if isinstance(sexp, str):
        return Constr(sexp)

    term_key = sexp[0]
    # print(f'term_key = {term_key}')

    if term_key in globals():
        return (globals()[term_key](sexp))
    else:
        return Constr(sexp)
