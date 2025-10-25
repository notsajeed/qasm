MACRO_MAP = {
    'bell': ['h {0};', 'cx {0},{1};'],
    'superpos': ['h {0};'],
    'measure all': ['measure q -> c;']
}

def qubit_to_index(qubit_name):
    """
    Convert DSL qubit name like q0 -> q[0]
    """
    if qubit_name.startswith('q'):
        return f"q[{qubit_name[1:]}]"
    return qubit_name

def transpile(commands):
    qasm_lines = ['OPENQASM 2.0;', 'include "qelib1.inc";']
    qregs_declared = False
    cregs_declared = False

    for cmd in commands:
        if cmd.startswith('qubits'):
            n = int(cmd.split()[1])
            qasm_lines.append(f'qreg q[{n}];')
            qregs_declared = True
        elif cmd.startswith('cregs'):
            n = int(cmd.split()[1])
            qasm_lines.append(f'creg c[{n}];')
            cregs_declared = True
        elif cmd.startswith('bell'):
            a, b = cmd.split()[1].split(',')
            a_idx = qubit_to_index(a.strip())
            b_idx = qubit_to_index(b.strip())
            for line in MACRO_MAP['bell']:
                qasm_lines.append(line.format(a_idx, b_idx))
        elif cmd.startswith('superpos'):
            a = cmd.split()[1]
            a_idx = qubit_to_index(a.strip())
            for line in MACRO_MAP['superpos']:
                qasm_lines.append(line.format(a_idx))
        elif cmd.startswith('measure all'):
            qasm_lines.extend(MACRO_MAP['measure all'])
        else:
            qasm_lines.append('// Unknown command: ' + cmd)
    return '\n'.join(qasm_lines)
