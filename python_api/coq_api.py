import subprocess

class Coq:
    def __init__(self, debug=False):
        '''
        1) run a serapi instance in the background
        2) send Coq commands to the runnign instance of serapi
        3) get responses and do stuff

        Protocol mli file: https://github.com/brando90/coq-serapi-python/blob/python-api/serapi/serapi_protocol.mli
        '''
        ## start serapi, TODO: --no_init flag, think about how to use feedback for ML better
        self.serapi = subprocess.Popen(['sertop','--no_init'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.debug = debug

    def run_command(self, cmd):
        ## send command
        self._send_command(cmd)
        ## get results of command
        results = self._get_results()
        return

    def new_doc(self, cmd):
        return

    def add(self, cmd, tag=None):
        cmd = f"( Add () \"{text}\")"
        if tag:
            cmd = add_tag(cmd)
        ##
        result = self.run_command(cmd)
        return

    def _send_command(cmd):
        '''
        '''
        self.stdin.write(cmd)
        self.stdin.flush(cmd)

    def _get_results(self):
        '''
        '''
        ## process result of command
        completed_getting_results = False
        results = []
        while not completed_getting_results: # while searching for completed tag command
            line = self.serapi.stdout.readline()
            if self.debug:
                print(f'line={line}')
            current_result = pythonize_sexpt(sexpt=line)
            results.append(current_result)
            ## if complete tag found then we don't need to keep reading from serapi
            completed_getting_results = 'Completed' in line
        return results

## utils

def add_tag(tag,cmd):
    return f"( {tag} {cmd} )"

def pythonize_sexpt(sexpt):
    '''
        TODO: convert sexpt to python object
    '''
    return str(sexpt)

if __name__ == '__main__':
