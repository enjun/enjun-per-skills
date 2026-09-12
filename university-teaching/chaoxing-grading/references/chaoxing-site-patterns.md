---
domain: chaoxing.com
aliases: [超星学习通, 学习通, Chaoxing]
updated: 2026-09-12
note: 超星平台经验存放在本技能内（web-access 是第三方技能，更新会覆盖其 site-patterns，勿写入）
---
## 平台特征
- 教师端课程页 `mooc2-ans.chaoxing.com/mooc2-ans/mycourse/tch?...` 登录态在日常浏览器 cookie 中（2026-09-12 验证）。
- 作业列表在课程页内嵌"作业"导航；批阅列表页 `/mooc2-ans/work/mark?...&id=<作业id>`；单个学生批阅页 `/mooc2-ans/work/library/review-work?...&workId=<>&workAnswerId=<学生提交id>`（2026-09-12 验证）。
- 批阅页是单页应用：学生答案（富文本+图片）在主文档 DOM 中，评分输入框 id 为 `#score<题目id>`（placeholder "0-100"），总分输入框 `#tmpscore` 会自动同步题目分；`#comment<workAnswerId>` 为批语 textarea。给 score 框设 value 并 dispatch input/change/blur 事件后 tmpscore 自动同步（2026-09-12 验证）。
- 批阅页有**两个可见提交按钮**：`<a>` text="提交并进入下一份"（onclick=`markAction(0)`，提交并跳下一份）；`<a>` text="提交"（onclick=`markAction(1)`，仅提交、页面停留原位）。另有隐藏的 confirmHref"提交"按钮，按纯文本匹配会误中，须用 onclick 过滤（2026-09-12 DOM 验证；markAction(1) 不跳转语义经用户确认）。

## 有效模式
- 学生答案中的截图 img src 有**两个图床域名**：`p.ananas.chaoxing.com/star3/origin/<hash>` 和 `p.cldisk.com/star4/<hash>/origin.jpg`（2026-09-12 验证）。提取时必须兼容两者，只过滤 ananas 会漏掉 cldisk 图床的学生截图。
- **图片可直接下载（2026-09-12 验证，比截图快约 50 倍且为原图）**：ananas 带 chaoxing cookie（须由 CDP `Storage.getCookies` 获取，`document.cookie` 不含 HttpOnly）+ 浏览器 UA + 跟随 302；cldisk 浏览器内根本没有其 cookie，带 UA + `Referer: https://mooc2-ans.chaoxing.com/` 即可。多图可用 curl 后台任务或脚本并行下载。
- 备用查看方式：在任意 tab navigate 到图片 URL（携带登录 cookie 即可显示，ananas 会 302 到 star4/.../origin.png），再用 /screenshot 截图读取。注意视口截图会裁掉竖版/旋转照片的边缘，直下原图无此问题。
- 批阅按钮 `a.cz_py` 的 data 属性含 review-work URL，可直接提取后用 /new 打开，比模拟点击 toMarkWork() 可靠。**注意 data 是相对路径**（`/mooc2-ans/work/library/review-work?...`），打开前需拼 `https://mooc2-ans.chaoxing.com` 前缀。
- **批量提取待批名单（2026-09-12 验证）**：列表页把 `size` 参数改为 50 可一页装下全部行（31 人班级实测）；遍历 `a.cz_py`，用 `closest("ul")` 找同行 `.py_name`（姓名）与 `input.scoreInput`（value 为空 = 待批），一次拿到全部 {name, url}。
- **并行批改（2026-09-12 验证机制）**：多个 review-work 页可同时 `/new` 开多个 tab，`/eval` 并行提取互不干扰；并行提交不同 workAnswerId 互不影响。
- 评分输入框 id 不确定时，按 `input[id^=score]` 且 placeholder 含 "0-" 探测（2026-09-12 验证）。填分后用 `#tmpscore` 同步值核对是否生效（2026-09-12 验证）。
- 提取答案截图时按 `img src 含 ananas|cldisk 且 getBoundingClientRect().width > 50` 过滤，排除表情小图（2026-09-12 验证）。

## 已知陷阱
- `p.ananas.chaoxing.com` 图片：curl 无 cookie 返回 403（早期记录的"0 字节/唯一通路是截图"已过时——带 CDP cookie 后可直下）；页面内 fetch 被 CORS 拦；canvas.toDataURL 被 SecurityError 污染拦截。直下取 cookie 必须走 CDP `Storage.getCookies`（`document.cookie` 只含部分非 HttpOnly cookie，不带全可能仍 403）（2026-09-12 验证）。
- `/screenshot` 是视口截图，会裁掉超出视口或居中显示的竖版图片边缘，可能丢失照片类作业截图的关键内容（2026-09-12 卢雨欣案例：创建命令恰在裁掉区域），优先直下原图。
- 批阅列表页点"批阅"按钮（onclick=toMarkWork）不弹窗也不新开 tab，必须自己从 data 属性取 URL 打开。
- 主文档 body.innerText 不含图片信息，仅看文字会漏掉学生的实操截图，误判"没有实操证据"。
- 提交后页面自动跳到下一份学生；全部批完则跳回 `/work/mark` 批阅列表页，列表中学生状态全部为"已完成"即批改完毕（2026-09-12 验证）。多 tab 并行提交时用普通"提交"（markAction(1)）则无跳转问题；若误用"提交并进入下一份"，"下一份"按当时未批队列分配，两个 tab 可能跳到同一位学生。
- `/screenshot` 偶发 "CDP 命令超时: Page.captureScreenshot"，sleep 3 后重试同一调用即可成功（2026-09-12 多次验证）。
