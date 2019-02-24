import subprocess

def simple():
    # Simple command
    #output = subprocess.call(['ls', '-1'], shell=True)
    output = subprocess.check_output(['ls', '-1'])
    print(f'output: {output}')
    ##
    #output = subprocess.call('echo $HOME', shell=True)
    #print(f'output echo $HOME = {output}')

def popen_pg():
    ##
    proc = subprocess.Popen(['echo', '"to stdout"'],
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE
                        )
    print(proc)
    ##
    stdout_value = proc.communicate()[0]
    print('\tstdout:', repr(stdout_value))


def serapi_attempt1():
    ##
    proc = subprocess.Popen(['sertop'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    #proc = subprocess.Popen(['sertop'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,)
    print(proc)
    comm = proc.communicate()
    print('\n---information about calling comm')
    print(type(comm))
    print(len(comm))
    print('\n---stdout_data')
    print(comm[0])
    print(type(comm[0]))
    print('\n---stderror_data')
    print(comm[1])
    print(type(comm[0]))
    ##
    #stdout_value = proc.communicate()[0]
    #print('\tstdout:', repr(stdout_value))

def context_manager():
    with subprocess.Popen(['sertop'],stdout=subprocess.PIPE) as proc:
        print(f'type(proc)={type(proc)}')
        print(f'proc={proc}')
        #stdout_value = proc.communicate()[0]
        #print('\tstdout:', repr(stdout_value))

if __name__ == '__main__':
    print('running main')
    #attempt1()
    #context_manager()
    #popen_pg()
    serapi_attempt1()

#(Sys_error"Input/output error")
##
print('end of main')
