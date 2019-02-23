import subprocess

def attempt1():
    #p = subprocess.Popen(['rlwrap', 'sertop', '--printer=human'])
    p = subprocess.Popen(['sertop'])
    #print(p)
    #print(f'type(p)={type(p)}')
    #print(f'p={p}')

def context_manager():
    with subprocess.Popen(['sertop']):
        print(f'type(p)={type(p)}')
        print(f'p={p}')

if __name__ == '__main__':
    attempt1()

#(Sys_error"Input/output error")
