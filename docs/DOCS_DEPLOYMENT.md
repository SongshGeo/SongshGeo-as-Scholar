# 文档发布指南

本项目使用 [Docsify](https://docsify.js.org/) 将 `docs/` 目录中的 Markdown 文档发布为一个美观的在线文档站点。

## 📖 在线访问

文档自动发布到 GitHub Pages：

**文档地址**: https://songshgeo.github.io/SongshGeo-as-Scholar/

> 注意：首次推送后，需要在 GitHub 仓库设置中启用 GitHub Pages（见下方设置说明）。

## 🚀 快速开始

### 本地预览文档

```bash
# 启动文档服务器
make docs-serve

# 或者直接使用 docsify
cd docs
docsify serve .
```

然后在浏览器中访问 http://localhost:3000

### 构建文档（用于测试）

```bash
# 构建文档到 _site/ 目录
make docs-build

# 在浏览器中预览
open _site/index.html
```

## 🔧 文档结构

```
docs/
├── index.html              # Docsify 主页面（自动加载）
├── _sidebar.md            # 侧边栏导航
├── _navbar.md             # 顶部导航栏
├── .nojekyll              # 告诉 GitHub Pages 不使用 Jekyll
├── README.md              # 文档首页
├── MAINTENANCE_GUIDE.md   # 维护指南
├── QUICKSTART.md          # 快速开始
├── WORKFLOW.md            # 工作流程
└── ...                    # 其他文档
```

### 关键文件说明

#### `index.html`
- Docsify 的主配置文件
- 定义了主题、插件、搜索功能等
- 无需修改（除非要自定义样式或功能）

#### `_sidebar.md`
- 左侧边栏导航
- 按类别组织文档链接
- 添加新文档时需要更新此文件

#### `_navbar.md`
- 顶部导航栏
- 提供快速访问链接
- 可以添加外部链接

## 📝 添加新文档

### 1. 创建 Markdown 文件

在 `docs/` 目录中创建新的 `.md` 文件：

```bash
echo "# 新文档标题" > docs/NEW_DOCUMENT.md
```

### 2. 更新侧边栏

编辑 `docs/_sidebar.md`，添加链接：

```markdown
* **你的分类**
  * [新文档](NEW_DOCUMENT.md)
```

### 3. 本地预览

```bash
make docs-serve
```

### 4. 提交并推送

```bash
git add docs/
git commit -m "docs: add new document"
git push
```

文档会自动发布到 GitHub Pages（约 1-2 分钟后生效）。

## 🎨 自定义样式

### 修改主题

编辑 `docs/index.html` 中的主题链接：

```html
<!-- 可选主题 -->
<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/buble.css">
<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/dark.css">
<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/pure.css">
```

### 自定义颜色

在 `index.html` 的 `<style>` 标签中修改：

```css
:root {
  --theme-color: #0066cc;  /* 主题颜色 */
  --theme-color-dark: #004d99;
}
```

### 添加自定义 CSS

```html
<style>
  /* 你的自定义样式 */
  .markdown-section h1 {
    color: #333;
  }
</style>
```

## 🔌 添加插件

Docsify 有丰富的插件生态。在 `index.html` 中添加：

### 示例：添加代码复制按钮

```html
<!-- 在 </body> 前添加 -->
<script src="//cdn.jsdelivr.net/npm/docsify-copy-code@2"></script>
```

### 示例：添加页脚

```html
<script>
  window.$docsify = {
    // ... 其他配置

    plugins: [
      function(hook) {
        var footer = [
          '<hr/>',
          '<footer>',
          '<span>&copy; 2025 SongshGeo. </span>',
          '<span>Built with <a href="https://docsify.js.org">Docsify</a>.</span>',
          '</footer>'
        ].join('');

        hook.afterEach(function(html) {
          return html + footer;
        });
      }
    ]
  }
</script>
```

更多插件见：https://docsify.js.org/#/plugins

## ⚙️ GitHub Pages 设置

### 首次设置

1. **推送文档到 GitHub**:
   ```bash
   git push origin main  # 或 dev 分支
   ```

2. **在 GitHub 仓库设置**:
   - 进入仓库页面
   - Settings → Pages
   - Source 选择 "GitHub Actions"
   - 保存设置

3. **查看部署状态**:
   - 进入 Actions 标签页
   - 查看 "Deploy Documentation to GitHub Pages" workflow
   - 等待部署完成（约 1-2 分钟）

4. **访问文档**:
   - https://songshgeo.github.io/SongshGeo-as-Scholar/

### 触发部署

文档会在以下情况自动部署：

1. **自动触发**（推荐）:
   - Push 到 `main` 或 `dev` 分支
   - 修改了 `docs/**` 或 `scripts/README.md` 文件

2. **手动触发**:
   - GitHub 仓库 → Actions 标签
   - 选择 "Deploy Documentation to GitHub Pages"
   - 点击 "Run workflow"
   - 选择分支并运行

### 部署原理

项目使用 GitHub Actions workflow (`.github/workflows/docs.yml`) 自动部署：

1. **监听文件变化**:
   - `docs/**`
   - `scripts/README.md`
   - `.github/workflows/docs.yml`

2. **触发条件**:
   - ✅ 只在 `main` 分支部署（避免环境保护规则冲突）
   - ✅ 监听文档相关文件变化
   - ✅ 支持手动触发

3. **构建步骤**:
   - 复制 `docs/` 内容到 `_site/`
   - 复制 `scripts/README.md` 到 `_site/scripts/`
   - 创建重定向页面

4. **部署到 GitHub Pages**:
   - 使用 GitHub Pages 官方 Actions
   - 自动部署到 `gh-pages` 分支（无需手动管理）

5. **与主站分离**:
   - 主站通过 Vercel 部署
   - 文档站通过 GitHub Pages 部署
   - 避免部署冲突

更多详情请查看 [.github/workflows/README.md](../.github/workflows/README.md)

## 🔍 搜索功能

文档内置了全文搜索功能（由 Docsify 提供）：

- 点击右上角搜索框
- 输入关键词
- 实时显示匹配结果
- 支持中文搜索

搜索配置在 `index.html` 中：

```javascript
search: {
  maxAge: 86400000,        // 缓存时间（1天）
  paths: 'auto',           // 自动搜索所有路径
  placeholder: '搜索文档',
  noData: '没有找到结果',
  depth: 6,                // 搜索深度（标题级别）
}
```

## 📊 文档统计

文档包含字数统计插件，会自动显示：
- 每篇文档的字数
- 预计阅读时间

## 🐛 常见问题

### Q: 本地预览时提示 "docsify command not found"？

A: 安装 docsify-cli：

```bash
npm install -g docsify-cli
```

### Q: GitHub Pages 显示 404？

A: 检查：
1. GitHub Pages 是否已启用（Settings → Pages）
2. Source 是否选择了 "GitHub Actions"
3. Actions workflow 是否成功运行（Actions 标签页）
4. 是否等待了足够的部署时间（1-2 分钟）

### Q: 文档更新后没有立即生效？

A: 可能原因：
1. **浏览器缓存**: 强制刷新（Ctrl+F5 / Cmd+Shift+R）
2. **GitHub Pages 缓存**: 等待 1-2 分钟
3. **CDN 缓存**: 部分 CDN 资源可能有缓存延迟

### Q: 如何查看部署日志？

A:
1. 进入 GitHub 仓库的 Actions 标签
2. 找到最近的 "Deploy Documentation" workflow
3. 点击查看详细日志

### Q: 侧边栏不显示？

A: 检查：
1. `_sidebar.md` 文件是否存在
2. `index.html` 中是否设置了 `loadSidebar: true`
3. Markdown 语法是否正确

### Q: 搜索功能不工作？

A: 检查：
1. 浏览器控制台是否有错误
2. 是否加载了搜索插件（`search.min.js`）
3. 清除浏览器缓存后重试

## 📚 参考资料

- [Docsify 官方文档](https://docsify.js.org/)
- [Docsify 主题](https://docsify.js.org/#/themes)
- [Docsify 插件列表](https://docsify.js.org/#/plugins)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

## 💡 最佳实践

1. **编写清晰的标题**: 使用有意义的标题层级（H1-H6）
2. **添加目录**: 使用 `[toc]` 或让 Docsify 自动生成
3. **代码块语法高亮**: 指定语言 (\`\`\`bash、\`\`\`python 等)
4. **内部链接**: 使用相对路径 `[链接](OTHER_DOC.md)`
5. **图片**: 放在 `docs/images/` 目录，使用相对路径引用
6. **定期更新**: 保持文档与代码同步
7. **测试链接**: 本地预览时检查所有链接是否有效

## 🔄 工作流程

### 日常文档更新

```bash
# 1. 编辑文档
vim docs/SOME_DOC.md

# 2. 本地预览
make docs-serve

# 3. 提交更改
git add docs/
git commit -m "docs: update documentation"

# 4. 推送并自动部署
git push origin main
```

### 重大文档改版

```bash
# 1. 创建新分支
git checkout -b docs-update

# 2. 修改文档
vim docs/*.md

# 3. 本地预览和测试
make docs-serve

# 4. 提交更改
git add docs/
git commit -m "docs: major documentation update"

# 5. 推送到远程
git push origin docs-update

# 6. 创建 Pull Request
# 在 GitHub 上创建 PR，审查后合并到 main

# 7. 合并后自动部署
```

---

**提示**: 如果有任何问题，请查看 [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) 或提交 Issue。
