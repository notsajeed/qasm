# ⚛️ Quantum DSL → QASM Transpiler

A small **experimental project** that converts a simple **Quantum DSL (`.qez`)** into **OpenQASM 2.0**.  
Built for **learning**, **experimentation**, and exploring **quantum circuit design**.

---

## 🧩 Example

### ✍️ DSL (`example.qez`)

```qez
qubits 4
cregs 4
ghz q0,q1,q2,q3
bell q0,q1
oracle11 q2,q3
measure all
```

### ⚙️ Generated QASM

```qasm
OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg c[4];
h q[0];
cx q[0],q[1];
cx q[0],q[2];
cx q[0],q[3];
h q[0];
cx q[0],q[1];
x q[2];
x q[3];
cx q[2],q[3];
x q[2];
x q[3];
measure q -> c;
```

---

## 📁 Structure

```
qasm/
├─ cli.py
├─ requirements.txt
├─ examples/
│   └─ test_bell.qez
└─ dslc/
   ├─ parser.py
   ├─ transpiler.py
   ├─ app.py
   ├─ utils.py
   └─ macros/
       ├─ bell.inc
       ├─ ghz.inc
       └─ oracle.inc
```

---

## ⚙️ Usage

```bash
python cli.py examples/test_bell.qez -o examples/test_bell.qasm
```

or use it directly in Python:

```python
from dslc.parser import parse_dsl
from dslc.transpiler import transpile

commands = parse_dsl("examples/test_big.qez")
qasm = transpile(commands)
print(qasm)
```

---

## Notes

- 🔬 **Experimental**
- 🪶 Small, modular, and easy to extend with new macros

---
