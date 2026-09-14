# GitHub Actions Workflows

本目录包含项目的 GitHub Actions 工作流配置。

## 📋 工作流概览

| Workflow | 触发条件 | 状态 | 用途 |
|----------|---------|------|------|
| [docs.yml](docs.yml) | Push to `main` (docs/\*\*) | ✅ 启用 | 部署文档到 GitHub Pages |
| [preview.yml](preview.yml) | Pull Request | ✅ 启用 | PR 预览构建 |
| [hugo.yml](hugo.yml) | Manual only | ⏸️ 禁用 | Hugo 站点部署（已迁移到 Vercel）|

## 🔄 工作流详情

### 1. Deploy Documentation to GitHub Pages (`docs.yml`)

**用途**: 自动部署项目文档到 GitHub Pages

**触发条件**:
- Push 到 `main` 分支
- 修改了 `docs/**` 或 `scripts/README.md`
- 手动触发

**部署目标**: https://songshgeo.github.io/SongshGeo-as-Scholar/

**工作流程**:
1. 检出代码
2. 复制 `docs/` 内容到 `_site/`
3. 复制 `scripts/README.md` 到 `_site/scripts/`
4. 上传构建产物
5. 部署到 GitHub Pages

**注意事项**:
- ✅ 只在 `main` 分支部署（避免环境保护规则冲突）
- ✅ 使用 Docsify 渲染文档
- ✅ 支持全文搜索
- ⚠️ 首次使用需要在 GitHub 仓库设置中启用 Pages（Settings → Pages → Source: GitHub Actions）

