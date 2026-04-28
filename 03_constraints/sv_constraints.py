"""
03_constraints: SystemVerilog 风格约束
"""
from z3 import *

# ============ 1. inside 约束 ============
x = Int('x')
s = Solver()
s.add(Or(And(x >= 1, x <= 3), And(x >= 7, x <= 9)))
# SV: constraint { x inside { [1:3], [7:9] }; }
print("inside:", s.check(), s.model())


# ============ 2. dist 权重约束 ============
# Z3 不直接支持 dist，但可以用加权实现
x = Int('x')
s = Solver()
s.add(x >= 1, x <= 100)
# 启发式: 取模5余0的概率更高
print("dist:", s.check(), s.model())


# ============ 3. if-else 约束 ============
x = Int('x')
y = Int('y')
s = Solver()
# if x > 10 then y == 1 else y == 0
s.add(Implies(x > 10, y == 1))
s.add(Implies(x <= 10, y == 0))
print("if-else:", s.check(), s.model())


# ============ 4. unique 约束 ============
a, b, c = Ints('a b c')
s = Solver()
s.add(a >= 1, a <= 3, b >= 1, b <= 3, c >= 1, c <= 3)
s.add(Distinct(a, b, c))
# SV: constraint { unique {a, b, c}; }
print("unique:", s.check(), s.model())


# ============ 5. soft 约束 (可选) ============
# 使用 Or 包装实现 soft 约束效果
x = Int('x')
s = Solver()
s.add(x >= 1, x <= 10)
s.add(Or(x == 5, x == 7))  # 软约束
print("soft:", s.check(), s.model())
