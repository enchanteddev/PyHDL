from parse import remove_comments, parse_chip_call

def nand(a: bool, b: bool) -> bool:
    return not(a and b)


GATE_REG: 'dict[str, Gate]' = {}
HDL_DIR = 'hdls'

class Gate:
    def __init__(self, name: str, inputs: list[str], outputs: list[str]) -> None:
        self.name = name
        GATE_REG[name.strip()] = self
        self.ins = inputs
        self.outs = outputs

        self.call_stack: list[tuple[str, dict[str, str]]] = []

        self.var: dict[str, bool] = {}
    
    def run(self, inputs: dict[str, bool]) -> dict[str, bool]:
        for ins in inputs:
            self.var[ins] = inputs[ins]
        for c in self.call_stack:
            # print(GATE_REG)
            gate = GATE_REG[c[0]]
            output = gate.run({inp: self.var[c[1][inp]] for inp in gate.ins})
            for out in output:
                self.var[c[1][out]] = output[out]
        
        return {inp: self.var[inp] for inp in self.outs}
    
    @classmethod
    def fp(cls, filepath: str):
        print(f"Loading: {filepath}")
        with open(f"{HDL_DIR}/{filepath}") as f:
            hdl = f.read()
        
        hdl = remove_comments(hdl)
        hdl = hdl[5:] # rm 'CHIP '
        name, code = hdl.split('{')
        code = code[:-1] # rm '}'

        statments = code.split(';')
        ins = []
        outs = []
        call_stack = []
        inside_parts = False
        for stmt in statments:
            if stmt.strip() == '': continue
            if stmt.startswith('IN'):
                ins = [e.strip() for e in stmt[2:].split(',')]
            elif stmt.startswith('OUT'):
                outs = [e.strip() for e in stmt[3:].split(',')]
            elif stmt.startswith('PARTS:'):
                inside_parts = True
                stmt = stmt[6:]

            if inside_parts:
                # print(stmt.split('('), 'a')
                partname, pins = stmt.split('(')
                if partname not in GATE_REG:
                    Gate.fp(f'{partname}.hdl')
                pins = pins[:-1]
                pins_dict = parse_chip_call(pins)
                call_stack.append((partname, pins_dict))
        
        ngate = cls(name=name, inputs=ins, outputs=outs)
        ngate.call_stack = call_stack

        return ngate


class Nand(Gate):
    def __init__(self, a: str = 'a', b: str = 'b', out: str = 'out') -> None:
        super().__init__('Nand', inputs = [a, b], outputs = [out])
    
    def run(self, inputs: dict[str, bool]) -> dict[str, bool]:
        return {self.outs[0]: nand(inputs[self.ins[0]], inputs[self.ins[1]])}
    

Nand()

# Not = Gate(["in"], ["out"])
# Not.call_stack = [(Nand(), {'a': 'in', 'b': 'in', 'out': 'out'})]
# # print(Not.run({'in': False}))

# And = Gate(["a", "b"], ["out"])
# And.call_stack = [(Nand(), {'a': 'a', 'b': 'b', 'out': 'o1'}), (Not, {'in': 'o1', 'out': 'out'})]

# And = Gate.fp('And.hdl')
# print(And.run({'a': True, 'b': True}))

Mux = Gate.fp('Mux.hdl')
print(Mux.run({'a': True, 'b': False, 'sel': True}))