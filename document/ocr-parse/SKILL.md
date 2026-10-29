---
name: ocr-parse
description: 使用 Unlimited-OCR-2 把 PDF/图片解析为整理好的 Markdown 文件。当用户说"使用OCR解析"、"OCR解析这篇论文/这个PDF"、"转成md"并指向论文PDF时触发。负责：检查部署（未部署则询问装本机还是服务器）；每次调用按需启动GPU服务、用完立即关闭（不驻留显存）；交付去除页眉页脚、公式规范为$$块级的干净md。
---

# Unlimited-OCR-2 论文解析流程

## 0. 确认目标文件
用户提供 PDF 路径或 Zotero 条目 → 确定本地 PDF 绝对路径，与用户确认输出位置（默认 `D:\obsidian-data\工作\ocr-test\<文档名>_OCR.md（按论文标题命名，禁用代号）`）。

## 1. 检查是否已部署
```
ssh xej@192.168.49.10 "test -f ~/workspace/github/Unlimited-OCR/ocr_server.py && echo DEPLOYED || echo NOT_DEPLOYED"
```
- **DEPLOYED** → 进入第 2 步。
- **NOT_DEPLOYED** → 用 AskUserQuestion 询问：安装到 GPU 服务器（xej@192.168.49.10，2×RTX 3060 12GB，推荐，需免密SSH可达）还是本机 Windows（本机必须有 NVIDIA GPU；无 CUDA 环境则明确告知不可用）。按附录 A 部署，部署完自测一张图后再进入第 2 步。

## 2. 启动 OCR 服务（每次解析前，用完必须关）
```
ssh xej@192.168.49.10 "cd ~/workspace/github/Unlimited-OCR && bash start_ocr_service.sh"
```
然后轮询健康检查直到返回 JSON（模型加载约 60~90 秒，显存驻留约 6.8GB）：
```
ssh xej@192.168.49.10 "curl -s --max-time 3 http://127.0.0.1:8100/health"
```
**启动前先 `nvidia-smi` 确认 GPU0 有足够空闲显存（≥8GB）；被占用时询问用户是否等待或换卡。**

## 3. 解析 PDF（逐页 OCR + 整理）
1. 上传：`scp <本地pdf> xej@192.168.49.10:workspace/github/Unlimited-OCR/test_data/<doc>.pdf`（`<doc>` 用 ASCII 短名）
2. 服务器执行（把脚本内 `PDF = 'test_data/zheng2025_elsa.pdf'` 与 `doc` 名改成 `<doc>`，或直接 `sed -i` 改）：
   ```
   cd ~/workspace/github/Unlimited-OCR && nohup .venv/bin/python run_ocr_paper.py > ocr_paper_run.log 2>&1 &
   ```
   轮询 `grep ALL_DONE ocr_paper_run.log`（IEEE 双栏论文约 150~230 秒/页，15 页约 40 分钟；**脚本支持断点续转**，中断后重跑即从缺页继续）。轮询间隔 ≥60s，不要频繁打扰。
3. 整理（两步，必须都做）：
   ```
   .venv/bin/python build_raw.py            # 若脚本是按 zheng2025 写死的，先改成 <doc> 参数化
   .venv/bin/python fix_clean.py <doc>      # 去 header/footer/page_number、equation 块统一 $$ 化、去 <MERGE> 等杂 token
   ```

## 4. 关闭服务（解析完成或中断后都必须执行，释放 GPU）
```
ssh xej@192.168.49.10 "pkill -f 'uvicorn ocr_server'"
```
确认：`ssh xej@192.168.49.10 nvidia-smi --query-gpu=index,memory.used --format=csv` 显存回落到 <100MiB。

## 5. 交付
```
scp xej@192.168.49.10:workspace/github/Unlimited-OCR/output/<doc>_clean/<doc>.md <输出路径>
```
向用户报告：页数、总耗时、公式块数。**只交付 fix_clean 整理后的 md**；`<BLOCK>` 原始结构版仅供溯源，不要作为交付物。

