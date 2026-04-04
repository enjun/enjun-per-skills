---
name: youdaonote
description:
  有道云笔记操作技能。通过 youdaonote CLI 操作有道云笔记：浏览目录结构、读取笔记、创建笔记、更新笔记、搜索笔记、网页剪藏、管理待办等。
  触发场景：用户要求查看/读取有道云笔记、列出目录、搜索笔记内容、创建或编辑笔记、剪藏网页到笔记、管理待办事项。
metadata:
  version: "1.0.0"
---

# youdaonote Skill

通过 `youdaonote` CLI 操作有道云笔记，所有操作在终端完成，无需打开客户端。

## 前置检查

首次使用前确认 CLI 可用：

```bash
which youdaonote || where youdaonote
youdaonote check
```

若提示 `API Key 未配置`，引导用户执行：

```bash
youdaonote config set apiKey YOUR_API_KEY
```

API Key 获取方式：打开 [有道云笔记 MCP 控制台](https://note.youdao.com/mcp)，登录后创建。

## 命令速查

| 操作 | 命令 |
|------|------|
| 列出目录/笔记 | `youdaonote list [-f <目录ID>]` |
| 读取笔记内容 | `youdaonote read <fileId>` |
| 创建笔记 | `youdaonote create -n "标题" -c "内容" [-f <目录ID>]` |
| 创建笔记(从文件) | `youdaonote create -n "标题" --file <path> [-f <目录ID>]` |
| 更新笔记(仅.md) | `youdaonote update <fileId> -c "新内容"` |
| 更新笔记(改标题) | `youdaonote update <fileId> -n "新标题"` |
| 更新笔记(从文件) | `youdaonote update <fileId> --file <path>` |
| 删除笔记 | `youdaonote delete <fileId>` |
| 重命名笔记 | `youdaonote rename <fileId> "新名称"` |
| 移动笔记 | `youdaonote move <fileId> <目标目录ID>` |
| 搜索笔记 | `youdaonote search <关键词>` |
| 最近收藏 | `youdaonote recent [-l 条数] [-c]` |
| 网页剪藏 | `youdaonote clip <URL> [-f <目录ID>]` |
| 保存剪藏数据 | `youdaonote clip-save --file <json文件>` |
| 保存任意类型笔记 | `youdaonote save --file <json文件>` |

## 目录导航

有道云笔记是树形目录结构，根目录 ID 为 `0`。

导航步骤：
1. `youdaonote list` 查看根目录，找到目标文件夹 ID
2. `youdaonote list -f <目录ID>` 递归进入子目录
3. 找到目标笔记后用 `youdaonote read <fileId>` 读取

分页：当目录内容较多时，用 `-l <上一页最后一条ID>` 获取下一页。

## 笔记操作

### 创建笔记

```bash
# 简单笔记
youdaonote create -n "标题" -c "正文内容"

# 保存到指定目录
youdaonote create -n "标题" -c "内容" -f <目录ID>

# 从文件创建
youdaonote create -n "标题" --file /path/to/content.md -f <目录ID>
```

### 更新笔记

仅支持 `.md` 文件类型的笔记。如果笔记是 `.note` 格式，无法用 `update` 命令修改。

```bash
# 更新内容
youdaonote update <fileId> -c "新内容"

# 同时改标题
youdaonote update <fileId> -n "新标题" -c "新内容"

# 从文件更新
youdaonote update <fileId> --file /path/to/new-content.md
```

### 保存任意类型笔记（Markdown、思维导图等）

```bash
# 先准备 JSON 文件
# 注意：必须用 UTF-8 编码保存

# Markdown 笔记
youdaonote save --file note.json
# JSON 格式: {"title": "笔记.md", "type": "md", "content": "# 标题\n正文"}
```

### 保存剪藏数据

```bash
# JSON 格式: {"title": "标题", "bodyHtml": "<p>正文</p>", "sourceUrl": "https://example.com", "images": []}
youdaonote clip-save --file clip.json
```

## 网页剪藏

```bash
# 剪藏到默认目录（我的资源/收藏笔记）
youdaonote clip "https://example.com/article"

# 剪藏到指定目录
youdaonote clip "https://example.com/article" -f <目录ID>
```

**Windows 注意**：URL 中含 `&` 时必须用双引号括起整个 URL。

## 待办管理

```bash
# 列出待办
youdaonote todo list [-g <分组ID>]

# 创建待办
youdaonote todo create -t "待办标题" -c "详细内容" -d 2025-12-31 [-g <分组ID>]

# 更新待办
youdaonote todo update --done          # 标记完成
youdaonote todo update --undone        # 标记未完成
youdaonote todo update -t "新标题" -c "新内容"

# 删除待办
youdaonote todo delete <todoId>

# 分组管理
youdaonote todo groups
youdaonote todo group-create "分组名"
youdaonote todo group-rename <groupId> "新名称"
youdaonote todo group-delete <groupId>  # 同时删除分组下所有待办
```

## 搜索

```bash
youdaonote search "关键词"
```

搜索结果包含笔记 ID 和标题，可用 `read` 命令进一步读取内容。

## 常见问题

| 现象 | 解决方案 |
|------|---------|
| 找不到 `youdaonote` | 未配置 PATH，或未安装 |
| `API Key 未配置` | `youdaonote config set apiKey YOUR_KEY` |
| `update` 失败 | 仅支持 .md 文件，.note 格式不支持 |
| Windows URL 含 `&` 报错 | 用双引号括起整个 URL |
| JSON 乱码 | 用 UTF-8 编码保存文件，或先 `chcp 65001` |
| `clip-save` 报缺少字段 | 确保 JSON 含 `title`、`bodyHtml`、`sourceUrl` |
| `save` 报缺少字段 | 确保 JSON 含 `title`、`content` |

## 输出格式

所有命令默认输出人类可读的文本格式。部分命令支持 `--json` 选项输出 JSON，适合程序化处理：

- `youdaonote recent --json`
- `youdaonote clip --json`
- `youdaonote todo list --json`
- `youdaonote todo groups --json`
- `youdaonote check --json`
- `youdaonote config show --json`
- `youdaonote tools --json`
- `youdaonote call <tool> [args] --json`

## 注意事项

- **文件夹不可删除/移动/重命名**：`delete`、`move`、`rename` 仅支持笔记，不支持文件夹
- **update 仅限 .md**：`.note` 格式的笔记无法通过 CLI 更新，只能删除重建或通过客户端编辑
- **目录 ID 格式**：可能是 `WEB` 前缀的长 ID（如 `WEB875baca673e6f331c020616c0fbdc11a`）或纯数字/字母 ID
- **根目录 ID 为 `0`**：`youdaonote list` 等同于 `youdaonote list -f 0`
