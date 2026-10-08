# 三个子代理的收集简报模板

主代理按本文件组装三个子代理的提示词。组装规则：
- 把 `{{WINDOW}}` 替换为显式日期区间（如 "2026-07-07 至 2026-10-07"），把 `{{TOPIC}}` 替换为主题范围描述。
- `{{SKILL_DIR}}` 替换为本技能当前运行的安装目录（一般为 `~/.claude/skills/ris-progress-radar`）。
- 关键词从 keywords.md 按主题裁剪后拼入。
- 用户指定详略侧重时，给被精简路线的简报追加一句："本次你为精简模式：不追求全量覆盖，摸清概况并给出 5-8 条最有代表性的条目即可，检索时间减半。"
- 三个 Agent 调用必须在同一条消息中发出（并行）。
- 每个简报末尾的输出格式是统一的，主代理依赖该格式做汇总。

通用约束（拼入每个简报开头）：

```
今天是 {{END_DATE}}。你的任务：收集 {{WINDOW}} 期间 RIS（可重构智能表面）领域的进展，主题范围：{{TOPIC}}。
硬性规则：
0. 先阅读 {{SKILL_DIR}}/references/state-baseline.md 中与你路线相关的基线小节：那是上次运行的
   状态快照（3GPP 已核查的会议与结论、玩家名单、阴性结果等）。你的策略是"验证增量"——直接核查
   基线指出的观察点、复核关键结论是否仍成立、寻找玩家新动态，而不是从零重建已知结论；发现基线
   过时或有误，在输出末尾单列"基线修正建议"供主代理更新。
1. 禁止凭内部知识罗列任何"进展"——每条信息必须有本次实际检索到的 URL 佐证。
2. 每条信息核对发布日期：不在 {{WINDOW}} 内的不收录（背景性内容可在"背景"小节简述并注明为窗口外）。
3. 宁多勿漏，后续由主代理筛选；但每条必须真实可访问。
4. 检索时间有限，合理分配：先广（多关键词并行搜）后精（对重要线索深挖）。
5. 结束时如实报告：查了哪些源、哪些源失败或跳过、覆盖自评。
```

---

## Brief A：学术理论代理（academic）

```
【任务】收集 {{WINDOW}} 期间 {{TOPIC}} 方向的学术研究进展：新论文、新综述、窗口内举行的会议/论文集。

【关键词】使用以下关键词组合（同义词矩阵已裁剪）：
{{KEYWORDS}}

【信息源与检索方法，按序执行】
1. IEEE Xplore（主力）：先阅读 ~/.claude/skills/ieee-literature-search/SKILL.md，按其多维度关键词矩阵方法检索。
   - 重点期刊：TWC、TCOM、JSAC、WCL、CL、OJ-COMS、TVT、IoT-J、Antennas Wireless Propag. Lett.
   - 日期过滤注意：检索 URL 的日级 ranges 参数不可靠（实测返回 0 结果）。做法：年份过滤 + 最新排序，
     抽样夹逼估算窗口内总量；候选论文逐篇打开核对 "Date of Publication"。期刊精选加 ContentType:Journals
     剔除会议论文（窗口若含 PIMRC/ICC 等会议论文集入库期，会议论文会淹没期刊列表）。
   - 侧栏 Conference 过滤窗口内举行的 ICC / GLOBECOM / WCNC / PIMRC 等，确认论文集是否已上线。
   - 只需搜索+读摘要，不需要机构登录下载 PDF。
2. arXiv：用 WebSearch 检索 `site:arxiv.org` + 关键词 + 年月限定；或 WebFetch 访问
   `https://arxiv.org/list/eess.SP/recent`（仅看最近页，历史月份用检索）。
   重点 cs.IT 与 eess.SP 两个分类。
3. 综述专搜：`(survey OR tutorial OR overview) AND <关键词>`，窗口内新综述单独归类——
   综述是领域风向标，即使质量一般也值得记录。

【记录要求】
- 目标数量级：先摸清窗口内总量（IEEE 检索结果页会显示命中数），然后精选 15-30 篇代表性论文
  （顶刊优先、引用价值高、方向代表性强；避免同质化堆叠）。
- 对每篇：读标题+摘要即可，判断其贡献类型（理论建模/算法/硬件/试验/综述）。

【输出格式】严格按此清单输出（Markdown）：
## 学术进展原始清单
### 总量概况
（窗口内各源命中数量级，1-2 句）
### 综述与tutorial
- [YYYY-MM-DD] 标题 | 期刊/会议 | 一句话概括 | 贡献类型 | URL
### 代表性论文（按方向分组）
#### <方向1，如 近场/ISAC/硬件>
- [YYYY-MM-DD] 标题 | 期刊/会议 | 一句话概括（方法+结果）| URL
### 背景参考（窗口外但重要）
- ...
### 覆盖情况
- 已查：<源列表>；失败/跳过：<原因>；自评覆盖度：<低/中/高> + 一句理由
```

---

## Brief B：标准化代理（standards）

```
【任务】收集 {{WINDOW}} 期间 {{TOPIC}} 相关的标准化动态：立项、文稿讨论、结题、白皮书、规划。

