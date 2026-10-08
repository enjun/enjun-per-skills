# RIS 关键词矩阵

RIS 领域文献与新闻的用词极度分散，只搜 `RIS` 一个词会漏掉近一半内容。收集代理检索时按以下矩阵逐组覆盖；注意 "RIS" 在医学里还有 radiology information system、在金融里是 return index，检索时始终与通信词（beamforming/6G/surface）同现以避免歧义。

## 1. 核心同义词（必搜）

| 中文 | 英文 |
|---|---|
| 可重构智能表面 | reconfigurable intelligent surface, RIS |
| 智能反射面 | intelligent reflecting surface, IRS |
| 智能超表面 | intelligent metasurface, smart metasurface |
| 可重构超表面 | reconfigurable metasurface, reconfigurable holographic surface, RHS |
| 智能无线环境 | smart radio environment, SRE |
| 大规模动态可编程表面 | large intelligent surface, LIS |

## 2. 结构变体（按子主题取舍）

| 变体 | 英文全称 | 备注 |
|---|---|---|
| STAR-RIS | simultaneously transmitting and reflecting RIS | 透射+反射双面 |
| 有源 RIS | active RIS, amplifying RIS | 含放大器件 |
| 超对角 RIS | beyond-diagonal RIS, BD-RIS | 2023 起热点 |
| 透射式 RIS | transmissive RIS, refractive RIS | 国内产品常用 |
| 堆叠智能超表面 | stacked intelligent metasurface, SIM | 近场波束域热点 |
| 动态超表面天线 | dynamic metasurface antenna, DMA | 相邻领域 |
| 全息 MIMO | holographic MIMO, HMIMO, holographic beamforming | 相邻领域 |
| 流体天线 | fluid antenna system, FAS | 相邻领域，全景模式单独归组 |
| 双基地/混合 RIS | hybrid RIS, active-passive RIS | — |

## 3. 应用组合词（子主题聚焦时扩展检索）

- 通感一体化：`RIS ISAC`、`RIS integrated sensing and communication`、`RIS DFRC`、`RIS radar`
- 近场：`near-field RIS`、`RIS beam focusing`
- 定位：`RIS localization`、`RIS positioning`、`RIS sensing`
- 安全：`RIS physical layer security`、`RIS jamming`
- 能效/供能：`RIS wireless power transfer`、`RIS SWIPT`、`RIS energy efficiency`
- 无人机/卫星：`RIS UAV`、`RIS NTN`、`RIS LEO satellite`
- AI：`RIS deep reinforcement learning`、`RIS channel estimation deep learning`、`latent space RIS`

## 4. 标准化与工业界用词（与学术界不同！）

工业界/标准组织的文档**很少用 "RIS" 这个词**，检索标准与新闻时必须用：

| 用词 | 场景 |
|---|---|
| smart repeater / 智能中继 | 中国运营商与设备商新闻中最常用 |
| network-controlled repeater, NCR | 3GPP Rel-18 正式立项的放大转发设备（非 RIS 本体，但同属"低成本覆盖增强"赛道，需区分） |
| reconfigurable surface / reconfigurable metasurface | 3GPP 6G 讨论与 ETSI 文档 |
| intelligent surface（不带 reconfigurable） | 厂商新闻稿 |
| 可调超表面 / 数字可编程超表面 | 中文新闻 |
| dynamic beam coverage / dynamic coverage | 运营商试验新闻 |
| passive beamforming hardware / low-cost array | 商业分析类文章 |

## 5. 中文媒体高频词

智能超表面、可重构智能表面、智能反射面、RIS 器件、超表面相控阵、透镜天线阵列、毫米波覆盖增强。

## 6. 排除词（noise 控制）

检索 IEEE/arXiv 时，`RIS` 单独命中噪声大，与下列词组合限定：
`(RIS OR IRS OR "intelligent surface" OR metasurface) AND (beamforming OR 6G OR communication OR wireless OR coverage)`
