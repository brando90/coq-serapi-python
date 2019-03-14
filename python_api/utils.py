from sexpdata import loads, dumps

from pdb import set_trace as st

def pythonize_sexpt(sexpt):
    '''
        TODO: convert sexpt to python object

        https://github.com/ocaml-ppx/ppx_deriving_yojson
    '''
    #pythonixed_sexpt = str(sexpt)
    pythonixed_sexpt = loads(sexpt)
    ##
    return pythonixed_sexpt
