# 部署指南 / Deployment Guide

本项目支持通过 GitHub Actions 自动部署到 GitHub Pages。

## 🚀 自动部署流程

### 1. 推送到 GitHub

每次推送到 `main` 或 `dev` 分支时，GitHub Actions 会自动：

1. ✅ 检出代码
2. ✅ 安装 Hugo 和依赖
3. ✅ 构建网站
4. ✅ 部署到 GitHub Pages

### 2. 使用 Makefile 快速部署

```bash
# 方式 1: 一键部署
make deploy

# 方式 2: 分步部署
make commit  # 提交更改
make push    # 推送到 GitHub（自动触发部署）
```

### 3. 查看部署状态

部署状态可在 GitHub Actions 页面查看：
https://github.com/SongshGeo/SongshGeo-as-Scholar/actions

## 📋 首次设置 GitHub Pages

如果是第一次部署，需要在 GitHub 仓库设置中启用 GitHub Pages：

1. 进入仓库设置：`Settings` → `Pages`
2. 在 **Source** 下选择 `GitHub Actions`
3. 保存设置

## 🔍 预览 Pull Request

当你创建 Pull Request 时：
- GitHub Actions 会自动构建并测试
- 构建成功后会在 PR 中评论通知
- 可以在合并前确保没有构建错误

## ⚙️ 工作流文件

- `.github/workflows/hugo.yml` - 主部署工作流（main/dev 分支）
- `.github/workflows/preview.yml` - PR 预览工作流

## 🛠️ 本地测试部署

在推送前，建议先本地测试构建：

```bash
# 清理旧文件
make clean

# 本地构建
make build

# 测试开发服务器
make server
```

## 📝 部署检查清单

推送前确保：

- [ ] 本地 `make build` 无错误
- [ ] 本地 `make server` 预览正常
- [ ] 所有更改已提交
- [ ] 提交信息清晰明确

## 🔄 更新出版物后的完整流程

```bash
# 1. 检查缺失的出版物
make check

# 2. 创建缺失的出版物页面
make create

# 3. 本地预览
make server

# 4. 确认无误后部署
make deploy
```

## 🌐 访问你的网站

部署成功后，你的网站将在以下地址可访问：
- GitHub Pages URL（在仓库 Settings → Pages 中查看）

## 💡 提示

- 部署通常需要 1-3 分钟
- 首次部署可能需要稍长时间
- 如果部署失败，查看 Actions 页面的日志
- 可以在 Actions 页面手动重新运行失败的工作流