【信息源与检索方法，按优先级执行】
1. 3GPP（一手来源，最权威）：
   a. 先阅读 ~/.claude/skills/3gpp-access/SKILL.md，严格遵守其访问铁律（UA、403、字母序陷阱）。
   b. RIS 在 3GPP 尚无独立立项，相关讨论出现在：RAN/RAN1 会议中对 6G 研究的讨论文稿、
      6G workshop 文稿、SA1/SA2 需求文档。检索方式：
      - 列出窗口内召开的 RAN 全会与 RAN1 会议届次（注意字典序陷阱，用 grep 找三位数届次）
      - 进入 Docs/ 目录，curl 下载后用 office2txt.py 转文本，grep 关键词：
        reconfigurable / RIS / intelligent surface / smart surface / metasurface
      - 文件多时先 grep 文件名列表，挑含关键词的下载（控制请求量，避免触发限流）
   c. 同时检查窗口内是否有新的 6G 相关 TR 发布（Specs/latest/Rel-20/ 等）。
2. ETSI：ISG RIS 已于 2023 年结束，但检查 etsi.org 是否有窗口内新发布的白皮书/报告/后续活动。
3. ITU-R / ITU-T：IMT-2030 愿景与评估材料中 RIS 相关内容是否有更新。
4. 区域组织（中文源）：IMT-2030(6G) 推进组（含智能超表面任务组/技术联盟 RISTA）、CCSA 立项公告、
   中国信通院发布物。用 WebSearch 检索。
5. IEEE 标准协会：搜窗口内 RIS/超表面相关标准动态（如有）。

【记录要求】
- 每条注明：文档号（如 RP-261576）/会议届次/组织、发布日期、状态（立项中/已发布/讨论稿）。
- 区分 NCR（network-controlled repeater，Rel-18 已标准化的放大转发设备）与 RIS 本体，二者相关
  但不同——NCR 的后续演进也算相关动态，但要标注清楚。
- 3GPP 会议有周期（每年约 4 次全会），窗口内可能没有关键会议——如实记录会议日历，说明下一场
  关键会议的时间，这本身就是有价值的预测信息。

【输出格式】（与 Brief A 同构）
## 标准化动态原始清单
### 3GPP
- [YYYY-MM-DD] 文档号/事件 | 会议届次 | 状态 | 与RIS的关系（直接/间接/NCR相关）| 一句话概括 | URL
### ETSI / ITU / 其他国际组织
- ...
### 中国：IMT-2030 推进组 / CCSA / 信通院
- ...
### 窗口外背景与前瞻
（如"RAN#113 预计于 YYYY-MM 召开，议程中含 XXX"）
### 覆盖情况
- 已查/失败/自评（同 Brief A）
```

---

## Brief C：工业界代理（industry）

```
【任务】收集 {{WINDOW}} 期间 {{TOPIC}} 相关的工业界动态：产品发布、现场试验、商用部署、
投融资、创业公司、行业报告。

【信息源与检索方法】
工业界文档不用 "RIS" 一词，检索词务必用：smart repeater / 智能中继 / reconfigurable surface /
intelligent surface / 数字可编程超表面 / dynamic coverage（详见 keywords.md 第 4 节）。

1. 设备商官方 newsroom（逐个检查窗口内新闻）：
   Huawei、ZTE（中兴）、Ericsson、Nokia、Samsung、Qualcomm、NTT DOCOMO（RIS 现场试验老玩家）、
   NEC、大唐/中信科。
   方法：WebSearch `site:<厂商域名> <关键词>`，或直接搜 `<厂商名> smart repeater|RIS|超表面 2026`。
2. 运营商：中国移动、中国电信、中国联通、Vodafone、NTT DOCOMO、SK Telecom、KT、Orange、TIM。
   关注：试验新闻、现网试点、招标/集采公告（中国运营商集采是商业化风向标）。
3. 创业公司与投融资：搜 `RIS startup funding 2026`、`reconfigurable intelligent surface company`、
   `智能超表面 创业 融资`。已知玩家（历史上活跃的）：Greenerwave（法国）、Pivotal Commware（美国）；
   以检索发现的为准，不限于这两个。
4. 行业媒体（B 类信源）：C114 通信网、通信世界网、Light Reading、RCR Wireless、6GWorld、
   Mobile World Live、副标题含 telecom 的主流科技媒体。
5. 展会与论坛（检查 {{WINDOW}} 是否覆盖）：MWC 巴塞罗那（2-3月）、MWC 上海（6月）、
   PT Expo 北京通信展（9月底）、GTI 论坛、IEEE GLOBECOM（12月）/ICC（5-6月）产业论坛。
   覆盖到哪个就重点搜哪个的 RIS/智能超表面相关发布。
6. 行业报告：搜窗口内新发布的 RIS 市场报告/白皮书（GSMA、ABI、Omdia、信通院等）。

【记录要求】
- 每条标注信源类型：[A] 厂商官方新闻稿 / [B] 权威媒体转述 / [C] 自媒体或无出处消息。
- 对"试验/试点"类消息，尽量提取硬信息：频段、规模（站点数/覆盖区域）、性能数字、合作方、时间表。
- 明显营销话术（"革命性""颠覆性"但无参数）如实标注为宣传性消息，不作重点。

【输出格式】（与 Brief A 同构）
## 工业界动态原始清单
### 设备商与芯片商
- [YYYY-MM-DD] 厂商 | 事件类型（产品/试验/合作）| 信源类型[A/B/C] | 摘要+硬参数 | URL
### 运营商与现网部署
- ...
### 创业公司与投融资
- ...
### 展会与行业活动（窗口内）
- ...
### 待证实消息（C类）
- ...
### 覆盖情况
- 已查/失败/自评（同 Brief A）
```
