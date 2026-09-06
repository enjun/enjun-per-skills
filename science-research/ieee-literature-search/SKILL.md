---
name: ieee-literature-search
license: MIT
description:
  IEEE Xplore 学术论文系统性检索与全文获取技能（GPNU 机构登录）。触发场景：用户要求"上网搜索IEEE论文""在IEEE上查相关文献""搜索有没有相关工作""核实是否有重复研究""确保不遗漏重要文献""从IEEE下载论文PDF""给出IEEE/DOI链接要原文或元数据""机构登录/校园网认证下载"。
  本技能确保：关键词覆盖多维度、搜索结果可追溯、机构登录态可用（搜索/读摘要免登录，PDF 下载需机构登录）、结论结构化展示给用户。
  不触发：arXiv 等免费开放平台、解析本地 PDF（用 odl-pdf）、非学术性普通网页搜索。
metadata:
  author: user
  version: "1.3"
  created: 2026-08-22
  modified: 2026-09-06
---

# IEEE Literature Search Skill

## 核心原则

在开始搜索之前，先回答三个问题：
1. **用户要解决什么科学问题？**（精确到关键词和场景）
2. **搜索的目标是什么？**（确认无重复 / 找到基线论文 / 补充文献列表 / 获取元数据 / 下载全文）
3. **成功标准是什么？**（找到 X 篇高相关论文 / 覆盖 Y 个维度 / 拿到 N 篇 PDF）

按目标决定执行深度：

| 目标 | 执行到哪步 |
|------|-----------|
| 搜索文献（找相关论文、查重、列文献列表） | 步骤 1-6，整理结果后停止 |
| 获取论文信息（标题/作者/摘要/DOI/引用数等元数据） | 步骤 1-6，不下载 |
| 下载 PDF 全文 | 步骤 1-8 全流程（需机构登录） |

## 站点经验（先读再用）

操作前读本技能目录下 `references/site-patterns/` 中对应域名的经验文件：

- `ieeexplore.ieee.org.md`
- `gpnu.edu.cn.md`

经验标注了日期，可能过期：选择器失效时回退通用模式（看页面结构重新定位），成功后更新经验文件。

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
先加载 /web-access 技能，按指引启动 CDP 代理（会自动处理路径和浏览器连接），完成前置检查（check-deps）后向用户展示其自动化风险须知。CDP API 用法（/new、/eval、/clickAt、/screenshot 等）均见该技能。

注意：web-access 是第三方技能，会被更新覆盖。只按当次加载到的指引操作，不依赖其内部目录结构，也不向其目录写入任何文件。

### Step 2：检查机构登录状态（必做，多数情况免登录）

机构会话（SeamlessAccess 记住机构 + CAS/IdP 的 Cookie）通常跨天甚至数周有效，**多数情况下无需重新登录**。后台新 tab 打开 IEEE，用 /eval 检查页头是否出现 `Access provided by: <机构名>`。已登录则直接跳到搜索步骤——不要盲目重走登录流程，无谓的认证操作既慢又可能触发风控。

注意：未登录状态下**搜索和浏览通常不受限**，只有下载 PDF 或查看某些详情才被付费墙拦截。目标只是搜索/获取公开元数据时，登录不是前置条件，遇到拦截再走 Step 3。

### Step 3：机构登录（仅被付费墙拦截时）

IEEE：页头点击 "Institutional Sign In" → 弹窗中点击 "Access Through Guangdong Polytechnic Normal University"（SeamlessAccess 已记住机构；若显示"Add or Change Institution"则需重新选择机构）→ 进入学校认证。

学校认证三段式（所有联邦认证服务通用）：

1. **webauth.gpnu.edu.cn**（应用认证平台）：点击 `a#cas-login`
2. **cas.gpnu.edu.cn**（CAS）：默认微信扫码页，点击切换到账号登录；账密已被浏览器记住自动填充，**只需识别算术验证码**——截图后读取图片中的算式（如 9*7），计算结果用原生 setter 填入 `#captcha`
3. **idp.gpnu.edu.cn**（SAML 同意页）两步：
   - 声明页：先勾选"我同意此使用条款"复选框，再点 `_eventId_proceed` 按钮
   - 信息发布页：直接点"接受"（`_eventId_proceed`）

完成后回跳 IEEE，重新检查登录标志确认成功（页头出现 `Access provided by: <机构名>`）。

