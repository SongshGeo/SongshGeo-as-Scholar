# 出版物管理工具

这两个脚本帮助你管理网站上的出版物：

1. **`check_missing_publications.py`** - 检测哪些论文在 BibTeX 文件中存在，但还没有在网站上创建对应的页面
2. **`create_publication_template.py`** - 为缺失的论文自动生成页面模板

## 使用方法

### 1. 准备你的总 BibTeX 文件

从 Zotero、Mendeley 或其他文献管理器导出你的所有论文为一个 `.bib` 文件，例如 `my_publications.bib`。

### 2. 运行检查脚本

```bash
# 基本用法 - 检查英文出版物
python check_missing_publications.py path/to/your/publications.bib

# 检查中文出版物
python check_missing_publications.py path/to/your/publications.bib --lang zh

# 显示详细信息（包括作者）
python check_missing_publications.py path/to/your/publications.bib --verbose

# 查看帮助
python check_missing_publications.py --help
```

### 3. 输出示例

```
📖 Parsing BibTeX file: my_publications.bib
   Found 25 entries in BibTeX file

📁 Checking existing publications in content/en/publication/
   Found 21 existing publication folders

⚠️  Found 4 missing publications:

================================================================================
1. [smith2023machine]
   Type:    article
   Year:    2023
   Title:   Machine learning approaches in social-ecological systems

2. [wang2024water]
   Type:    article
   Year:    2024
   Title:   Water resource management in the Yellow River Basin

...
================================================================================

📊 Summary:
   Total entries in BibTeX:     25
   Existing publication pages:  21
   Missing publication pages:   4

💡 Tip: Use 'hugo import --bibtex my_publications.bib' to create pages for missing entries
```

## 工作原理

1. **解析 BibTeX 文件**：提取所有条目的 citation key（如 `song2022b`）
2. **扫描现有页面**：检查 `content/en/publication/` 或 `content/zh/publication/` 下的文件夹
3. **比对差异**：找出在 BibTeX 中但不在网站文件夹中的条目
4. **生成报告**：列出所有缺失的出版物及其元数据

## 参数说明

- `bib_file`：必需，你的 BibTeX 文件路径
- `--lang`：可选，检查哪个语言版本（`en` 或 `zh`），默认 `en`
- `--content-dir`：可选，content 目录路径，默认 `content`
- `--verbose` / `-v`：可选，显示更多详细信息（包括作者列表）

## 注意事项

1. **Citation Key 匹配**：脚本通过 BibTeX 的 citation key（如 `@article{key, ...}` 中的 `key`）与文件夹名称匹配
2. **大小写敏感**：文件夹名称必须与 citation key 完全匹配
3. **只检测文件夹**：只要存在 `content/*/publication/key/index.md`，就认为页面已创建

## 创建缺失的页面

### 方法 1：使用配套的创建脚本（推荐）

```bash
# 先预览会创建什么（默认只创建真正缺失的论文）
python create_publication_template.py my_publications.bib --dry-run

# 确认无误后，实际创建（默认只创建真正缺失的论文）
python create_publication_template.py my_publications.bib

# 创建所有缺失的论文（包括标题匹配的）
python create_publication_template.py my_publications.bib --all

# 为中文版本创建
python create_publication_template.py my_publications.bib --lang zh
```

**脚本会自动：**
- 创建出版物文件夹（使用 citation key 作为文件夹名）
- 生成 `index.md`，包含从 BibTeX 提取的元数据
- 复制原始 BibTeX 条目到 `cite.bib`
- 自动识别作者中的 admin（你自己）

### 方法 2：使用 Hugo 学术模板导入工具

```bash
# 安装 academic 命令行工具
pip install -U academic

# 从 BibTeX 批量导入
academic import --bibtex my_publications.bib
```

### 方法 3：手动创建

为每个缺失的出版物：
1. 创建文件夹：`content/en/publication/citation_key/`
2. 创建 `index.md` 并填写元数据
3. （可选）添加 `cite.bib`、`featured.jpg` 等文件

---

## 创建模板脚本详解

### 使用方法

```bash
# 基本用法 - 创建英文出版物模板（默认只创建真正缺失的）
python create_publication_template.py path/to/your/publications.bib

# 创建中文出版物模板
python create_publication_template.py path/to/your/publications.bib --lang zh

# 预览不实际创建（干运行）
python create_publication_template.py path/to/your/publications.bib --dry-run

# 创建所有缺失的论文（包括标题匹配的）
python create_publication_template.py path/to/your/publications.bib --all

# 强制覆盖已存在的文件夹
python create_publication_template.py path/to/your/publications.bib --force

# 查看帮助
python create_publication_template.py --help
```

### 生成的文件结构

对于每个缺失的出版物，脚本会创建：

```
content/en/publication/citation_key/
├── index.md          # Hugo 页面（自动生成，包含元数据）
└── cite.bib          # BibTeX 引用（从原始文件复制）
```

### 生成的 index.md 包含

- ✅ 标题、作者、年份
- ✅ DOI（如果有）
- ✅ 摘要（如果有）
- ✅ 期刊名称
- ✅ 自动识别 admin 作者
- ✅ 符合 Hugo Blox 新格式的 `hugoblox.ids.doi`
- ✅ 空的 `links: []` 数组供后续填充

### 参数说明

- `bib_file`：必需，你的 BibTeX 文件路径
- `--lang`：可选，创建哪个语言版本（`en` 或 `zh`），默认 `en`
- `--content-dir`：可选，content 目录路径，默认 `content`
- `--dry-run`：可选，只显示会创建什么，不实际创建
- `--force`：可选，覆盖已存在的文件夹（谨慎使用）
- `--only-missing`：可选，只创建真正缺失的论文（默认行为）
- `--all`：可选，创建所有缺失的论文，包括标题匹配的
- `--include-unpublished`：可选，把尚无发表年份的草稿（submitted、under review 等）也算进来

### 使用建议

1. **先干运行**：使用 `--dry-run` 预览会创建什么
2. **检查结果**：创建后检查生成的 `index.md`，补充/修正信息
3. **添加图片**：手动添加 `featured.jpg` 或 `featured.png`
4. **完善元数据**：
   - 添加 tags
   - 设置 featured: true（如果是重点论文）
   - 关联 projects
   - 补充 links（PDF、代码、数据等）

### 工作流程示例

```bash
# 1. 从文献管理器（如 Zotero）导出所有论文
#    File -> Export Library -> Format: BibTeX -> Save as publications.bib

# 2. 检查哪些缺失
python check_missing_publications.py publications.bib --verbose

# 3. 预览会创建什么（默认只创建真正缺失的）
python create_publication_template.py publications.bib --dry-run

# 4. 实际创建（默认只创建真正缺失的）
python create_publication_template.py publications.bib

# 或者创建所有缺失的（包括标题匹配的）
python create_publication_template.py publications.bib --all

# 5. 检查生成的文件并手动完善
# 6. 测试构建
hugo server

# 7. 如果满意，提交到版本控制
git add content/*/publication/
git commit -m "Add new publications"
```

## 常见问题

**Q: 脚本显示某篇文章缺失，但我确定已经创建了？**

A: 检查文件夹名称是否与 BibTeX 中的 citation key 完全一致（包括大小写）。

**Q: 如何批量创建缺失的页面？**

A: 使用 `academic import --bibtex` 命令，或编写脚本批量生成 `index.md` 模板。

**Q: 我有多个 BibTeX 文件怎么办？**

A: 先合并成一个总文件，或多次运行脚本检查不同的文件。
