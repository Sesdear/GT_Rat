import paramiko


def send_command_ssh(host, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    ssh.close()
    return output

if __name__ == "__main__":
    host = "remote_host_ip"
    port = 22
    username = "your_username"
    password = "your_password"
    command = input("Введите команду для отправки: ")
    output = send_command_ssh(host, port, username, password, command)
    print("Результат выполнения команды:", output)