---
name: chaoxing-grading
description: 批改超星学习通(Chaoxing)课程作业。从批阅列表一次取全待批名单，按波次并行批改（每波并行打开多个学生批阅页，并行识图验证实操、并行填分提交），直至批完；单件或兜底时串行循环。当用户要求批改/批阅/打分超星作业时使用。
---

# 超星作业批改

批改超星学习通教师端作业：逐个查看学生提交（文字+截图），从截图验证实操后打分提交，直到待批列表清空。

## 前置

1. 必须加载 web-access skill 并完成 CDP 前置检查，同时读取本技能的平台经验 `references/chaoxing-site-patterns.md`。**web-access 是第三方技能，更新会覆盖个人修改——超星经验只存本技能内，不写入 web-access 的任何文件**。向用户展示自动化操作须知。
2. 教师端登录态在日常浏览器 cookie 中，无需额外登录。
3. 所有操作在**自己新建的后台 tab** 中进行。用户可能同时在手动批改（处理个别学生），**绝不操作用户正在编辑的 tab**；结束时只关自己建的 tab。
4. 先向用户确认三件事：**①作业页面的网址链接；②批改哪个作业；③使用哪个评分标准**。评分标准按课程分类存放于本技能 `references/rubrics/`，一门课一个文件，现有 `python.md`（Python语言程序设计）；用户给出新课程的评分标准时，确认后保存为新文件以便复用。是否写评语、满分/最低分约定以所选课程文件内的约定为准。

## 工作方式选择

- **并行波次（默认，≥2 名待批学生）**：每波同时打开 K=4 个批阅 tab，并行提取/识图/提交。验证过：并行 `/new`、并行 `/eval`、并行提交（不同 workAnswerId 互不冲突）均正常（2026-09-12）。
- **串行循环（兜底）**：仅 1 名待批学生，或并行某环节失败时使用：一个批改 tab 提交后自动跳下一份，一个看图 tab 备用 navigate+screenshot。

tab id 从 `/new` 返回值获取，后续所有请求用 `?target=<tabId>` 指定。

## 并行波次批改流程

`一次取全待批名单 → 每波 K 人：并行开 tab → 并行提取 → 并行直下识图 → 并行填分提交 → 关闭本波全部 tab`，直到待批清空。

### 1. 一次取全待批名单

列表页 URL 把 `size` 参数改为 50（一个教学班一页装下；超 50 人再循环 pages）。打开后执行：

```js
(() => {
  const out = [];
  for (const a of document.querySelectorAll("a.cz_py")) {
    const row = a.closest("ul") || a.closest("tr") || a.parentElement;
    const name = row ? row.querySelector(".py_name") : null;
    const score = row ? row.querySelector("input.scoreInput") : null;
    if (score && score.value.trim() === "") out.push({name: name ? name.textContent.trim() : "?", url: a.getAttribute("data")});
  }
  return JSON.stringify({pending: out.length, list: out});
})()
```

- **data 属性是相对路径**（`/mooc2-ans/work/library/review-work?...`），打开前拼 `https://mooc2-ans.chaoxing.com` 前缀。
- `pending: 0` 即全部批完，直接进入收尾。
- 该名单是本波的输入，不需要模拟点击任何按钮。

### 2. 每波处理 K=4 名学生

**2a. 并行开批阅 tab**（一条 bash 内连续 `/new`，URL 走 POST body，记下各 targetId；K≤6 避免触发反爬）。

**2b. 并行提取学生信息**（后台任务 + wait，一段 bash 同时发出）：

```bash
eval_js='<第2节提取JS>'
( curl -s -X POST "http://localhost:3456/eval?target=<tab1>" -d "$eval_js" > /tmp/s1.json & \
  curl -s -X POST "http://localhost:3456/eval?target=<tab2>" -d "$eval_js" > /tmp/s2.json & \
  curl -s -X POST "http://localhost:3456/eval?target=<tab3>" -d "$eval_js" > /tmp/s3.json & \
  curl -s -X POST "http://localhost:3456/eval?target=<tab4>" -d "$eval_js" > /tmp/s4.json & wait )
```

