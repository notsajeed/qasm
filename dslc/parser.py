import re

def parse_dsl(file_path):
    """
    Reads DSL file and returns a list of commands.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    commands = []
    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        commands.append(line)
    return commands
