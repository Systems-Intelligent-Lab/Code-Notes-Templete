# Code-Notes-Templete

一个用于「边写代码边记笔记」的模板仓库，核心特点：

- **笔记用 Markdown 写在 `docs/` 下**
- **Python 示例代码写在 `.py` 文件里（如 `python-demos/`）**
- **在 Markdown 中通过自定义指令引用 `.py` 里的函数/类，构建时自动插入源码**

最终通过 **VitePress** 构建成一个静态网站，可以部署到 GitHub Pages 上浏览。

---

## 项目结构

大致目录结构如下：

- `docs/`：你亲自编写的 Markdown 笔记
  - `index.md`：首页
  - `.vitepress/config.ts`：VitePress 配置（导航、侧边栏、`base` 等）
  - `python-basics/default_args.md`：示例笔记，演示如何引用 Python 函数源码
- `python-demos/`：Python 示例代码
  - `basics/default_args.py`：包含 `append_item` 函数的示例文件
- `scripts/`：构建前的预处理脚本
  - `extract_snippet.py`：从 `.py` 文件中按函数/类名提取源码
  - `expand_py_symbols.py`：扫描 `docs/**/*.md`，将自定义指令替换为真正的代码块，生成到 `docs_generated/`
- `docs_generated/`：由 `expand_py_symbols.py` 自动生成的 Markdown（不会提交到 Git）
- `.github/workflows/deploy-docs.yml`：GitHub Pages 部署 workflow

---

## Markdown 中如何引用 `.py` 文件里的函数/类

在你自己的笔记中，只需要写一段自定义块指令 `py-symbol`，**不需要粘贴任何 Python 源码**：

```markdown
::: py-symbol
path: python-demos/basics/default_args.py
symbol: append_item
type: function   # function 或 class
:::
```

含义说明：

- `path`：相对于仓库根目录的 `.py` 文件路径
- `symbol`：要展示的函数名或类名（必须是顶层定义）
- `type`：`function` 或 `class`

在构建前，会运行脚本：

```bash
npm run docs:prebuild
```

该脚本会：

1. 遍历 `docs/**/*.md`
2. 找到所有 `::: py-symbol ... :::` 区块
3. 用 `scripts/extract_snippet.py` 从对应 `.py` 文件中提取目标函数/类源码
4. 在生成目录 `docs_generated/` 中，把这些指令替换成真正的 ```python 代码块

VitePress 最终使用 `docs_generated/` 作为内容源进行构建。

---

## 本地开发与预览

前置条件：已安装 Node.js（推荐 18+，本仓库使用 20 测试）和 Python 3.8+。

```bash
# 安装依赖
npm install

# 预处理 Markdown：从 .py 中提取代码到 docs_generated/
npm run docs:prebuild

# 本地开发预览（默认 http://localhost:5173）
npm run docs:dev

# 或直接构建静态站点（输出到 docs_generated/.vitepress/dist）
npm run docs:build
```

日常编辑建议流程：

1. 在 `python-demos/` 中新增或修改 Python 示例代码
2. 在 `docs/` 中新增/修改 Markdown 笔记，并用 `py-symbol` 指令引用函数/类
3. 运行 `npm run docs:prebuild && npm run docs:dev` 本地预览效果

---

## 部署到 GitHub Pages

仓库示例地址：`https://github.com/Systems-Intelligent-Lab/Code-Notes-Templete`

GitHub Pages 访问地址形如：

```text
https://systems-intelligent-lab.github.io/Code-Notes-Templete/
```

关键点：

- 在 `docs/.vitepress/config.ts` 中已经设置：

```ts
base: '/Code-Notes-Templete/'
```

- `.github/workflows/deploy-docs.yml` 会在推送到 `main` 分支时：
  1. 安装依赖
  2. 运行 `npm run docs:prebuild`
  3. 运行 `npm run docs:build`
  4. 将 `docs_generated/.vitepress/dist` 部署到 GitHub Pages

你需要在 GitHub 仓库中：

1. 打开 `Settings → Pages`
2. 将 **Source** 设置为 **GitHub Actions**
3. 推送代码到 `main`，等待 Actions 完成构建与部署

部署成功后，`Settings → Pages` 页面会显示站点访问链接。