提取内容同串行流程第 2 节（student/imgs/scoreInputId/answerText）。作业要求第一位学生时通读一次，共用。

**2c. 并行直下全部截图并识图**：每位学生调用一次 fetch-images.mjs 并 **`--out` 按学生分目录**（脚本默认文件名都从 img1 开始，同目录会互相覆盖），多个调用后台并行：

```bash
( node ".../fetch-images.mjs" <学生1的img url...> --out /tmp/hw_s1 > /tmp/dl1.json 2>&1 & \
  node ".../fetch-images.mjs" <学生2的img url...> --out /tmp/hw_s2 > /tmp/dl2.json 2>&1 & wait )
```

然后在**同一消息中并行 Read 全部学生的全部图片**（4 人 ×3 图 ≈ 12 张一次读完）。

**2d. 打分**：逐生按评分校准给分，向用户汇报本波每人截图验证结论 + 得分理由（一两句）。

**2e. 并行填分提交**：每个 tab 用**各自的 scoreInputId** 构造 JS，后台并行提交。并行模式**必须点普通"提交"按钮（onclick 含 `markAction(1)`）**，绝不能点"提交并进入下一份"（markAction(0)，会跳到未知学生）：

```js
(() => {
  const s = document.querySelector("#score<QUESTION_ID>");
  s.focus(); s.value = "<SCORE>";
  s.dispatchEvent(new Event("input", {bubbles:true}));
  s.dispatchEvent(new Event("change", {bubbles:true}));
  s.dispatchEvent(new Event("blur", {bubbles:true}));
  const t = document.querySelector("#tmpscore").value;
  const btn = [...document.querySelectorAll("a")].find(a => /markAction\(1\)/.test(a.getAttribute("onclick")||"") && a.getBoundingClientRect().width > 0);
  if (!btn) return JSON.stringify({score: s.value, total: t, btn: "not found"});
  btn.click();
  return JSON.stringify({score: s.value, total: t, btn: "clicked"});
})()
```

```bash
( curl -s -X POST "http://localhost:3456/eval?target=<tab1>" -d '<学生1的JS>' > /tmp/sub1.json & \
  curl -s -X POST "http://localhost:3456/eval?target=<tab2>" -d '<学生2的JS>' > /tmp/sub2.json & wait )
```

核对每个返回 `"btn":"clicked"` 且 `total === score`。不同 tab 提交的是不同 workAnswerId，服务端互不影响，可安全并行；普通"提交"不跳转，页面停留在当前学生。

**2f. 关闭本波全部 tab**。并行用普通"提交"后页面停留原位不跳转，每波 tab 一次性使用后关闭即可。**并行 tab 里绝不能点"提交并进入下一份"**——会跳到未知学生，造成批错对象或重复批改。

### 3. 收尾

所有波次结束后，回到列表页（size=50）重跑第 1 节提取，`pending: 0` 即批完；进入"批改完成总结"。

## 串行循环（兜底）

`提取当前学生信息 → 逐张查看全部截图验证实操 → 按校准打分 → 填分提交 → 自动进入下一份 → 提取下一位`，循环到列表清空。看图 tab 仅在直下脚本失败退回 navigate+screenshot 时使用。

### 1. 从批阅列表进入（串行首位学生；并行模式用上文「一次取全待批名单」）

批阅列表 URL 形如 `/mooc2-ans/work/mark?courseid=...&clazzid=...&id=<作业id>&status=0`（可从课程页"作业"导航进入）。列表页每个待批学生有"批阅"按钮：

- **陷阱**：模拟点击"批阅"（onclick=toMarkWork）无任何反应。
- **有效模式**：从 `a.cz_py` 元素的 data 属性直接提取 review-work 完整 URL（保留全部参数），用 `/new` 打开（URL 走 POST body）。

若属性名不确定，遍历元素 attributes 找含 `review-work` 的值。

### 2. 提取学生信息（共用）

在批改 tab 上执行：

