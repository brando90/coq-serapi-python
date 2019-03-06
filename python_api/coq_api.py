import subprocess

class coq:
    def __init__(self):
        '''
        1) run a serapi instance in the background
        2) send Coq commands to the runnign instance of serapi
        3) get responses and do stuff

        Protocol mli file: https://github.com/brando90/coq-serapi-python/blob/python-api/serapi/serapi_protocol.mli
        '''
        ## start serapi, TODO: --no_init flag, think about how to use feedback for ML better
        self.serapi = subprocess.Popen(['sertop','--no_init'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

  def run_command(cmd):
      '''
      TODO
      '''
      return

  def newdoc(self, action):
      '''
      TODO
      '''

  def add(self, text, tag=None):
      '''
      '''
      cmd = f" (Add () \"{text}\") "
      if tag:
          cmd = add_tag(tag,cmd)

        p.stdin.write(b)
        p.stdin.flush() # it pushes things to the actual file rather than keep it in the buffer
        return



## utils

def add_tag(tag,cmd):
    return f"( {tag} {cmd} )"


if __name__ == '__main__':
