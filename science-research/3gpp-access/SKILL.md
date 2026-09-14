---
name: 3gpp-access
description: 访问 3GPP 官网（www.3gpp.org/ftp）查找、下载、解析 3GPP 规范文件。凡涉及下载 3GPP TR/TS 规范、RAN/SA 会议 TDoc（RP-/R1-/R2-/SP- 文件）、查 Rel-XX 版本状态、6G/5G/LTE 标准化调研、3gpp.org FTP 目录浏览，或用户给出 spec 编号（如 38.914、TS 22.137）想获取原文时，务必使用本技能。包含网站结构地图、curl 访问要点（UA/403/206 行为）、命名规则、目录字母序陷阱、docx/pptx 嵌套解析。
---

# 3GPP 网站访问与文件获取

3GPP 的所有一手资料（规范、技术报告、会议文稿）都在 `https://www.3gpp.org/ftp/` 这棵 FTP 目录树上，无登录即可下载。本技能沉淀了 2026-09 实战验证的访问方式、目录结构和解析方法。

## 1. 访问铁律（每条都是踩坑换来的）

- **WebFetch 不可用**：对 www.3gpp.org 会被网络策略拦截。一律用 Bash + curl。
- **必须带浏览器 User-Agent**：`-A "Mozilla/5.0 ..."`。默认 UA 返回 200，但内容是带 base64 logo 的拦截页——HTTP 码正常但拿到的不是目标数据，容易被误判为"目录为空"。
- **HEAD 一律 403**：判断文件是否存在不要用 `-I`，用 ranged GET：
  ```bash
  curl -s -A "Mozilla/5.0" -r 0-0 -o /dev/null -w '%{http_code}\n' "<url>"
  # 206 = 存在；403 = 不存在或被封
  ```
- **目录列表是 HTML**：提取条目用 `curl -s -A UA "<dir-url>" | grep -o 'href="[^"]*"'`。
- **SA 全会会议目录被封**：`/ftp/tsg_sa/TSG_SA/TSGS_NNN/` 对程序访问整体 403（列表和文件都拒绝，换完整浏览器请求头也无效）。SP- 文档改走 3GPP 门户 `https://portal.3gpp.org/` 检索；SA 的 WG 目录（如 S2-）可尝试，失败就降级。
- **download.zip 打包端点**（目录页的"一键打包"）对 HEAD 和 ranged GET 都 403：要批量文件就从目录列表逐个下载。

## 2. 目录结构地图（全部实测验证）

```
https://www.3gpp.org/ftp/
├── Specs/
│   ├── latest/Rel-XX/               某 Release 的最新批准版（XX=15,16,…）
│   ├── archive/NN_series/<spec>/    全部历史版本，按 series 分目录
│   │                                例：archive/38_series/38.914/38914-k00.zip
│   ├── latest-drafts/               已起草未定稿（全会批准后转入 archive）
│   └── YYYY-MM/                     每月快照（等价于当月的 latest+drafts）
├── tsg_ran/
│   ├── TSG_RAN/TSGR_NNN/
│   │   ├── Docs/                    RAN 全会 TDoc（RP-xxxxx.zip）
│   │   ├── Report/                  全会报告（RP-261576 之类也在 Docs 编号）
│   │   └── Agenda/
│   ├── WG1_RL1/TSGR1_NNN/           RAN1（TDoc 前缀 R1-）
│   └── WG2_RL2/ … WG4_RL4/          RAN2（R2-）、RAN3（R3-）、RAN4（R4-）
├── tsg_sa/
│   ├── TSG_SA/TSGS_NNN/             SA 全会（SP-）——程序访问被封，见铁律
│   └── WG2_Architecture/ 等         SA2（S2-）等工作组
├── workshop/YYYY-MM-DD_名称/Docs/   研讨会文稿（如 2025-03-10_3GPP_6G_WS，6GWS- 前缀）
├── Email_Discussions/               电子会议讨论
└── Information/                     会议计划等
```

找会议文件套路：先列 `TSG_RAN/` 找到目标届次目录（注意第 3 节陷阱），进 `Docs/` grep 文件名；全会报告一般在 `Report/`。

## 3. 命名规则（读懂数字和字母）

**Spec 文件名**：`38914-k00.zip` = TR 38.914，版本字母 = **Release**：

| 字母 | f | g | h | i | j | k |
|---|---|---|---|---|---|---|
| Release | 15 | 16 | 17 | 18 | 19 | 20 |

