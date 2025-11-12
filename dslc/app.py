from transpiler import transpile
from parser import parse_dsl

# Option 1: Parse a DSL file
commands = parse_dsl("examples/test_bell.qez")
qasm_code = transpile(commands)

# Option 2: Direct list of commands
dsl_commands = [
    'qubits 4',
    'cregs 4',
    'ghz q0,q1,q2,q3',
    'bell q0,q1',
    'oracle11 q2,q3',
    'measure all'
]
qasm_code = transpile(dsl_commands)

# Print or save
print(qasm_code)
with open("examples/test_bell.qasm", "w") as f:
    f.write(qasm_code)
