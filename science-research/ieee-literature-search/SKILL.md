---
name: ieee-literature-search
license: MIT
description:
  IEEE Xplore 学术论文系统性检索技能。触发场景：用户要求"上网搜索IEEE论文""在IEEE上查相关文献""搜索有没有相关工作""核实是否有重复研究""确保不遗漏重要文献"。
  本技能确保：关键词覆盖多维度、搜索结果可追溯、结论结构化展示给用户。
metadata:
  author: user
  version: "1.1"
  created: 2026-08-22
  modified: 2026-08-23
---

# IEEE Literature Search Skill

## 核心原则

在开始搜索之前，先回答三个问题：
1. **用户要解决什么科学问题？**（精确到关键词和场景）
2. **搜索的目标是什么？**（确认无重复 / 找到基线论文 / 补充文献列表）
3. **成功标准是什么？**（找到 X 篇高相关论文 / 覆盖 Y 个维度）

---

## 搜索策略：多维度关键词矩阵

不要只用一个关键词组合搜索一次。按以下维度逐一覆盖，确保不遗漏：

### 第一维度：核心主题词（必做）
从用户问题的核心概念出发，覆盖所有同义词：
- 中文→英文翻译（如"位置误差"→"location error" / "position uncertainty" / "location uncertainty"）
- 缩写全称（如"ISAC"→"integrated sensing and communication" / "dual-functional radar-communication"）
- 场景限定（如"近场"→"near-field" / "near field"）

### 第二维度：方法/手段词（必做）
覆盖研究手段的同义词：
- 资源分配类：`resource allocation` / `time allocation` / `power allocation` / `pilot allocation` / `time switching` / `power splitting` / `time resource`
- 优化类：`joint optimization` / `tradeoff` / `trade-off` / `optimization` / `design`
- 误差类：`robust` / `uncertainty` / `error` / `misalignment` / `imperfect` / `mismatch`

### 第三维度：系统架构词（必做）
- RIS 相关：`RIS` / `reconfigurable intelligent surface` / `STAR-RIS` / `active RIS` / `BD-RIS`
- 场景：`near-field` / `far-field` / `mmWave` / `THz` / `6G`

### 第四维度：结果/指标词（按需）
- 性能指标：`CRB` / `rate` / `capacity` / `throughput` / `SNR` / `beamforming`
- 权衡类：`tradeoff` / `trade-off` / `balance` / `fraction`

### 第五维度：系统场景扩展（重要！）
**不要局限于用户指定的系统架构**。当核心问题可能存在于其他场景时，扩展搜索范围：
- 将 RIS 替换为 MIMO / 天线阵列：`MIMO` / `antenna array` / `phased array` / `massive MIMO`
- 去掉场景限定词：如去掉 `near-field` 限定，搜索更广泛的场景
- 跨场景方法迁移：不同场景提出的方法可能适用于目标场景

示例：
```
# 原搜索
"position error" AND "beam focusing" AND RIS AND "near-field"
# 扩展搜索（去掉近场限定）
"position error" AND "beam focusing" AND RIS
"position error" AND "beam focusing" AND (MIMO OR "antenna array")
"coordinate mismatch" AND "beamforming" AND (MIMO OR "antenna array")
```

### 组合策略
每组搜索使用 AND/OR 组合上述维度，例如：
```
"pilot allocation" AND "integrated sensing and communication" AND RIS
"location error" AND beamforming AND RIS
"sensing-aided" OR "sensing-assisted" AND communication AND RIS
"position error" AND "beam focusing" AND (MIMO OR "antenna array")
"coordinate mismatch" AND "beamforming gain" AND RIS
```

---

## 执行流程

### Step 1：启动 CDP
先加载 /web-access 技能，按指引启动 CDP 代理（会自动处理路径和浏览器连接）。

### Step 2：并行创建搜索标签页
每个关键词组合创建一个新标签页，批量发送：
```bash
curl -s http://localhost:3456/new --data-raw 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=<URL编码关键词>&topic=&newsearch=true&rowsPerPage=20'
```
同时创建多个（6-8 个为宜，避免浏览器负担过重）。

### Step 3：等待页面加载，提取结果
```bash
sleep 5  # 等待页面完全加载
curl -s "http://localhost:3456/eval?target=<ID>" -d 'JSON.stringify(Array.from(document.querySelectorAll("h3 a, [class*=title] a")).map(a => ({title: a.textContent.trim(), href: a.href})).slice(0, 8))'
```

### Step 4：识别高相关论文（分阶段读取）
**重要：如果某轮搜索命中论文超过 10 篇，按以下规则分阶段处理：**

