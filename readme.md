# HDL
An HDL interpreter implemented in python.

## How To Use

1. Make A folder called ```hdls``` in your working directory
2. Write your CHIP ```(.hdl)``` file inside of it
3. Load your CHIP by its filename (and NOT THE RELATIVE PATH).

```python
from PyHDL import Gate

gate = Gate.fp('Xor.hdl')
print(gate.run({'a': True, 'b': False}))
```

**Output:**
```
Loading: Xor.hdl
Loading: Not.hdl
Loading: And.hdl
Loading: Or.hdl
{'out': True}
```
## Note
Bus has not been implemented, i.e. multibit inputs and outputs will not work as of now. Will be implemented soon.

Made by Kaushik.