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

def context_manager():
    with subprocess.Popen(['sertop'],stdout=subprocess.PIPE) as proc:
        print(f'type(proc)={type(proc)}')
        print(f'proc={proc}')
        #stdout_value = proc.communicate()[0]
        #print('\tstdout:', repr(stdout_value))
    return

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

def serapi_continuous_communication_not_work():
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

def original_SO_example():
    fw = open("tmpout", "wb")
    fr = open("tmpout", "r")
    p = Popen("./a.out", stdin = PIPE, stdout = fw, stderr = fw, bufsize = 1)
    p.stdin.write("1\n")
    out = fr.read()
    p.stdin.write("5\n")
    out = fr.read()
    fw.close()
    fr.close()

def serapi_interactive_communication():
    '''
    TODO: make sure I can have interactivitity with SerAPI, send commands continuously

    https://stackoverflow.com/questions/19880190/interactive-input-output-using-python
    https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/4896288#4896288

    blocking readline: https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/4896288#4896288
    '''
    print('in  serapi_interactive_communication')
    # import os
    # try:
    #     os.remove('a.out')
    # except OSError:
    #     pass
    # f = open("a.out","w+")
    ##
    fw = open("tmpout", "wb")
    fr = open("tmpout", "r")
    frw = open("tmpout", "r+")
    p = subprocess.Popen(['python'],stdin=subprocess.PIPE,stdout=fw,stderr=fw,)
    #p = subprocess.Popen(['sertop'],stdin=subprocess.PIPE,stdout=frw,stderr=frw,)
    #p = subprocess.Popen("/Users/brandomiranda/home_simulation_research/coq-serapi-python/playground/a.out", stdin = subprocess.PIPE, stdout = fw, stderr = fw, bufsize = 1)
    #p = subprocess.Popen(['python'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    #p = Popen("./a.out", stdin=PIPE, stdout=fw, stderr=fw, bufsize=1)
    #p.stdin.write( bytes("(Add () \"Example test_oddb1: Nat.odd 1 = true.\")","utf-8") )
    #p.stdin.write( bytes("(Add () \"Example test_oddb1: Nat.odd 1 = true.\")","utf-8") )
    out = frw.readline()
    print(out)
    print(len(out))
    print(type(out))
    # p.stdin.write( "(Add () \"Example test_oddb1: Nat.odd 1 = true.\")" )
    #p.stdin.write( bytes("(Add () \"Example test_oddb1: Nat.odd 1 = true.\")", "utf-8") )
    p.stdin.write(  bytes('print(1)', 'utf-8') )
    out = fr.read()
    print(out)
    # for line in fr:
    #     print(line)
    return

def talk_to_python_interactively():
    '''
    https://stackoverflow.com/questions/19880190/interactive-input-output-using-python

    https://gist.github.com/brando90/99b10cdc73dc6b604ca661712c1c7b0d

    The interaction I want to implement:

    -run process
    then its in the background waiting for a command to be received
    -then my script decides to send a command.
    1) p.send_command(cmd)
    then wait until the command is fully executed and the full response is written somewhere for the python script to read
    2) output = p.read_fully_the_cmd_output()
    then do stuff with output, repeat when the next time we need to execute a command
    '''
    fw = open("tmpout", "wb")
    fr = open("tmpout", "r")
    p = subprocess.Popen(['python'],stdin=subprocess.PIPE,stdout=fw,stderr=fw,)
    out = frw.readline()
    print(out)
    print(len(out))
    print(type(out))
    p.stdin.write(  bytes('print(1)', 'utf-8') )
    out = fr.read()
    print(out) # prints nothing interesting

def send_command_test():
    '''
    TODO: make sure I can send commands to SerAPI and confirm it in python

    https://stackoverflow.com/questions/37601804/typeerror-string-argument-without-an-encoding-but-the-string-is-encoded?rq=1
    '''
    # make sure sending
    p = subprocess.Popen(['sertop'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    #out = p.stdout.readline()
    #print(out)
    p.stdin.write( bytes("(Add () \"Example test_oddb1: Nat.odd 1 = true.\")", "utf-8") )
    for line in p.stdout:
        print('--- NEW LINE')
        print(line)
    return

def tutorial_example():
    '''
    https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
    '''
    proc = subprocess.Popen(['python3', '-i'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    # To avoid deadlocks: careful to: add \n to output, flush output, use
    # readline() rather than read()
    #proc.stdin.write(b'2+2\n')
    proc.stdin.write(b'print(\'hello\')\n')
    proc.stdin.flush()
    print(proc.stdout.readline())

    proc.stdin.write(b'len("foobar")\n')
    proc.stdin.flush()
    print(proc.stdout.readline())

    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)
    return

def tutorial_example_to_serapi():
    '''
    https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
    To avoid deadlocks: careful to: add \n to output, flush output, use
    readline() rather than read()
    '''
    proc = subprocess.Popen(['sertop'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    ## remove the superflous part
    for line in proc.stdout:
        print('--- NEW LINE')
        proc.stdin.flush()
        print(line)
    print('FINISHED PROCESSING THE FIRST MSG')
    ## send command
    proc.stdin.write(b'(Add () \"Example test_oddb1: Nat.odd 1 = true.\")\n')
    proc.stdin.flush()
    #print(proc.stdout.readline())
    for line in proc.stdout:
        print('--- NEW LINE')
        print(line)
    ##
    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)
    return

if __name__ == '__main__':
    print('running main')
    #attempt1()
    #context_manager()
    #popen_pg()
    #serapi_attempt1()
    #serapi_interactive_communication()
    #send_command_test()
    #tutorial_example()
    tutorial_example_to_serapi()

print('end of main')
