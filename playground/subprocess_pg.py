import subprocess

import pdb

'''
Goal:

(Add () "Example test_oddb1: Nat.odd 1 = true.")
(Exec 0)
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
    WORKS

    first make sure that the command is received and we can make sure the
    command was received by checking the output (even if it deadlocks)
    '''
    proc = subprocess.Popen(['sertop'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    # send command to sertop
    proc.stdin.write(b'(Add () \"Example test_oddb1: Nat.odd 1 = true.\")\n')
    proc.stdin.flush() # I think it pushes things to the actual file rather than keep it in buffer
    # read intro strings AND check that the real command was received
    for line in proc.stdout:
        #print('--- NEW LINE')
        print()
        print(line)

def make_sure_serapi_receives_command_fine_NO_DEADLOCK_Queue_Soln():
    '''
    TODO: fix deadlock, this still doesn't work, I can't see any output for some reason, despite me trying to flush it

    by continuously reading from Queue.
    https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
    '''
    print('make_sure_serapi_receives_command_fine_NO_DEADLOCK_Queue_Soln')
    ##
    # sertop = SerapiAPI()
    # sertop.process_intro_msg()
    ## Queue version
    import sys
    from subprocess import PIPE, Popen
    from threading  import Thread
    from queue import Queue, Empty

    # checks if its on a Portable Operating System Interface
    ON_POSIX = 'posix' in sys.builtin_module_names

    # TODO: why do I need this?
    def enqueue_output(out, queue):
        '''
        intention:
            out=p.stdout
            queueue=instance of Queue()
        '''
        #TODO: why does this not need a flush?
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()
        ##
        # while True: # while there are new lines to read put them in the queue
        #     out.flush()
        #     line = out.readline()
        #     queue.put(line)
        return
    ##
    p = Popen(['sertop'], stdout=PIPE,stdin=PIPE,stderr=PIPE, close_fds=ON_POSIX)
    q = Queue()
    # TODO: when is p.stdout.flush being called...?
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True # thread dies with the program
    t.start()
    # trim the beginning
    trimming = True
    while trimming:
        try:
            line = q.get_nowait() # or q.get(timeout=.1)
            print(f'line={line}')
        except Empty:
            trimming = False
    # read the new command sent to sertop
    #p.stdin.write(b'(Add () \"Example test_oddb1: Nat.odd 1 = true.\")\n')
    #p.stdin.flush()
    #print(f'output from ADD command: line={q.get_nowait()}')
    return

def make_sure_serapi_receives_command_fine_NO_DEADLOCK():
    '''
    TODO: fix deadlock

    by just reading until the command response is done
    '''
    #
    p = subprocess.Popen(['sertop'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    # send command to sertop
    p.stdin.write(b'(Add () \"Example test_oddb1: Nat.odd 1 = true.\")\n')
    p.stdin.flush() # I think it pushes things to the actual file rather than keep it in buffer
    ##
    reading_command = True
    while reading_command: # while reading for completed command
        line = str(p.stdout.readline())
        print(line)
        reading_command = not ('Completed' in line) # if completed then we don't need to keep reading

if __name__ == '__main__':
    print('Running main')
    #make_sure_serapi_receives_command_fine() ## PASSED
    #make_sure_serapi_receives_command_fine_NO_DEADLOCK_Queue_Soln() ## TODO
    make_sure_serapi_receives_command_fine_NO_DEADLOCK()
