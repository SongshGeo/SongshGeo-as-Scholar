# 出版物管理工具

这些脚本帮助你管理网站上的出版物：

1. **`check_missing_publications.py`** - 检测哪些论文在 BibTeX 文件中存在，但还没有在网站上创建对应的页面
2. **`check_missing_publications_enhanced.py`** - 增强版检查脚本，支持智能标题匹配和 PDF 检查
3. **`create_publication_template.py`** - 为缺失的论文自动生成页面模板
4. **`extract_abstract_from_pdf.py`** - 从 PDF 文件自动提取摘要并更新到 index.md（使用 OpenAI + LangChain）

## 安装依赖

本项目使用 poetry 管理依赖。

```bash
# 安装基础依赖（PyYAML，用于所有脚本）
poetry install

# 安装 PDF 提取功能的额外依赖
poetry install --extras pdf-extraction

# 或者使用 pip（如果不用 poetry）
pip install PyYAML
pip install langchain langchain-community langchain-openai openai pypdf python-dotenv
```

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

---

## PDF 摘要自动提取工具

### 功能说明

`extract_abstract_from_pdf.py` 使用 OpenAI 和 LangChain 自动从 PDF 文件中提取摘要并生成简短总结，然后更新到 `index.md` 文件中。

### 准备工作

1. **安装依赖**：
```bash
pip install -r scripts/requirements.txt
```

2. **设置 OpenAI API Key**：

方法 1：环境变量
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

方法 2：创建 `.env` 文件（推荐）
```bash
echo 'OPENAI_API_KEY=sk-your-key-here' > .env
```

### 使用方法

```bash
# 处理所有包含 PDF 的出版物
python scripts/extract_abstract_from_pdf.py

# 只处理特定的出版物
python scripts/extract_abstract_from_pdf.py --key wang2025g

# 预览模式（不实际修改文件）
python scripts/extract_abstract_from_pdf.py --dry-run

# 强制重新提取（即使已有摘要）
python scripts/extract_abstract_from_pdf.py --key wang2025g --force

# 完全覆盖现有 index.md（创建最小化模板，只保留摘要）
python scripts/extract_abstract_from_pdf.py --key wang2025g --override

# 处理中文出版物
python scripts/extract_abstract_from_pdf.py --lang zh

# 只处理前 5 个出版物（用于测试）
python scripts/extract_abstract_from_pdf.py --max-publications 5

# 使用不同的 OpenAI 模型
python scripts/extract_abstract_from_pdf.py --model gpt-4o

# 查看帮助
python scripts/extract_abstract_from_pdf.py --help
```

### 工作原理

1. **扫描 PDF**：在 `content/{lang}/publication/*/` 下查找 PDF 文件
2. **提取摘要**：使用 LangChain 的 PyPDFLoader 读取 PDF 前几页
3. **AI 处理**：使用 OpenAI 识别并提取摘要部分
4. **生成总结**：自动生成 1-2 句话的简短总结
5. **更新文件**：将提取的 `abstract` 和 `summary` 写入 `index.md` 的 frontmatter

### 输出示例

```
🔍 Scanning for publications with PDFs...

📚 Found 15 publications with PDFs

🤖 Initializing OpenAI (gpt-4o-mini)...

[1/15] Processing: wang2025g
      📄 Loading PDF: Wang et al. - 2025 - Anthropogenic impacts.pdf
      🤖 Extracting abstract with OpenAI...
      ✅ Abstract extracted (1234 chars)
      🤖 Generating summary...
      ✅ Summary generated (156 chars)
      ✏️  Updating abstract
      ✏️  Updating summary
      ✅ Updated index.md

...

================================================================================
📊 Summary:
   Total publications found:    15
   Successfully processed:      14
   Updated:                     12
   Skipped (already has data):  2
   Errors:                      1

✅ Files updated successfully!
💡 Review the changes and commit if satisfied:
   git diff content/en/publication/
```

### 参数说明

- `--key`：只处理指定的出版物（使用 citation key）
- `--lang`：语言版本（`en` 或 `zh`，默认 `en`）
- `--content-dir`：content 目录路径（默认 `content`）
- `--model`：使用的 OpenAI 模型（默认 `gpt-4o-mini`）
- `--dry-run`：预览模式，不实际修改文件
- `--force`：强制重新提取，即使已有摘要
- `--override`：完全覆盖现有 index.md，创建只包含摘要的最小化模板（⚠️ 慎用）
- `--max-publications`：限制处理的出版物数量

### 注意事项

1. **API 费用**：使用 OpenAI API 会产生费用，建议先用 `--dry-run` 或 `--max-publications 1` 测试
2. **PDF 质量**：如果 PDF 是扫描版或格式复杂，提取效果可能不理想
3. **摘要位置**：脚本假设摘要在前 1-2 页，如果位置特殊可能需要调整
4. **已有数据**：默认不覆盖已有的 abstract 和 summary，使用 `--force` 强制更新
5. **备份**：修改前建议先提交当前更改或创建备份

### 推荐模型

- **gpt-4o-mini**（默认）：性价比高，适合批量处理，每次调用约 $0.0001-0.0003
- **gpt-4o**：质量最好，适合重要论文，每次调用约 $0.001-0.003
- **gpt-3.5-turbo**：最便宜，质量稍逊，每次调用约 $0.00005