```js
(() => {
  const stu = document.querySelector("#stuRealName");
  const imgs = [...document.querySelectorAll("img")].filter(i => /ananas|cldisk/.test(i.src||"") && i.getBoundingClientRect().width > 50).map(i => i.src);
  const scoreInput = [...document.querySelectorAll("input[id^=score]")].find(i => i.placeholder && i.placeholder.includes("0-"));
  const body = document.body.innerText;
  const seg = body.slice(body.indexOf("学生答案："), body.indexOf("正确答案："));
  return JSON.stringify({student: stu ? stu.value : "?", imgCount: imgs.length, imgs, scoreInputId: scoreInput ? scoreInput.id : "?", answerText: seg.slice(0,1500)});
})()
```

curl 调用（URL 含 query 必须走 POST body；`-d` 传 JS）：

```bash
curl -s -X POST "http://localhost:3456/eval?target=<批改tab>" -d '<上述JS>'
```

- 作业要求在页面文字"学生答案："之前的部分，第一位学生时通读一次，后续学生共用同一要求。
- `answerText` 只是文字部分；**body.innerText 不含图片**，实操证据全在 `imgs` 里。
- `width > 50` 过滤表情小图。
- 评分输入框 id 形如 `#score<题目id>`，用提取到的 `scoreInputId`。

### 3. 逐张查看截图（共用；核心步骤，不可跳过）

**判断学生是否实际操作，唯一依据是提交的运行截图**，不能凭文字里的路径/版本来推断。每张截图都要看。

**首选：脚本并行直下（毫秒级、原图分辨率）**：

```bash
node "C:/Users/hp/.claude/skills/chaoxing-grading/scripts/fetch-images.mjs" <img-url1> <img-url2> ...
```

- 脚本自动从浏览器 CDP（DevToolsActivePort）取全量 cookie 供 ananas 图床（curl 无 cookie 是 403），cldisk 图床只需 UA+Referer；全部 URL **并行下载**，打印本地路径 JSON。
- 随后把多个本地文件**在同一消息中并行 Read** 识图；下一位学生的提取调用可与当前识图批量并发。
- 直接下载是原图，比视口截图更清晰，且不会像截图那样裁掉竖版/旋转照片的边缘（曾致证据漏看）。

**备用：tab navigate + screenshot**（脚本失败时，如浏览器调试端口未开）：

```bash
curl -s -X POST --data-raw '<img-url>' "http://localhost:3456/navigate?target=<看图tab>" && sleep 2 && curl -s "http://localhost:3456/screenshot?target=<看图tab>&file=C:/Users/hp/AppData/Local/Temp/hw_<姓名缩写><序号>.png"
```

**陷阱**：ananas 图片 curl 无 cookie 返回 403（带 CDP 取出的 cookie + UA + `-L` 跟随 302 即 200）；cldisk 图床无 cookie 但带 UA + Referer 即 200；页面内 fetch 被 CORS 拦、canvas.toDataURL 被 SecurityError 拦，这两条死路不必再试。`document.cookie` 拿不到 HttpOnly cookie，必须走 CDP `Storage.getCookies`。

对照作业要求逐项核对截图证据；证据核对清单按课程维护在评分标准文件中（如 `references/rubrics/python.md`）。

## 评分标准（按课程）

评分标准按课程分类，存放于本技能 `references/rubrics/`，一门课一个文件；批改前加载用户选定的课程文件并遵循其中全部约定（权重、档位、满分/最低分、是否写评语、证据核对清单）。

- 现有：`references/rubrics/python.md` —— Python语言程序设计
- 用户给出新课程的评分标准时，确认后保存为 `references/rubrics/<课程>.md` 再开始批改

不论哪门课，打分前都向用户简要汇报：每位学生截图验证结论 + 得分理由（一两句即可）。

### 填分提交（共用）

在批改 tab 上执行（替换 `<QUESTION_ID>` 和 `<SCORE>`）：