1. **第一轮（快速筛选）**：只读取标题和链接，记录所有候选论文
2. **第二轮（摘要读取）**：按相关度排序，每次导航到 3-4 篇论文的详情页读取摘要
3. **第三轮（深度阅读）**：仅对前 3-4 篇最相关的论文导航到详情页完整阅读
4. **每轮结束后向用户反馈**，询问是否需要继续读取更多论文

```bash
# 导航到论文页
curl -s -X POST --data-raw '<完整IEEE URL>' "http://localhost:3456/navigate?target=<ID>"
sleep 3
# 读取摘要
curl -s "http://localhost:3456/eval?target=<ID>" -d 'document.querySelector(".abstract-content, [class*=abstract]")?.innerText?.substring(0, 1500) || document.body.innerText.substring(0, 1200)'
```

### Step 5：关闭标签页，整理结果
```bash
curl -s "http://localhost:3456/close?target=<ID>"  # 逐个关闭
```

### Step 6：向用户报告进度
每次完成一个搜索轮次后，向用户汇报：
- 本轮搜索的关键词
- 命中论文数
- 高相关论文（已读摘要的）
- 候选论文（仅记录标题的，等待后续读取）
- 询问是否继续搜索或读取更多论文

---

## 结果整理与展示

### 必须记录的内容
每次搜索结束时，整理以下信息，直接返回给用户：

#### 1. 搜索记录表
| 搜索轮次 | 关键词 | 命中论文数 | 高相关论文 |
|:---:|:---|:---:|:---|
| 1 | `"integrated sensing and communication" AND RIS` | 748 | — |
| 2 | `"resource allocation" AND "integrated sensing and communication" AND RIS` | 33 | Peng et al. 2024 WL |
| ... | ... | ... | ... |

#### 2. 核心发现总结
- **结论**：（如"未发现同时满足三个条件的工作"）
- **最接近的文献**：（列出 2-3 篇，说明接近程度和关键差异）
- **与新工作的差距**：（明确说明本研究填补的空白）

#### 3. 完整参考文献列表
每条文献包含：
- 作者、年份、期刊/会议
- 完整标题
- IEEE 链接（可点击）
- 与研究的差异（一句话说明为何不覆盖目标问题）

### 展示格式
```markdown
## 搜索结果报告

### 搜索概览
- 搜索时间：YYYY-MM-DD HH:MM
- 关键词总数：N 组
- 累计命中论文：M 篇
- 高相关论文：K 篇

### 搜索关键词（按维度分类）
| 维度 | 关键词组合 | 命中数 |
|:---|:---|:---:|
| ... | ... | ... |

### 核心发现
**结论**：...

### 最接近的文献（按相关度排序）
| 文献 | 相关度 | 排序理由 | 关键差异 |
|:---|:---:|:---|:---|
| ... | ... | ... | ... |

### 完整参考文献
| 简称 | 引用 | IEEE链接 |
|:---|:---|:---|
| ... | ... | https://ieeexplore.ieee.org/document/... |
```

---

## 注意事项

### 关键词设计技巧
- **同义词扩展**：`location error` / `position uncertainty` / `position error` 需同时搜索
- **缩写展开**：`ISAC` / `integrated sensing and communication` 都搜索
- **精确短语**：用双引号包裹固定搭配，如 `"time resource allocation"`
- **避免过宽**：单独搜索 `RIS` 会返回数百万结果，始终加入限定词
- **场景扩展**：搜索到核心问题后，主动去掉场景限定词（如 `near-field`），并在其他系统架构（如 MIMO、天线阵列）中搜索类似问题，不同场景的方法可能具有可迁移性
- **跨系统架构搜索**：将 RIS 替换为 MIMO / 天线阵列 / phased array 进行搜索

### 页面加载
- IEEE Xplore 搜索结果页需要 3-5 秒加载，务必 `sleep 5`
- 摘要页需要 2-3 秒，`sleep 3` 足够
- 超时或空白时，检查 `document.title` 确认页面是否加载

### 链接获取
- 搜索结果中的链接格式：`https://ieeexplore.ieee.org/document/<DOI号>/`
- 部分论文（如 arXiv 预印本）在 IEEE 尚未收录，改用 `https://arxiv.org/abs/<ID>`
- 导航到论文页后，从 URL 提取 DOI 号

### 标签页管理
- 搜索标签页读取完结果后立即关闭
- 论文摘要页读完摘要后关闭
- 避免同时打开超过 8 个标签页