### Step 4：并行创建搜索标签页
每个关键词组合创建一个新标签页，批量发送：
```bash
curl -s http://localhost:3456/new --data-raw 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=<URL编码关键词>&topic=&newsearch=true&rowsPerPage=20'
```
同时创建多个（6-8 个为宜，避免浏览器负担过重）。

### Step 5：提取搜索结果
代理 `/new` 已内置页面加载等待，无需额外 sleep，直接提取。使用已验证的选择器 `a.fw-bold`（限定 a 标签，避免命中 "Sign In to Save Your Search" 等干扰元素）：
```bash
curl -s "http://localhost:3456/eval?target=<ID>" -d 'JSON.stringify(Array.from(document.querySelectorAll("a.fw-bold")).map(a => ({title: a.textContent.trim(), href: a.href})).slice(0, 15))'
```
注意：站点经验中记录的 `xpl-root-list-item` 在搜索结果页实测不存在（2026-09-06 验证），若个别页面状态出现可用作备用。

### Step 6：自动读取前 10 篇论文摘要
**关键改进**：仅凭标题难以判断论文价值，必须读取摘要。对每轮搜索的前 10 篇论文，在**同一搜索标签页**中依次导航读取摘要，然后重新导航回搜索结果页：
```bash
# 第1篇：导航到论文页（代理自动等待加载）
curl -s -X POST --data-raw '<论文URL>' "http://localhost:3456/navigate?target=<搜索页targetID>"
sleep 5  # IEEE 论文页加载较慢
# 读取摘要
curl -s "http://localhost:3456/eval?target=<搜索页targetID>" -d 'document.querySelector(".abstract-text-content")?.innerText?.substring(0, 1500)'
# 重新导航回搜索结果页
curl -s -X POST --data-raw '<搜索URL>' "http://localhost:3456/navigate?target=<搜索页targetID>"
sleep 5  # IEEE 搜索结果 JS 渲染需要重建 DOM
# 重复上述流程，读完所有论文
```
**注意**：
- 摘要选择器使用 `.abstract-text-content`（IEEE Xplore 论文页标准类名）
- 搜索页重建需 `sleep 5`，因 IEEE 使用 JS 动态渲染列表
- 重新导航回搜索页比 `/back` 更可靠，避免 DOM 未重建的问题

### Step 7：下载 PDF 全文（仅下载需求）

**不要**用浏览器直接导航到 PDF URL 或 blob `<a download>` 点击（原因见陷阱）。使用本技能自带脚本（`<skill-dir>` 为本技能所在目录）：

```bash
node "<skill-dir>/scripts/extract_pdf.js" <targetId> "<PDF真实URL>" "<输出绝对路径.pdf>"
```

- `<targetId>`：当前文献页所在 tab 的 ID（脚本会在该页面上下文内 fetch，同源携带机构 Cookie）
- IEEE 的 PDF 真实 URL：打开 `stamp/stamp.jsp?tp=&arnumber=<id>` 后从 iframe src 提取，形如 `stampPDF/getPDF.jsp?tp=&arnumber=<id>&ref=`
- 脚本自动完成：非阻塞 fetch → 轮询缓存 → 分块 base64 提取 → 本地解码落盘 → 魔数与 %%EOF 校验
- 校验通过即下载成功，**不要做内容解析**（提取文本、验证页数、读标题等）——解析由 odl-pdf 负责，本技能只负责把 PDF 完整下载到本地
- 下载完成后：关闭自己创建的 tab、删除临时截图文件

### Step 8：关闭标签页，整理结果
```bash
curl -s "http://localhost:3456/close?target=<ID>"  # 逐个关闭
```

### Step 9：向用户报告进度
每次完成一个搜索轮次后，向用户汇报：
- 本轮搜索的关键词
- 命中论文数
- 前 10 篇论文的摘要（含核心方法和主要结论）
- 关键发现（是否有满足条件的文献）
- 询问是否继续搜索其他关键词组合

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
- 已读摘要论文：K 篇

### 搜索关键词（按维度分类）
| 维度 | 关键词组合 | 命中数 | 已读摘要 |
|:---|:---|:---:|:---:|
| ... | ... | ... | ... |

### 论文摘要（按相关度排序，前10篇）
| # | 标题 | 核心方法 | 主要结论 | 差异 |
|:---:|:---|:---|:---|:---|
| 1 | [标题](IEEE链接) | 方法简述 | 结论简述 | 与目标差距 |
| ... | ... | ... | ... | ... |