## 附录 A：服务器部署步骤（2026-10-28 已全程验证）
前提与镜像：uv 在服务器 `~/.local/bin`（非交互 ssh 需 `export PATH=$HOME/.local/bin:$PATH`）；pip 走清华镜像 `https://pypi.tuna.tsinghua.edu.cn/simple`；HuggingFace 走 `HF_ENDPOINT=https://hf-mirror.com`。
1. `git clone --depth 1 https://github.com/baidu/Unlimited-OCR` 到 `~/workspace/github/`
2. `uv venv --python 3.10 .venv`
3. **torch 版本由驱动决定**：先 `nvidia-smi` 看驱动 CUDA 上限。CUDA 12.4 → 必须 `torch==2.6.0+cu124 torchvision==0.21.0+cu124 --find-links https://mirrors.aliyun.com/pytorch-wheels/cu124`；更高驱动才能装 PyPI 默认新 torch。**SGLang 官方 wheel 硬锁 torch==2.13.0，驱动 CUDA<12.6 装不上 → 走 Transformers 路径**（本技能即 Transformers 路径）。
4. `uv pip install -p .venv/bin/python transformers==4.52.1 tokenizers==0.21.4 addict einops easydict pymupdf fastapi "uvicorn[standard]" python-multipart`
5. `HF_ENDPOINT=https://hf-mirror.com hf download baidu/Unlimited-OCR-2 --local-dir models/Unlimited-OCR-2`（约 6.5G；wheel/ 目录里的 sglang wheel 本路径用不到）
6. 写 `ocr_server.py`（FastAPI：`GET /health`；`POST /ocr` multipart 传图返回 `{ok,elapsed_s,text}`，模型 bf16 单卡加载 + threading.Lock 串行推理）和 `start_ocr_service.sh`（`nohup .venv/bin/python -m uvicorn ocr_server:app --host 0.0.0.0 --port 8100`）
7. 写 `run_ocr_paper.py`（pymupdf 200dpi 逐页渲染→POST /ocr→checkpoint jsonl 断点续转→汇总）与整理脚本 `build_raw.py`、`fix_clean.py`
8. 冒烟测试：生成含已知文字的 PNG → POST /ocr → 逐字核对。
坑：HF 批量下载文件可能损坏——安装失败先 `.venv/bin/python -m zipfile -t` 校验；安装脚本的"成功"标记必须绑定真实检查（`test -d .venv/lib/python3.10/site-packages/<包名>`），禁止无条件 echo。

## 附录 B：fix_clean.py 整理规则（v5，2026-10-29 定稿）
1. 丢弃 header/footer/page_number 块；text/other 块含 e-mail: 或 Digital Object Identifier 的（IEEE 首页作者脚注）一并丢弃
2. 行内公式 "$ x $" 内侧空格必须剥除（Obsidian 对 $ 后紧跟空格不渲染）→ $x$
3. equation 块：剥掉一切 $ 字符（模型会输出 $ 独占一行甚至多层堆叠的跨行结构）→ 统一 $$ 块
4. gundam 裁剪会把多行长公式切成多块（前块 begin 无 end、后块反之）→ 相邻 $$ 块间无正文时自动缝合至配平（上限跨 3 块）
5. OCR 丢失配对定界符时：left/right 计数不均的块把 \left(X 降级为 X、\left. 丢弃（转义 \{ 形式保留）
6. 花括号配平检查必须跳过转义 { }（\left\{ 的 { 不是失衡）——栈匹配法
7. 诊断一律用 heredoc 写脚本执行，禁止 python -c 内联复杂代码；反斜杠经 JSON 层会减半，构造字面反斜杠用 chr(92)
8. 交付前验证：BAD 块数=0、ARRAY 开闭计数、用户报障点上下文 repr
