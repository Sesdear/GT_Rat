###################
### Клиент < Сервер

import subprocess
import os



def send_command(command):

    command_operator = command.split()[0]
    command_text = ' '.join(command.split()[1:])
    print(f'Operator: {command_operator}')
    print(f'Text: {command_text}\n')

    if command_operator == "bash":
        print(f"Command send: {command_text}")
        process = subprocess.Popen(command_text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # Read output and error messages line by line
        print("Output:")
        for line in process.stdout:
            print(line, end="")
        print("Error:")
        for line in process.stderr:
            print(line, end="")
    else:
        print("Invalid operator")

command = input()
send_command(command)



