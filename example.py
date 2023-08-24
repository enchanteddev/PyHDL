from PyHDL import Gate

gate = Gate.fp('Xor.hdl')
print(gate.run({'a': True, 'b': False}))