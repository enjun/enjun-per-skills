# Experiment Design Guide

本文档包含实验设计的详细指南。主 SKILL.md 中的实验相关内容应引用此文件。

---

## Quick Reference

**Supporter runs experiments to:**
- Validate performance predictions
- Compare with baselines
- Test theoretical assumptions
- Demonstrate feasibility

**Critic runs experiments to:**
- Test edge cases or failure modes
- Challenge optimistic assumptions
- Compare with alternative methods
- Reveal hidden weaknesses

**Principles:**
- Focused (one claim per experiment)
- Fast (< 3 minutes)
- Reproducible (set random seeds)
- Visual (publication-quality figures)

**RIS Integration:** For RIS problems, see `references/ris-code-integration.md` for available modules (RIS channel models, phase optimization, beamforming design).

---

## 何时运行实验

### Supporter (Stage 2) 运行实验来：

1. **验证性能预测**
   - 当提出具体的性能指标（如 "可达速率提升 30%"）
   - 需要数学模型或仿真来支撑数字

2. **与基线方法对比**
   - 声称"优于现有方法"时
   - 需要公平对比实验

3. **验证理论假设**
   - 当方案依赖于特定假设（如 "信道是瑞利衰落"）
   - 需要验证假设的合理性

4. **证明关键组件可行性**
   - 当提出新的算法或协议
   - 需要原型验证

### Critic (Stage 3) 运行实验来：

1. **测试边界情况**
   - 当理论分析未覆盖边界条件
   - 需要压力测试

2. **挑战乐观假设**
   - 当性能预测过于乐观
   - 需要更现实的场景测试

3. **与替代方法比较**
   - 当存在竞争方案
   - 需要对比实验

4. **揭示隐藏弱点**
   - 当理论分析可能有遗漏
   - 需要实验发现潜在问题

---

## 实验设计原则

### 1. 聚焦原则

每次实验只测试一个具体声明或假设。

**好的实验设计：**
- "验证在 SNR=10dB 时，提出方案的误码率低于 QPSK"
- "测试在 100 个用户场景下的算法收敛速度"

**不好的实验设计：**
- "验证整个系统的性能"（太宽泛）

### 2. 快速原则

实验应在 3 分钟内完成。

**实现方法：**
- 减少仿真点数（1000 次蒙特卡洛通常足够）
- 使用简化信道模型
- 限制参数扫描范围
- 避免复杂的多层仿真

### 3. 可重现原则

```python
# 总是设置随机种子
np.random.seed(42)
random.seed(42)

# 记录所有参数
config = {
    "snr_range": np.linspace(0, 20, 11),
    "num_users": 50,
    "num_iterations": 1000,
    ...
}
```

### 4. 可视化原则

