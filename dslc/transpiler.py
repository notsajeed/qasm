import re
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Built-in macros
# -----------------------------
def measure_macro(args):
    if args == ['all']:
        return 'measure q -> c;'
    elif len(args) == 2:
        return f'measure {args[0]} -> {args[1]};'
    else:
        return f'// Invalid measure args: {args}'

def ghz_macro(args):
    if len(args) < 2:
        return '// GHZ requires at least 2 qubits'
    lines = [f'h {args[0]};']
    for target in args[1:]:
        lines.append(f'cx {args[0]},{target};')
    return lines

# -----------------------------
# Macro map
# -----------------------------
MACRO_MAP = {
    # Single-qubit gates
    'h': ['h {0};'],
    'x': ['x {0};'],
    'y': ['y {0};'],
    'z': ['z {0};'],
    's': ['s {0};'],
    't': ['t {0};'],
    'sdg': ['sdg {0};'],
    'tdg': ['tdg {0};'],

    # Two-qubit gates
    'cx': ['cx {0},{1};'],
    'cz': ['cz {0},{1};'],
    'swap': ['swap {0},{1};'],

    # External macros (parameterized .inc files)
    'bell': os.path.join(ROOT_DIR, 'macros', 'bell.inc'),
    'oracle11': os.path.join(ROOT_DIR, 'macros', 'oracle.inc'),
    'ghz': ghz_macro,  # built-in variable-length macro

    # Measurement
    'measure': measure_macro,
    'measure all': ['measure q -> c;']
}

# -----------------------------
# Helper functions
# -----------------------------
def qubit_to_index(qubit_name):
    """Convert qubit/classical names to QASM format"""
    if qubit_name.startswith('q'):
        return f"q[{qubit_name[1:]}]"
    if qubit_name.startswith('c'):
        return f"c[{qubit_name[1:]}]"
    return qubit_name

def load_macro_file(file_path, args):
    """Load external macro file and replace placeholders {0},{1},..."""
    if not os.path.isfile(file_path):
        return [f'// Macro file not found: {file_path}']

    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            # Handle placeholder {cx_lines} for GHZ-style macros if present
            if '{cx_lines}' in line:
                if len(args) < 2:
                    lines.append('// Not enough qubits for cx_lines')
                    continue
                cx_lines = [f'cx {args[0]},{q};' for q in args[1:]]
                line = line.replace('{cx_lines}', '\n'.join(cx_lines))
                lines.extend(line.split('\n'))
                continue
            try:
                lines.append(line.format(*args))
            except IndexError:
                lines.append(f'// Invalid args for macro line: {line} with args {args}')
    return lines

# -----------------------------
# Main transpiler
# -----------------------------
def transpile(commands):
    qasm_lines = ['OPENQASM 2.0;', 'include "qelib1.inc";']

    for cmd in commands:
        cmd = cmd.strip()
        if not cmd or cmd.startswith('#'):
            continue

        # Registers
        if cmd.startswith('qubits'):
            n = int(cmd.split()[1])
            qasm_lines.append(f'qreg q[{n}];')
            continue
        if cmd.startswith('cregs'):
            n = int(cmd.split()[1])
            qasm_lines.append(f'creg c[{n}];')
            continue

        # Include statements
        if cmd.startswith('include'):
            qasm_lines.append(cmd + ';')
            continue

        # Split command and arguments
        parts = cmd.split()
        name = parts[0]
        args = []
        if len(parts) > 1:
            args = [qubit_to_index(a.strip()) for a in re.split('[, ]', ' '.join(parts[1:])) if a]

        # Handle macros
        if name in MACRO_MAP:
            macro = MACRO_MAP[name]
            if callable(macro):
                result = macro(args)
                if isinstance(result, list):
                    qasm_lines.extend(result)
                else:
                    qasm_lines.append(result)
            elif isinstance(macro, str):
                # External macro file
                qasm_lines.extend(load_macro_file(macro, args))
            else:  # list of QASM lines
                for line in macro:
                    try:
                        qasm_lines.append(line.format(*args))
                    except IndexError:
                        qasm_lines.append(f'// Invalid args for {name}: {args}')
        else:
            qasm_lines.append('// Unknown command: ' + cmd)

    return '\n'.join(qasm_lines)

