def parse(command):
    comp_uuid: bytes = command.split()[0]
    command_text: bytes = command.split()[1]
    return (comp_uuid.decode("utf-8"), command_text.decode('utf-8'))