```js
(() => {
  const s = document.querySelector("#score<QUESTION_ID>");
  s.focus(); s.value = "<SCORE>";
  s.dispatchEvent(new Event("input", {bubbles:true}));
  s.dispatchEvent(new Event("change", {bubbles:true}));
  s.dispatchEvent(new Event("blur", {bubbles:true}));
  const t = document.querySelector("#tmpscore").value;
  const btn = [...document.querySelectorAll("a")].find(a => a.textContent.trim() === "提交并进入下一份" && a.getBoundingClientRect().width > 0);
  if (!btn) return JSON.stringify({score: s.value, total: t, btn: "not found"});
  btn.click();
  return JSON.stringify({score: s.value, total: t, btn: "clicked"});
})()
```

- 页面上有两个**可见**提交按钮：**"提交并进入下一份"（onclick=`markAction(0)`）**与**普通"提交"（`markAction(1)`）**；另有一个隐藏的 confirmHref"提交"，按文本匹配会误中，必须按 onclick 过滤。串行用前者（自动进入下一份）；**并行必须用普通"提交"**（页面不跳转）。
- 必须 dispatch input/change/blur 三个事件，`#tmpscore` 会自动同步，返回值中核对 `total === score`。
- 不写评语时，评语框 `#comment<workAnswerId>` 留空即可。
- 串行提交后页面自动跳到下一份，sleep 5 再提取下一位；并行提交后停留原页，波末关闭 tab。

### 收尾判断（串行；并行见流程第 3 节）

- 提取返回全空时：先 sleep 3 重试一次；仍空则检查批改 tab 的 URL——若已跳回 `/work/mark` 列表页，说明**全部批完**，用 `/eval` 核对列表中所有学生状态为"已完成"后收尾。
- `curl -s "http://localhost:3456/close?target=<tabId>"` 关闭自己建的两个 tab，保留用户 tab。

## 批改完成总结（共用）

全部批完后，向用户输出一份简要总结，方便审阅：

1. **分数分布**：各档位人数（如 `95×10、93×8…`），可附平均分。
2. **本次评分依据**：简要复述实际采用的评分标准——实操截图验证为主、文字说明次之、满分/最低分约定、用户给定的特殊标准。
3. **最高分**：学生姓名 + 分数 + 理由（哪些证据使其进入最高档）。
4. **最低分**：学生姓名 + 分数 + 理由（缺失什么证据导致最低档）。
5. **备注**：用户手动改过分的学生、证据存疑或建议复核的情况（如有）。

## 已知陷阱汇总

| 症状 | 处理 |
|------|------|
| 点击"批阅"按钮无反应 | 从 `a.cz_py` 的 data 属性取 URL 直接打开 |
| **学生截图提取为 0** | **先查域名：截图可能托管在 `p.ananas.chaoxing.com` 或 `p.cldisk.com`，只过滤 ananas 会漏图**（2026-09-12 卢雨欣因此被误判纯文字打 80，实际 3 张完整截图）。提取正则必须兼容两个域名；仍为 0 时再滚动页面排除懒加载 |
| 图片直下 403 | ananas 需带 CDP 取出的 cookie（`document.cookie` 不含 HttpOnly）+ UA；cldisk 只需 UA+Referer；脚本已封装 |
| 脚本连不上 CDP | 浏览器未开远程调试时退回 tab navigate + screenshot |
| `/screenshot` 报 "CDP 命令超时: Page.captureScreenshot" | sleep 3 后重试同一调用，均能成功 |
| 提取学生信息返回全空 | 先重试；再查是否已跳回列表页（批完了） |
| URL 含 query 的请求失败 | URL 一律走 POST `--data-raw` body |
| 评分框填了值但没生效 | 必须依次 dispatch input/change/blur 事件 |
| 并行模式误点"提交并进入下一份" | 该按钮（markAction(0)）会跳到未知学生，可能批错/重复对象——**并行只用普通"提交"（onclick 含 markAction(1)）**；页面上还有隐藏的 confirmHref"提交"，勿按纯文本匹配 |
| 多位学生截图下到同一目录互相覆盖 | fetch-images.mjs 文件名都从 img1 开始，必须 `--out` 按学生分目录 |
| 从列表 data 属性打开 review 页 404 | data 是相对路径（`/mooc2-ans/...`），需拼 `https://mooc2-ans.chaoxing.com` 前缀 |
| 班级超 50 人名单不全 | size=50 仍分页时循环 pages 取全，再开始波次 |
