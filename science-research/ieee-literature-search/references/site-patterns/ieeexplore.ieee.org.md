---
domain: ieeexplore.ieee.org
aliases: [IEEE Xplore, IEEE]
updated: 2026-09-11
---
## 平台特征
- Angular SPA，搜索/文献页均为动态渲染，需 CDP 等待 JS 执行（2026-09）
- 机构访问通过 SeamlessAccess：页头 "Institutional Sign In" → 弹窗 "Access Through <机构名>" → 学校 IdP SAML 流程（2026-09）
- 登录成功标志：页头出现 "Access provided by: <机构名>"（2026-09）
- 机构会话长期有效（SeamlessAccess 勾选记住机构 + IdP Cookie），后续访问多数免登录，先检查页头再决定是否重走认证（2026-09）

## 有效模式
- 搜索：首页搜索框（`form[role=search]` 内 input）原生 setter 填词后 `clickAt button[aria-label=Search]`，结果页 URL `search/searchresult.jsp?queryText=...`（2026-09）
- 结果列表选择器：`a.fw-bold`（2026-09-06 验证；不限标签的 `.fw-bold` 会命中 "Sign In to Save Your Search" 干扰 DIV，必须限定 a 标签）。`xpl-root-list-item` 在搜索结果页实测不存在（2026-09-06），勿再作为首选
- 文献页 PDF 入口：`a` 文本 "PDF"/"Download PDF"，href 指向 `stamp/stamp.jsp?tp=&arnumber=<id>`（2026-09）
- **文献页元数据（作者/期刊/日期）**：`window.xplGlobal.document.metadata`，含 `authors[].name`、`publicationTitle`、`publicationDate`，结构化且稳定（2026-09-11 验证）
- **文献页摘要**：`.abstract-text-content` 匹配 **2 个元素**，`[0]` 是 ~170 字符的截断预览（以 "..." 结尾），`[1]` 才是完整摘要——必须用 `querySelectorAll(".abstract-text-content")[1]`（2026-09-11 验证）
- 真实 PDF 地址：stamp 页 iframe src = `stampPDF/getPDF.jsp?tp=&arnumber=<id>&ref=`，机构登录态下可直接 fetch（2026-09-06 再次验证）
- 未登录时付费墙表现：导航到 stamp.jsp 直接重定向回 `/document/<id>` 且无 iframe（2026-09-06 验证），此时应走机构登录流程
- **PDF 落盘最稳方式**：在文献页（正常 DOM 上下文）非阻塞 fetch 缓存到 `window.__pdfBuf`，再分块（786432B，8192 步进 String.fromCharCode + btoa）提取 base64，本地解码。注意 proxy 返回格式为 `{"value":"<内层JSON字符串>"}`，需两层 JSON.parse（2026-09）

## 已知陷阱
- 文献页**没有** `script[type="application/ld+json"]`，`meta[name="citation_*"]` 标签实测为空——提取元数据不要走这两条路，用 `xplGlobal.document.metadata`（2026-09-11 验证）
- 搜索页滚动触发的动态加载会使 `a.fw-bold` 数量逐步增加，先 `/scroll` 到底部再提取可拿全前 20 条（2026-09-11 观察，默认每页 rowsPerPage=20 时首轮提取通常已完整）
- 直接导航到 getPDF.jsp 会进入 Chrome 内置 PDF 查看器，该上下文无正常 DOM，fetch+`<a download>` 触发下载会失败或被拦（2026-09）
- blob URL `<a download>` 点击（无用户手势）在 IEEE 域名下会被 Chrome 静默拦截，文件不落盘（2026-09）
- IEEE PDF 带 owner 权限标记，部分工具（如 Claude Read）误报 "password-protected"，pypdf 验证实为未加密，阅读器可正常打开（2026-09）
- React 表单（如登录页验证码）必须用 `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,"value").set` 原生 setter 赋值后 dispatch input 事件，直接 `.value=` 会在提交时被清空（2026-09）