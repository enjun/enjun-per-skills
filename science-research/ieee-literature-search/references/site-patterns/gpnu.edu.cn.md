---
domain: gpnu.edu.cn
aliases: [广东技术师范大学, GPNU, 统一身份认证]
updated: 2026-09-06
---
## 平台特征
- 学校统一认证三段式：webauth.gpnu.edu.cn（应用认证平台）→ cas.gpnu.edu.cn（CAS 登录）→ idp.gpnu.edu.cn（SAML IdP 同意页），全部完成后回跳业务站点（2026-09）
- webauth 页：`a#cas-login` 进入 CAS（2026-09）
- CAS 默认微信扫码登录，需点 `.index-tip-kPsHR`（返回账号登录）或 `.index-type_box-1R6Y0`（切换账号登录）切换到账密表单（2026-09）
- 账密表单：`#userName` `#password` `#captcha`（算术验证码，题目为图片样式数字，截图识别即可），浏览器常已记住账密自动填充（2026-09）

## 有效模式
- 验证码填入必须用原生 value setter + dispatch input/change 事件（React 表单）（2026-09）
- IdP 同意页两步：`button[name=_eventId_proceed]`（声明页需先勾选 checkbox，用原生 checked setter；信息发布页直接点接受）。若此前已同意过，两页可能被跳过、直接回跳业务站点（2026-09-06 验证）
- 全程 clickAt 真实鼠标事件，总耗时约 30-40 秒（2026-09-06 再次验证）

## 已知陷阱
- CAS 登录后停在本页不动 = 验证码未被表单接受（React 清空了程序化赋值），需原生 setter 重填（2026-09）
- CAS 扫码/账号切换按钮（`.index-type_box-1R6Y0` 等）用 el.click() 完全无效（表单不渲染、DOM 无 input），必须用 clickAt 真实鼠标事件（2026-09-06 验证）
