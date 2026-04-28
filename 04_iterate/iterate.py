"""
04_iterate: 遍历 + 随机采样
"""
from z3 import *
import random

def solve_all(s: Solver, vars, max_solutions: int = 100) -> list:
    """遍历所有解"""
    solutions = []
    while len(solutions) < max_solutions and s.check() == sat:
        m = s.model()
        solutions.append({v: m[v] for v in vars})
        # 排除当前解
        s.add(Or([v != m[v] for v in vars]))
    return solutions


def random_sample(s: Solver, vars, n: int = 1) -> list:
    """随机采样 n 个解"""
    all_sols = solve_all(s, vars, max_solutions=1000)
    if len(all_sols) <= n:
        return all_sols
    return random.sample(all_sols, n)


# 示例: 遍历小范围所有解
x, y = Ints('x y')
s = Solver()
s.add(x >= 1, x <= 5)
s.add(y >= 1, y <= 5)
s.add(x + y == 6)

vars = [x, y]
print("=== solve_all ===")
for i, m in enumerate(solve_all(s, vars)):
    print(f"解{i+1}: x={m[x]}, y={m[y]}")

print("\n=== random_sample(3) ===")
x2, y2 = Ints('x2 y2')
s2 = Solver()
s2.add(x2 >= 1, x2 <= 10)
s2.add(y2 >= 1, y2 <= 10)
s2.add(x2 + y2 <= 12)
for m in random_sample(s2, [x2, y2], 3):
    print(f"x2={m[x2]}, y2={m[y2]}")
