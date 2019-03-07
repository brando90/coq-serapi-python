import subprocess

import pdb

class Coq:
    # docstrings according to https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    # function_with_types_in_docstring
    def __init__(self, debug=False):
        '''Constructor for the Coq API class that talks to Coq.

        1) run a serapi instance in the background
        2) send Coq commands to the running instance of serapi
        3) get responses and do stuff
        Protocol mli file: https://github.com/brando90/coq-serapi-python/blob/python-api/serapi/serapi_protocol.mli

        Args:
            debug (bool): True when in debugging state.
        '''
        ## start serapi, TODO: --no_init flag, think about how to use feedback for ML better
        self.serapi = subprocess.Popen(['sertop','--no_init'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.debug = debug

    def run_command(self, cmd):
        ''' Runs the raw command command cmd given.

        Args:
            cmd (str): command as a string.
        '''
        ## send command fully to serapi
        self._send_command(cmd)
        ## get results of command
        result = self._get_result()
        return result

    ## COMMANDS: https://github.com/brando90/coq-serapi-python/blob/d394050372b6ab680fda2680d6e4ba53fdabb875/serapi/serapi_protocol.mli#L212

    def new_doc(self, cmd):
        '''
        TODO
        '''
        return

    def add(self, text, tag=None):
        ''' Executes the Add command with the given text (and tag).

        Args:
            text (str): text for Coq proof script.
            tag (text): text for tag.
        '''
        cmd = f"( Add () \"{text}\")"
        if tag:
            cmd = add_tag(cmd)
        ##
        result = self.run_command(cmd)
        return result

    def _send_command(self,cmd):
        ''' Sends command to be executed to serapi.

        Args:
            cmd (str): command text for serapi. e.g. cmd = '( Add () "Example test_oddb1: Nat.odd 1 = true.")'
        '''
        cmd = bytes(cmd,'utf-8')
        # send command to serapi
        self.serapi.stdin.write(cmd)
        # pushes things to the actual file serapi reads rather than keep it in the buffer
        self.serapi.stdin.flush()

    def _get_result(self):
        ''' Get the result from the last command executed.

        Args:
            result (list): list of s-expressions from the command result.
        '''
        ## process result of command
        completed_getting_results = False
        result = []
        # extract the whole command result from the buffer (separated by \n)
        while not completed_getting_results: # while searching for completed tag command
            line = self.serapi.stdout.readline()
            if self.debug:
                print(f'-> line={line}')
            current_result_sexpt = pythonize_sexpt(sexpt=line)
            result.append(current_result_sexpt)
            ## if complete tag found then we don't need to keep reading from serapi
            completed_getting_results = "Completed" in str(line)
        return result

## utils

def add_tag(tag,cmd):
    ''' Adds the given tag to the command.

    Args:
        tag (str): tag for command e.g. 'tag1' in '( tag1 (Add () "Example test_oddb1: Nat.odd 1 = true.") )'
        cmd (str): coq serapi command '(Add () "Example test_oddb1: Nat.odd 1 = true.")'
    '''
    tagged_command = f"( {tag} {cmd} )"
    return tagged_command

def pythonize_sexpt(sexpt):
    '''
        TODO: convert sexpt to python object

        https://github.com/ocaml-ppx/ppx_deriving_yojson
    '''
    pythonixed_sexpt = str(sexpt)
    ##

    return pythonixed_sexpt
