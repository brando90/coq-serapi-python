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

'''
Pseudo-code:

-run process
-then its in the background waiting for a command to be received.
-then my script decides to send a command.
1) p.send_command(cmd).
-then wait until the command is fully executed and the full response is written
    somewhere for the python script to read.
2) output = p.read_fully_the_cmd_output()
-then do stuff with output, repeat when the next time we need to execute a command
'''

def make_sure_serapi_receives_command_fine():
    '''
    first make sure that the command is received and we can make sure the
    command was received by checking the output (even if it deadlocks)
    '''
    proc = subprocess.Popen(['sertop'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    # send command to sertop
    proc.stdin.write(b'(Add () \"Example test_oddb1: Nat.odd 1 = true.\")\n')
    proc.stdin.flush()
    # read intro strings AND check that the real command was received
    for line in proc.stdout:
        #print('--- NEW LINE')
        print()
        print(line)

def make_sure_serapi_receives_command_fine_NO_DEADLOCK():
    '''
    TODO: fix deadlock
    '''
    proc = subprocess.Popen(['sertop'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

if __name__ == '__main__':
    print('Running main')
    make_sure_serapi_receives_command_fine()