字母后两位是版本号（k00 → V20.0.0）。要最新 Rel-20 就找 `-k` 开头最大版本。

**TDoc 编号**：`前缀-YY + 序号`，**YY 是年份（20YY）**：
- `R1-26xxxxx` = RAN1 2026 年文稿；`RP-26xxxxx` = RAN 全会 2026 年文稿
- `SP-`/`S2-`/`CP-` = SA 全会/SA2/CT；`6GWS-25xxx` = 2025 年 6G 研讨会
- ⚠️ 真实踩坑：把 `RP-231443` 当成最新全会报告下载——它是 **2023** 年的文件。下载前先核对 YY。

## 4. 目录列表的字母序陷阱（最容易搞错"最新版本"）

列表按**字典序**排列：`TSGR_113` 排在 `TSGR_99` **前面**，所以 `tail` 看到的"最后几行"不是最新的。找三位数届次必须单独 grep：

```bash
curl -s -A "Mozilla/5.0" https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/ \
  | grep -o 'TSGR_1[0-9][0-9]' | sort -u | tail -3   # ← 这才是最新三届
```

RAN1 同理：`grep -o 'TSGR1_1[0-9][0-9]'`。

## 5. 常用命令模板

```bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

# 某规范的全部版本（确认最新版文件名）
curl -s -A "$UA" https://www.3gpp.org/ftp/Specs/archive/38_series/38.914/ \
  | grep -o '38914-[a-z][0-9]*\.zip' | sort -u

# 下载 TR
curl -s -A "$UA" -o 38914-k00.zip \
  https://www.3gpp.org/ftp/Specs/archive/38_series/38.914/38914-k00.zip

# 列某届全会所有 TDoc（例：RAN#112）
curl -s -A "$UA" https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/ \
  | grep -o 'RP-26[0-9]*\.zip' | sort -u

# 下载会议 TDoc（直接 zip）
curl -s -A "$UA" -O https://www.3gpp.org/ftp/tsg_ran/TSG_RAN/TSGR_112/Docs/RP-261501.zip
```

大规模探索时控制请求量：目录页可能很大，先 `grep` 过滤再看；连续请求注意别触发限流。

## 6. 解析内容：zip 套 docx 套 zip（嵌套两层！）

TR/TDoc 的 zip 里是 `.docx`/`.pptx`，而 **docx 本身又是一个 zip**——直接读外层 zip 拿到的 docx 字节里根本没有 `<w:t>` 文本，必须二次解压。

- **快速看标题/概要**（实测可用的 Python 一行命令，输出开头即标题）：
  ```bash
  python3 -c "
  import zipfile,io,re
  z=zipfile.ZipFile('38745-k00.zip')
  d=[n for n in z.namelist() if n.endswith('.docx')][0]
  xml=zipfile.ZipFile(io.BytesIO(z.read(d))).read('word/document.xml').decode('utf-8','ignore')
  print(''.join(re.findall(r'<w:t[^>]*>([^<]+)', xml))[:200])"
  ```
  （注意：`unzip -p ... | unzip -p /dev/stdin` 这类 shell 管道方案实测无效，静默无输出，不要用。）
- **完整转文本**：用本技能自带脚本（外层 zip → docx/pptx 字节 → `ZipFile(BytesIO)` → XML → 段落/文本正则；pptx 按 `ppt/slides/slideN.xml` 数值序拼接）：
  ```bash
  python3 <本技能目录>/scripts/office2txt.py 38914-k00.zip > 38.914.txt
  ```
  输入可以是 .docx/.pptx/.zip，输出 UTF-8 纯文本到 stdout。

## 7. 完整工作流示例

> 任务：调研 3GPP 6G 进展（2026-09 实战）
> 1. 列 `Specs/latest/Rel-20/` → 找到 6G 研究 TR（22.870-k00 等）
> 2. 下载并逐个 `office2txt.py` 转文本，读标题、Scope、Conclusions
> 3. grep `TSGR_1[0-9][0-9]` 确认 RAN 全会已到 #112（字典序陷阱曾导致误判为 #99）
> 4. 下载 `TSGR_112/Report/RP-261576.zip`（RAN#112 报告）→ 提取各研究项目进度、 moderated 结论
> 5. 从 `workshop/2025-03-10_3GPP_6G_WS/Docs/` 取 6GWS 总结报告
> 6. 引用规范时给链接：`https://www.3gpp.org/ftp/Specs/archive/<NN>_series/<spec>/<file>.zip`（用 ranged GET 验证 206 后再写入文档）