### 核心发现
**结论**：...（基于摘要的综合判断）

### 完整参考文献
| # | 引用 | IEEE链接 | 已读摘要 |
|:---:|:---|:---|:---:|
| 1 | 作者, 年份, 期刊 | https://ieeexplore.ieee.org/document/... | ✅ |
```

---

## 通用机构模式（其他数据库）

任何支持 SeamlessAccess/Shibboleth 的数据库（Springer、Wiley、Web of Science、ACM 等）流程同构：

1. 找入口：页面找 "Institutional Sign In" / "Sign in via your institution" / "Access through your institution" / Shibboleth 登录入口
2. 机构选择：可能需要手动输入机构名 "Guangdong Polytechnic Normal University"（或中文"广东技术师范大学"）
3. 进入学校认证后，走 Step 3 的"学校认证三段式"，与入口无关
4. 搜索/信息提取/下载方式按目标站点结构调整，但 extract_pdf.js 的模式通用：在站点域名下的正常 HTML 页面上下文 fetch PDF 地址

首次操作新站点验证成功后，把站点经验写入本技能 `references/site-patterns/<域名>.md`（不要写入第三方技能目录）。

---

## 注意事项

### 关键词设计技巧
- **同义词扩展**：`location error` / `position uncertainty` / `position error` 需同时搜索
- **缩写展开**：`ISAC` / `integrated sensing and communication` 都搜索
- **精确短语**：用双引号包裹固定搭配，如 `"time resource allocation"`
- **避免过宽**：单独搜索 `RIS` 会返回数百万结果，始终加入限定词
- **场景扩展**：搜索到核心问题后，主动去掉场景限定词（如 `near-field`），并在其他系统架构（如 MIMO、天线阵列）中搜索类似问题，不同场景的方法可能具有可迁移性
- **跨系统架构搜索**：将 RIS 替换为 MIMO / 天线阵列 / phased array 进行搜索

### 机构登录
- **React 表单赋值**（登录页、搜索框）：必须用 `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,"value").set` 原生 setter 赋值后 dispatch `input` 事件；直接 `.value=` 会在提交时被 React 清空，表现为"点了登录没反应/验证码被清空"
- **算术验证码**：`#captcha` 输入框旁的图片显示算式，截图用视觉读取。填错时页面停留原地，重新截图识别新题
- **CAS 登录后停在本页不动** = 验证码未被表单接受（React 清空了程序化赋值），需原生 setter 重填

### PDF 下载
- **PDF 查看器上下文无 DOM**：直接导航到 PDF URL 后，Chrome 内置查看器页面无法执行 fetch+DOM 操作
- **blob 下载被静默拦截**：无用户手势的 `<a download>` 点击在 IEEE 域下不产生文件，Downloads 目录为空。所以用分块提取脚本
- **Proxy 返回两层 JSON**：eval 结果格式为 `{"value":"<JS返回值的JSON字符串>"}`，需两次 JSON.parse（extract_pdf.js 已处理）
- **IEEE PDF 权限标记误报**：部分工具（如直接 Read PDF）会报 "password-protected"，实际未加密，任何阅读器和解析工具可正常打开。下游用 odl-pdf 解析时如遇此报错，忽略或直接跑 ODL 即可

### 页面加载
- 代理 `/new` 和 `/navigate` 已内置页面加载等待（polling `document.readyState`），无需额外 `sleep`
- 超时或空白时，检查 `document.title` 确认页面是否正常加载：`curl -s "http://localhost:3456/eval?target=<ID>" -d 'document.title'`

### 链接获取
- 搜索结果中的链接格式：`https://ieeexplore.ieee.org/document/<DOI号>/`
- 部分论文（如 arXiv 预印本）在 IEEE 尚未收录，改用 `https://arxiv.org/abs/<ID>`
- 导航到论文页后，从 URL 提取 DOI 号

### 标签页管理
- 搜索标签页读取完结果后立即关闭
- 论文摘要页读完摘要后关闭
- 避免同时打开超过 8 个标签页

### 其他
- **Node 的 /tmp 路径**：Windows 下 Node 将 `/tmp` 解析为 `<当前盘>:\tmp`。跨工具传路径用 `cygpath -w` 转换或直接用绝对路径
