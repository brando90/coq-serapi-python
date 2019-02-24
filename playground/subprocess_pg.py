import subprocess

'''
Goal:

(Add () "Example test_oddb1: Nat.odd 1 = true.")
(Exec 2)
(Query () Goals)
(Query ((pp((pp_format PpStr)))) Goals)
(Add () "reflexivity.")
(Exec 4)
(Add () "Qed.")

'''

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
    '''
    https://stackoverflow.com/questions/16768290/understanding-popen-communicate
    '''
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
    '''
    (Add () "Example test_oddb1: Nat.odd 1 = true.")

    (Answer 0 Ack)
    (Answer 0(Added 2((fname ToplevelInput)(line_nb 1)(bol_pos 0)(line_nb_last 1)(bol_pos_last 0)(bp 0)(ep 37))NewTip))
    (Answer 0 Completed)
    '''
    comm = proc.communicate('(Add () "Example test_oddb1: Nat.odd 1 = true.")')
    print(comm)

def serapi_continuous_communication():
    '''
    https://stackoverflow.com/questions/19880190/interactive-input-output-using-python
    '''
    #p = subprocess.Popen(['sertop'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    p = subprocess.Popen(['python'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    # get output from process "Something to print"
    #one_line_output = p.stdout.readline()
    #print(one_line_output)
    for line in p.stdout:
        print(line)

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
    #serapi_attempt1()
    serapi_continuous_communication()

print('end of main')
