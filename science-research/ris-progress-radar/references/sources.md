# 信息源速查（访问方式与已知 URL）

简报模板（collection-briefs.md）定义检索策略；本文件是具体锚点：已知 URL、访问方式、历史踩坑。标注 ⚠ 的是未验证或易变项，使用时现场确认。

## 学术

| 源 | 访问方式 | 备注 |
|---|---|---|
| IEEE Xplore | `ieee-literature-search` 技能（搜索免登录） | 顶刊清单见 Brief A；高级检索支持发布日期过滤 |
| arXiv eess.SP | WebFetch `arxiv.org/list/eess.SP/recent` 只见最近；历史用 WebSearch `site:arxiv.org` | cs.IT 同理 |
| IEEE 会议论文集 | IEEE Xplore 侧栏 Conference 过滤 | ICC/GLOBECOM 论文集上线通常滞后会议 2-8 周 |

## 标准化

| 源 | URL / 方式 | 备注 |
|---|---|---|
| 3GPP FTP | `3gpp-access` 技能（curl + UA，WebFetch 不可用） | 铁律见该技能；SA 全会目录被封走 portal.3gpp.org |
| 3GPP portal | portal.3gpp.org | SP- 文档检索兜底 |
| ETSI ISG RIS | `etsi.org/technologies/reconfigurable-intelligent-surfaces` ⚠ | ISG 2023-11 结束；查后续白皮书/报告 |
| ITU-R IMT-2030 | `itu.int` 检索 IMT-2030 ⚠ | 框架建议书 RIS 列为候选技术 |
| IMT-2030(6G)推进组 / 智能超表面技术联盟 | 中文检索；imt2030.cn ⚠ | RISTA 峰会每年举办 |
| CCSA | ccsa.org.cn 检索 ⚠ | 立项公告在 TC5 等 |
| 中国信通院 | caict.ac.cn | 白皮书/蓝皮书发布 |

## 工业界

| 源 | 访问方式 | 备注 |
|---|---|---|
| 厂商 newsroom | WebSearch `site:<域> smart repeater` 等 | Huawei huawei.com/en/news、ZTE zte.com.cn/global/about/media、Ericsson ericsson.com/en/newsroom、Nokia nokia.com/about-us/newsroom、NTT DOCOMO docomo.ne.jp/english/info/media/（RIS 试验报道多）⚠ |
| 中国运营商 | 中文检索（新闻通稿多经媒体发布） | 集采/招标看中国移动/电信/联通采购网 ⚠ |
| 创业公司 | 检索为主 | Greenerwave greenerwave.com、Pivotal Commware pivotalcommware.com ⚠ 以检索发现为准 |
| 行业媒体 | C114.com.cn、cww.net.cn、lightreading.com、rcrwireless.com、6gworld.com、mobileworldlive.com | B 类信源主力 |
| 展会日历 | MWC 巴塞罗那 2-3 月 / MWC 上海 6 月 / PT Expo 北京 9 月底 / GLOBECOM 12 月 / ICC 5-6 月 | 判断窗口覆盖 |

## 实测验证记录（2026-10-07 全景运行）

可正常访问（优先走这些）：
- morningstar.com / microwavejournal.com：转载厂商新闻稿全文（Business Wire 类稿源的可靠镜像）
- newsroom.kddi.com、investors.airgain.com、news.pedaily.cn（投融资）、telecomtalk.info（印度运营商）
- risalliance.com（RISTA 官网，含白皮书库与新闻栏）、ptexpo.com.cn（PT 展官网）
- m.c114.com.cn：WebFetch 被拦但 **curl 直连可读**
- ieeexplore.ieee.org/document/<ID>/：机构登录态下文献页可读（GPNU）

已确认被拦/受限（直接走替代路径，别浪费时间重试）：
- WebFetch 被拦：zte.com.cn、docomo.ne.jp、voicendata.com、news.qq.com、xxf315.com → 改 WebSearch 快照核对
- b2b.10086.cn（中国移动招标网）：公示不可程序化获取 → 集采中标信息靠媒体报道，系统性盲区须在报告注明
- portal.3gpp.org TDoc 列表：Telerik 动态页无法脚本化 → 走 FTP
- itu.int WP5D 会议文档：仅 TIES 会员可见 → 靠第三方报道交叉确认
- CCSA 官网会议日历：动态加载 → 靠 C114 等会议报道

## 已知踩坑（2026-10-07 实测迭代）

- **IEEE Xplore 检索 URL 不支持日级日期过滤**：`ranges=YYYYMMDD_YYYYMMDD_Year` 参数页面显示已应用但实际返回 0 结果。窗口内总量用"最新排序 + 抽样日期夹逼"估算；单篇核实逐篇打开文献页看 "Date of Publication"。`/rest/search` 内部 API 从页面 fetch 返回非 JSON，弃用。2026 年 9-10 月 PIMRC 会议大批 RIS 论文集中入库，期刊精选需加 `ContentType:Journals` 剔除会议论文。
- **WebFetch 对部分中/日文域名被"域名安全验证"拦截**（实测：zte.com.cn、c114.com.cn、docomo.ne.jp、voicendata.com、news.qq.com 等）：先试 curl 直连（C114 实测 curl 可用），不行再退 WebSearch 快照核对日期与要点，条目标注"原文访问受限"。
- **中国移动采购与招标网（b2b.10086.cn）公示无法程序化检索**：集采中标结果这一最硬商业化信号存在系统性盲区，报告中要注明；可搜媒体报道补偿。
- **portal.3gpp.org 的 TDoc 标题列表是 Telerik 动态页**，无法脚本化——RAN 会议文稿逐篇排查改走 FTP：列 Docs/ 目录文件名 grep + 下载会议纪要（`Report/Draft_Minutes_report_RAN1%23NNN_vXXX.docx` 可直接下载，几十万字全文 grep 关键词，是判断"某话题是否上会"的一手利器）。
- **IEEE 大批量二手转述噪声大**：学术路以 IEEE Xplore 站内检索 + arXiv API 为主，WebSearch 仅作综述交叉验证。
- **二手信源会与一手证据矛盾**：RIS Alliance 白皮书等宣传性页面声称"RIS 正随 3GPP Rel-20 推进"，与 3GPP 文档实查（Rel-20 研究无 RIS）不符——凡"标准化进展"类转述，必须回一手文档核验后才能定级 A。
- **3GPP TDoc 正文检索成本高**：会议 Docs/ 目录数百文件，先 grep 文件名，再挑目标下载转文本；一次性大批量下载易触发限流（3gpp-access 技能已记录）。
- **NTT DOCOMO 新闻稿是英文+日文双语**，RIS（他们称 reconfigurable intelligent surface / smart surface）试验历史最长，是工业界试验动态的可靠锚点。
- **中文新闻常无明确日期**：搜索引擎结果页显示的日期可能是快照日期；点进原文核对发布时间，核对不出则放弃该条或降为 C 类。
- **厂商新闻页反爬差异大**：WebFetch 失败时换 WebSearch 快照摘要确认日期与要点，标注"原文访问受限"。
