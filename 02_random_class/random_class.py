"""
02_random_class: RandomClass 封装 - 类似 SV randomize 风格
"""
from z3 import *

class RandomClass:
    def __init__(self):
        self.vars = {}
        self.constraints = []
    
    def rand(self, name, sort):
        self.vars[name] = Const(name, sort)
        return self.vars[name]
    
    def constraint(self, *conds):
        self.constraints.extend(conds)
    
    def randomize(self, solver=None):
        s = solver or Solver()
        for c in self.constraints:
            s.add(c)
        if s.check():
            return s.model()
        return None
    
    def solve_all(self, max_solutions=100):
        s = Solver()
        for c in self.constraints:
            s.add(c)
        solutions = []
        while len(solutions) < max_solutions and s.check() == sat:
            m = s.model()
            solutions.append(m)
            s.add(Or([v != m[v] for v in self.vars.values()]))
        return solutions


class RandPacket(RandomClass):
    def __init__(self):
        super().__init__()
        self.length = self.rand('length', BitVecSort(8))
        self.addr = self.rand('addr', BitVecSort(32))
        self.data = [self.rand('data_' + str(i), BitVecSort(8)) for i in range(4)]
        self._build_constraints()
    
    def _build_constraints(self):
        self.constraint(
            self.length >= 1,
            self.length <= 64,
            self.addr & 0x3 == 0,
            And([d != 0 for d in self.data])
        )


if __name__ == "__main__":
    pkt = RandPacket()
    m = pkt.randomize()
    if m:
        print("length =", m[pkt.length])
        print("addr   =", m[pkt.addr])
        d0 = m[pkt.data[0]]
        d1 = m[pkt.data[1]]
        d2 = m[pkt.data[2]]
        d3 = m[pkt.data[3]]
        print("data  =", [d0, d1, d2, d3])
    
    print("\n--- solve_all 前3个解 ---")
    for i, m in enumerate(pkt.solve_all(3)):
        print("solution", i+1, ": length=", m[pkt.length], ", addr=", m[pkt.addr])
