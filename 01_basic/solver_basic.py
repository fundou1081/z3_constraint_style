"""
01_basic: Z3 基础 - 变量、约束、求解
"""
from z3 import *

# 1. 创建求解器
s = Solver()

# 2. 定义变量
x = Int('x')
y = Int('y')

# 3. 添加约束
s.add(x > 0)
s.add(y > 0)
s.add(x + y == 10)

# 4. 求解
if s.check() == sat:
    model = s.model()
    print(f"x = {model[x]}")
    print(f"y = {model[y]}")
else:
    print("unsat")

# 5. 简化写法
x = Int('x')
s = Solver()
s.add(x >= 1, x <= 10)  # 类似 SV: constraint { x inside [1:10]; }
print(s.check(), s.model())