### 工作流程示例

```bash
# 1. 先测试单个出版物
python scripts/extract_abstract_from_pdf.py --key wang2025g --dry-run

# 2. 如果效果满意，实际处理
python scripts/extract_abstract_from_pdf.py --key wang2025g

# 3. 检查生成的内容
git diff content/en/publication/wang2025g/index.md

# 4. 如果满意，批量处理其他出版物（建议分批）
python scripts/extract_abstract_from_pdf.py --max-publications 5

# 5. 检查所有更改
git diff content/en/publication/

# 6. 提交更改
git add content/en/publication/
git commit -m "Auto-extract abstracts from PDFs"
```

---

## 增强版检查脚本

### 使用方法

`check_missing_publications_enhanced.py` 提供了更智能的出版物检查功能：

```bash
# 基本用法
python scripts/check_missing_publications_enhanced.py content/My-Publications.bib

# 同时检查哪些出版物没有 PDF 文件
python scripts/check_missing_publications_enhanced.py content/My-Publications.bib --check-pdf

# 检查中文出版物
python scripts/check_missing_publications_enhanced.py content/My-Publications.bib --lang zh --check-pdf

# 预览将要重命名的文件（推荐先运行此命令）
python scripts/check_missing_publications_enhanced.py content/My-Publications.bib --renaming --dry-run

# 实际重命名文件（将 cite.bib 的 key 和 PDF 文件名统一为 citation key）
python scripts/check_missing_publications_enhanced.py content/My-Publications.bib --renaming
```

### 主要功能

1. **智能标题匹配**：不仅检查 citation key，还通过标题相似度匹配，识别可能是同一篇论文的不同版本
2. **PDF 检查**：使用 `--check-pdf` 参数可以列出所有没有 PDF 文件的出版物
3. **自动重命名**：使用 `--renaming` 参数可以将 cite.bib 中的 key 和 PDF 文件名统一为 citation key（文件夹名）
4. **详细报告**：
   - 精确匹配的出版物
   - 标题相似的出版物（可能是 citation key 变化）
   - 真正缺失的出版物
   - 缺少 PDF 的出版物（使用 --check-pdf）

### 输出示例

#### PDF 检查示例

```
📄 PDF CHECK
================================================================================

⚠️  PUBLICATIONS WITHOUT PDF (3):

   1. [song2024a]
      Year:  2024
      Title: Machine learning in water resources management

   2. [wang2023b]
      Year:  2023
      Title: Urban water systems adaptation

   3. [li2024]
      Year:  2024
      Title: Climate change impacts on agriculture

   Publications with PDF:    16
   Publications without PDF: 3

💡 To extract abstracts from PDFs:
   python scripts/extract_abstract_from_pdf.py
```

#### 文件重命名示例

```
📝 FILE RENAMING
================================================================================

⚠️  DRY RUN MODE - No files will be changed

📁 [song2023a]
   📄 cite.bib: Would rename: song2024d -> song2023a

📁 [wang2025g]
   📄 PDF: Would rename: Wang et al. - 2025 - Anthropogenic impacts.pdf -> wang2025g.pdf

📁 [wu2022b]
   📄 cite.bib: Would rename: xutong_wu_decoupling_2022 -> wu2022b

📊 Renaming Summary:
   Would rename items (dry run)

💡 Remove --dry-run to actually rename files
```

### 重命名功能说明

`--renaming` 参数会自动标准化文件名：

1. **cite.bib 中的 citation key**：修改为文件夹名（citation key）
   - 例如：`@article{old_key,` → `@article{folder_name,`

2. **PDF 文件名**：重命名为 `{citation_key}.pdf`
   - 例如：`Wang et al. - 2025 - Long Title.pdf` → `wang2025g.pdf`

**优点**：
- ✅ 统一命名规范
- ✅ 更易于管理和引用
- ✅ 避免文件名过长
- ✅ 与 citation key 保持一致

**使用建议**：
1. **先使用 `--dry-run` 预览**：确保重命名符合预期
2. **备份重要数据**：虽然脚本很安全，但建议先提交 git 更改
3. **检查结果**：重命名后使用 `git diff` 查看更改

**详细指南**：查看 [`RENAMING_GUIDE.md`](RENAMING_GUIDE.md) 获取完整的使用步骤和案例

---

## 常见问题

**Q: 脚本显示某篇文章缺失，但我确定已经创建了？**

A: 检查文件夹名称是否与 BibTeX 中的 citation key 完全一致（包括大小写）。

**Q: 如何批量创建缺失的页面？**

A: 使用 `academic import --bibtex` 命令，或编写脚本批量生成 `index.md` 模板。

**Q: 我有多个 BibTeX 文件怎么办？**

A: 先合并成一个总文件，或多次运行脚本检查不同的文件。

**Q: PDF 提取的摘要不准确怎么办？**

A: 可以尝试：
1. 使用更好的模型（如 `--model gpt-4o`）
2. 手动检查并编辑生成的 `index.md`
3. 如果 PDF 质量太差，建议手动输入

**Q: 提取摘要时出现 API 错误？**

A: 检查：
1. API Key 是否正确设置
2. OpenAI 账户是否有余额
3. 网络连接是否正常
4. 是否触发了速率限制（可以减少 `--max-publications`）