生成出版质量的图表：

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.plot(snr_range, ber_proposed, 'o-', label='Proposed', linewidth=2)
plt.plot(snr_range, ber_baseline, 's--', label='Baseline', linewidth=2)
plt.xlabel('SNR (dB)', fontsize=12)
plt.ylabel('Bit Error Rate', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.yscale('log')
plt.tight_layout()
plt.savefig('docs/figures/ber_comparison.png', dpi=300)
```

---

## 实验输出格式

### JSON 输出

每个实验应产生结构化输出：

```json
{
  "experiment_name": "ber_vs_snr_comparison",
  "purpose": "验证提出方案在 SNR=10dB 时 BER 低于 QPSK",
  "method": "蒙特卡洛仿真，1000 次迭代，SNR 范围 0-20dB",
  "results": {
    "ber_at_10dB_proposed": 1.2e-4,
    "ber_at_10dB_baseline": 3.5e-4,
    "improvement": "66% reduction"
  },
  "figure": "docs/figures/ber_comparison.png",
  "conclusion": "实验结果支持方案的性能声明：在 SNR=10dB 时，BER 降低 66%"
}
```

### 文件组织

```
scripts/
├── experiment_proposed_method.py    # Stage 2 实验脚本
├── experiment_challenge_edge_case.py # Stage 3 实验脚本
└── utils/
    ├── channel_models.py            # 可复用的信道模型
    └── metrics.py                   # 评估指标

docs/figures/
├── ber_comparison.png
├── convergence_speed.png
└── scalability_test.png
```

---

## 常见实验模板

### 1. 性能对比实验

```python
import numpy as np
import matplotlib.pyplot as plt

def performance_comparison():
    """比较提出方案与基线方案的 BER 性能"""
    snr_range = np.linspace(0, 20, 11)
    ber_proposed = []
    ber_baseline = []

    for snr in snr_range:
        # 提出方案
        ber_proposed.append(simulate_proposed(snr, n_iter=1000))
        # 基线方案
        ber_baseline.append(simulate_baseline(snr, n_iter=1000))

    # 绘图
    plt.figure(figsize=(8, 6))
    plt.semilogy(snr_range, ber_proposed, 'o-', label='Proposed', linewidth=2)
    plt.semilogy(snr_range, ber_baseline, 's--', label='Baseline', linewidth=2)
    plt.xlabel('SNR (dB)', fontsize=12)
    plt.ylabel('Bit Error Rate', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.title('BER Performance Comparison', fontsize=14)
    plt.tight_layout()
    plt.savefig('docs/figures/ber_comparison.png', dpi=300)

    return {
        "ber_at_10dB": float(ber_proposed[5]),
        "improvement_factor": float(ber_baseline[5] / ber_proposed[5])
    }
```

### 2. 收敛性实验

```python
def convergence_test():
    """测试算法收敛速度"""
    iterations = range(1, 101)
    objective_proposed = []
    objective_baseline = []

    for n in iterations:
        objective_proposed.append(run_proposed(n))
        objective_baseline.append(run_baseline(n))

    plt.figure(figsize=(8, 6))
    plt.plot(iterations, objective_proposed, label='Proposed')
    plt.plot(iterations, objective_baseline, label='Baseline')
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Objective Value', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('docs/figures/convergence.png', dpi=300)
```

### 3. 边界情况测试（Critic 使用）

```python
def edge_case_test():
    """测试极端场景下的性能"""
    test_cases = [
        {"name": "Low SNR", "snr": -5},
        {"name": "High SNR", "snr": 30},
        {"name": "Many users", "num_users": 500},
        {"name": "Few users", "num_users": 2}
    ]

    results = {}
    for case in test_cases:
        try:
            results[case["name"]] = simulate(**case)
        except Exception as e:
            results[case["name"]] = f"Failed: {str(e)}"

    return results
```

---

## RIS 系统实验

对于 RIS（可重构智能表面）相关问题，可复用 [ris-code-integration.md](ris-code-integration.md) 中的仿真模块。

### 可用模块

- `ris_channel.py`: RIS 信道模型
- `phase_optimization.py`: 相位优化算法
- `beamforming.py`: 波束成形设计

### 使用示例

```python
from scripts.ris_channel import RISChannel
from scripts.phase_optimization import optimize_phases

# 创建 RIS 信道
channel = RISChannel(
    num_elements=64,
    tx_position=[0, 0, 10],
    rx_position=[100, 0, 0],
    ris_position=[50, 0, 5]
)

# 优化相位
phases = optimize_phases(
    channel=channel,
    method="proposed_algorithm"
)

# 评估性能
rate = channel.calculate_rate(phases)
```

---

## 实验审查清单

在提交实验结果前，检查：

- [ ] 实验目的清晰
- [ ] 只测试一个具体声明
- [ ] 运行时间 < 3 分钟
- [ ] 设置了随机种子
- [ ] 参数已记录
- [ ] 生成了可视化图表
- [ ] 图表有清晰的标签和图例
- [ ] 结果以 JSON 格式输出
- [ ] 结论明确链接到方案声明
- [ ] 代码保存到 `scripts/`
- [ ] 图表保存到 `docs/figures/`

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 实验太慢 | 减少迭代次数，简化信道模型，限制参数范围 |
| 内存不足 | 批量处理，使用生成器而非列表 |
| 结果不稳定 | 增加随机种子，增加迭代次数 |
| 图表不清晰 | 增加 dpi，使用矢量格式（PDF），调整字体大小 |
| 代码不可复现 | 检查随机性，记录所有参数，保存配置 |
