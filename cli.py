# cli.py
import argparse
from dslc.parser import parse_dsl
from dslc.transpiler import transpile

def main():
    parser = argparse.ArgumentParser(description="QASM DSL Compiler")
    parser.add_argument('input', help='Input DSL script (.qez)')
    parser.add_argument('-o', '--output', help='Output QASM file', default='output.qasm')
    args = parser.parse_args()

    commands = parse_dsl(args.input)
    qasm_code = transpile(commands)

    with open(args.output, 'w') as f:
        f.write(qasm_code)
    print(f'QASM code generated in {args.output}')

if __name__ == '__main__':
    main()