**查看部署状态**: [Actions 标签页](https://github.com/SongshGeo/SongshGeo-as-Scholar/actions/workflows/docs.yml)

---

### 2. Preview PR (`preview.yml`)

**用途**: 为 Pull Request 构建预览版本，验证构建成功

**触发条件**:
- 创建或更新 PR（目标分支为 `main` 或 `dev`）

**工作流程**:
1. 安装 Hugo 和依赖
2. 构建网站（包含草稿和未来发布的内容）
3. 在 PR 中发布构建状态评论

**权限**:
- `contents: read` - 读取仓库代码
- `pull-requests: write` - 在 PR 中创建评论

**注意事项**:
- ✅ 只构建不部署（快速验证）
- ✅ 使用开发环境配置
- ✅ 包含草稿内容预览
- ⚠️ 需要 `pull-requests: write` 权限

**查看运行历史**: [Actions 标签页](https://github.com/SongshGeo/SongshGeo-as-Scholar/actions/workflows/preview.yml)

---

### 3. Deploy Hugo site to Pages (`hugo.yml`) - 已禁用

**状态**: ⏸️ **已禁用** - 主站通过 Vercel 部署

**原因**:
- 主站已迁移到 Vercel 进行自动部署
- 避免与文档部署冲突（都使用 GitHub Pages）
- Vercel 提供更好的预览和回滚功能

**如何重新启用**:
1. 如果需要回到 GitHub Pages 部署主站
2. 编辑 `hugo.yml`，取消注释 `push` 触发器
3. 禁用或修改 `docs.yml`（避免冲突）
4. 在 GitHub 设置中配置 Pages 环境

**原始功能**:
- 构建 Hugo 网站
- 部署到 GitHub Pages
- 支持 `main` 分支部署

---

## ⚙️ 配置说明

### 环境保护规则

GitHub Pages 环境默认只允许 `main` 分支部署。如果需要从其他分支部署：

1. 进入仓库 Settings → Environments → github-pages
2. 修改 Deployment branches 规则
3. 添加允许的分支（如 `dev`）

**当前配置**: 只允许 `main` 分支部署（推荐）

### Concurrency 控制

文档部署 workflow 使用 `group: "pages"` 来确保：
- 同一时间只有一个部署任务运行
- 避免多个部署任务冲突
- 旧的排队任务会被取消

### 权限说明

| 权限 | 用途 | 使用的 workflow |
|------|------|----------------|
| `contents: read` | 读取仓库代码 | 所有 |
| `pages: write` | 部署到 GitHub Pages | docs.yml |
| `id-token: write` | GitHub Pages 认证 | docs.yml |
| `pull-requests: write` | 在 PR 中评论 | preview.yml |

## 🐛 常见问题

### Q: "Branch 'dev' is not allowed to deploy to github-pages"

**A**: 这是正常的环境保护规则。现在 `docs.yml` 已修改为只在 `main` 分支部署，不会再出现此错误。

**解决方案**:
- ✅ 已修改 `docs.yml` 只监听 `main` 分支
- ✅ 已禁用 `hugo.yml` 自动触发

### Q: "Restore cache failed: Dependencies file is not found (go.sum)"

**A**: Go 依赖缓存失败，但不影响构建。

**解决方案**:
- ✅ 已添加 `cache: false` 禁用 Go 缓存
- 或者在项目根目录运行 `go mod tidy` 生成 `go.sum`

### Q: "Resource not accessible by integration" (preview.yml)

**A**: PR 评论需要 `pull-requests: write` 权限。

**解决方案**:
- ✅ 已添加 `pull-requests: write` 权限到 `preview.yml`

### Q: 两个 workflow 同时部署到 GitHub Pages 冲突

**A**: 多个 workflow 使用相同的 concurrency group 会冲突。

**解决方案**:
- ✅ 已禁用 `hugo.yml` 自动部署（主站用 Vercel）
- ✅ `docs.yml` 只在 `main` 分支部署文档
- 明确职责分工：Vercel 部署主站，GitHub Pages 部署文档

## 📊 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                     代码推送                                  │
└────────────┬───────────────────────────┬────────────────────┘
             │                           │
             ▼                           ▼
      ┌─────────────┐            ┌─────────────┐
      │   Push to   │            │  Pull        │
      │  main/dev   │            │  Request     │
      └──────┬──────┘            └──────┬───────┘
             │                          │
    ┌────────┴────────┐                 ▼
    │                 │          ┌─────────────┐
    ▼                 ▼          │ preview.yml │
┌─────────┐    ┌──────────┐     │  (构建+评论) │
│ Vercel  │    │ docs.yml │     └─────────────┘
│ (主站)  │    │ (main)   │
└─────────┘    └────┬─────┘
    │               │
    │               ▼
    │        GitHub Pages
    │      (文档站点)
    │
    ▼
Production
(yoursite.com)
```

## 🔄 工作流程推荐

### 开发新功能

```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发并提交
git add .
git commit -m "feat: add new feature"

# 3. 推送并创建 PR
git push origin feature/new-feature

# 4. PR 自动触发 preview.yml 构建验证
#    查看 PR 评论中的构建状态

# 5. 合并到 dev 分支测试
git checkout dev
git merge feature/new-feature

# 6. Vercel 自动部署预览环境
```

### 发布到生产

```bash
# 1. 从 dev 创建 PR 到 main
git checkout dev
gh pr create --base main --title "Release v1.0.0"

# 2. 审查并合并 PR

# 3. 自动触发：
#    - docs.yml → 文档部署到 GitHub Pages
#    - Vercel → 主站部署到生产环境
```

### 更新文档

```bash
# 1. 编辑文档
vim docs/SOME_DOC.md

# 2. 提交到 main 分支
git add docs/
git commit -m "docs: update documentation"
git push origin main

# 3. docs.yml 自动部署文档
#    访问 https://songshgeo.github.io/SongshGeo-as-Scholar/
```

## 📚 相关文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [GitHub Pages 配置](https://docs.github.com/en/pages)
- [Vercel 部署指南](https://vercel.com/docs)
- [项目文档发布指南](../../docs/DOCS_DEPLOYMENT.md)

## 💡 最佳实践

1. **职责分离**:
   - Vercel 负责主站部署（支持预览、回滚）
   - GitHub Pages 负责文档站点

2. **环境管理**:
   - `main` 分支 → 生产环境
   - `dev` 分支 → 开发/测试环境
   - PR → 预览构建

3. **减少冲突**:
   - 避免多个 workflow 部署到同一目标
   - 使用 concurrency 控制并发部署
   - 明确分支部署规则

4. **安全性**:
   - 最小权限原则（只授予必需的权限）
   - 使用环境保护规则
   - 定期审查 workflow 配置

---

**最后更新**: 2025-10-19
