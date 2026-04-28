# Z3 Constraint Style Project

## 项目目标
用 Z3 实现 SystemVerilog constraint 风格的约束系统，具备：
- **约束定义**：类似 SV random class 的声明式约束
- **随机生成**：constraint solve + random pick
- **快速遍历**：类似 SV foreach+randomize() 的全遍历/采样
- **约束求解**：唯一解/多解/解数量统计

## 核心功能对标 SV

| SystemVerilog | Z3 实现 |
|--------------|---------|
| `rand int x` | `x = Int('x')` + `rand_var(x)` |
| `constraint c { x > 0; x < 10 }` | `s.add(x > 0, x < 10)` |
| `randomize()` | `s.check()` -> `model` |
| `randomize with { x == 5; }` | 添加额外约束后求解 |
| `foreach(i) randomize` | `solve_all()` 遍历所有解 |

## 目录结构
```
z3_constraint_style/
├── 01_basic/           # 基础：Int/BitVec 变量 + 约束求解
├── 02_random_class/   # RandomClass 封装（核心）
├── 03_constraints/    # 各类约束：dist/inside/solve
├── 04_iterate/         # 遍历所有解 + 随机采样
├── 05_rtl_gen/        # 生成合法 RTL 输入向量
├── 06_multi_var/      # 多变量 + 数组约束
└── REPOS.md
```

## RandomClass 设计模式
```python
class RandomPacket:
    def __init__(self):
        self.length = Int('length')
        self.addr = BitVec('addr', 32)
        self.data = [BitVec(f'data_{i}', 8) for i in range(4)]
    
    def constraints(self):
        return [
            self.length >= 1,
            self.length <= 64,
            self.addr[1:0] == 0,  # alignment
        ]
    
    def randomize(self, solver=None):
        s = solver or Solver()
        for c in self.constraints():
            s.add(c)
        if s.check():
            return s.model()
        return None
    
    def solve_all(self):
        """遍历所有可行解"""
        s = Solver()
        for c in self.constraints():
            s.add(c)
        solutions = []
        while s.check():
            solutions.append(s.model())
            s.add(Or([v != s.model()[v] for v in s.model()]))
        return solutions
```

## 关键参考
- Z3 Python: https://pythonz3.readthedocs.io
- SV Constraint: IEEE 1800 `randomize()` + `constraint`
