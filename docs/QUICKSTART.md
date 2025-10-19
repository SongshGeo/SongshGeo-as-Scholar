# 快速开始指南

5 分钟搞定出版物更新！

## ⚡ 最快方式

```bash
# 1. 确保依赖已安装
make install

# 2. 导出 BibTeX 到根目录
# 文件名：My-Publications.bib

# 3. 运行完整更新
make full-update
```

就这么简单！✨

## 📋 详细步骤

### 第一次使用

#### 1. 安装依赖

```bash
make install
```

这会安装：
- PyYAML
- loguru（日志系统）
- langchain, openai, pypdf（PDF 提取）

#### 2. 设置 OpenAI API Key（可选）

如果要使用 PDF 摘要提取功能：

```bash
echo 'OPENAI_API_KEY=sk-your-actual-key' > .env
```

获取 API Key：https://platform.openai.com/api-keys

### 日常使用

#### 方式 A：一键更新（推荐）

```bash
make full-update
```

这会自动：
1. ✅ 检查缺失的出版物
2. 📄 检查 PDF 覆盖率
3. 📝 重命名文件统一命名
4. 🤖 提取摘要（可选）
5. 📋 更新发表列表
6. 📊 记录所有操作

#### 方式 B：分步操作

```bash
# 1. 检查状态
make check

# 2. 检查 PDF
make check-pdf

# 3. 预览重命名（安全）
make preview-rename

# 4. 执行重命名
make rename

# 5. 提取摘要（可选）
make extract-abstracts

# 6. 更新发表列表
make update-publist
```

### 查看结果

```bash
# 查看更改
git diff

# 查看日志
make show-log

# 本地预览
make server
```

### 部署

```bash
# 快速部署
make deploy

# 或分步
make commit   # 提交
make push     # 推送（自动部署）
```

## 🎯 常见任务

### 添加新论文

```bash
# 1. 在 Zotero 中添加论文

# 2. 导出 BibTeX
#    File → Export Library → BibTeX
#    保存为 My-Publications.bib

# 3. 上传 PDF 到对应文件夹
#    content/en/publication/{key}/{key}.pdf

# 4. 运行更新
make full-update

# 5. 部署
make deploy
```

### 只更新某篇论文的摘要

```bash
# 使用脚本直接调用
poetry run python scripts/extract_abstract_from_pdf.py --key wang2025g
```

### 查看最近的操作日志

```bash
make show-log
```

### 清理旧文件

```bash
# 清理构建文件
make clean

# 清理旧日志（>3 个月）
make clean-logs
```

## ⚙️ 配置

### 环境变量（.env）

```bash
# OpenAI API Key（用于摘要提取）
OPENAI_API_KEY=sk-your-api-key
```

### 项目配置

在 `Makefile` 中修改：

```makefile
BIB_FILE := My-Publications.bib    # BibTeX 文件名
LANG := en                          # 语言（en/zh）
CONTENT_DIR := content             # 内容目录
```

## 🔍 检查清单

运行 `make full-update` 前：

- [ ] ✅ 已导出最新的 BibTeX 文件
- [ ] ✅ 新论文的 PDF 已上传
- [ ] ✅ 设置了 OpenAI API Key（如需摘要提取）
- [ ] ✅ publist 目录可访问（如需更新列表）

## 💡 提示

### 节省 API 费用

```bash
# 只处理没有摘要的论文（默认行为）
make extract-abstracts

# 限制处理数量
poetry run python scripts/extract_abstract_from_pdf.py --max-publications 5
```

### 安全第一

```bash
# 总是先用 dry-run 预览
make preview-rename

# 提交前先测试
make server
```

### 查看帮助

```bash
# 查看所有命令
make help

# 查看脚本帮助
poetry run python scripts/check_missing_publications_enhanced.py --help
```

## 📖 更多文档

- **完整工作流**：[`WORKFLOW.md`](WORKFLOW.md)
- **项目总览**：[`README.md`](README.md)
- **脚本文档**：[`scripts/README.md`](scripts/README.md)
- **更新日志**：[`scripts/CHANGELOG.md`](scripts/CHANGELOG.md)

## ❓ 遇到问题？

### 常见问题

**Q: 找不到 My-Publications.bib**
```bash
# 确认文件在项目根目录
ls My-Publications.bib
```

**Q: OpenAI API 错误**
```bash
# 检查 .env 文件
cat .env

# 测试 API Key
poetry run python scripts/extract_abstract_from_pdf.py --key test --dry-run
```

**Q: XeLaTeX 编译失败**
```bash
# 手动编译查看错误
cd publist
xelatex main.tex
```

查看完整故障排查：[`WORKFLOW.md#故障排查`](WORKFLOW.md#🐛-故障排查)

---

**准备好了吗？**

```bash
make full-update
```

就这么简单！🚀

