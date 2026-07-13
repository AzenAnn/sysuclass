# 如何贡献与更新

不会 Git 也可以参与。小修正可直接编辑网页，大文件可在课程目录中上传；如果仍不确定，开一个“资料投稿”Issue 交给维护者整理。

## 上传前的 30 秒检查

- [ ] 这是我原创的，或我能指出允许再分发的明确授权；
- [ ] 文件中没有姓名、学号、邮箱、手机号、成绩、手写签名等个人信息；
- [ ] 不是盗版教材、付费内容、未授权课件或正在进行的考核内容；
- [ ] 文件名能看出年份、学期、类型与主题；
- [ ] 我会同步更新该课程的资料清单，而不是只扔一个文件。

不确定能否上传时，先阅读[版权与隐私规范](policies/copyright.md)，只提交描述和公开链接，不要先上传文件。

## 方法一：只用 GitHub 网页（推荐新手）

以“数学分析”资料为例：

1. 登录 GitHub，打开本项目，点击右上角 **Fork**；
2. 进入 `docs/courses/math-analysis/resources/`，选择一个分类目录：
   - `notes/`：原创课堂或自学笔记；
   - `review/`：复习提纲、知识框架；
   - `exams/`：获准公开的往年试卷或题型整理；
   - `homework/`：本人原创题解、勘误或公开授权材料；
   - `other/`：确实无法归入以上类别的资料；
3. 点击 **Add file → Upload files**，上传文件并填写提交说明；
4. 返回 `docs/courses/math-analysis/resources/index.md`，点击铅笔图标，在表格中新增一行；
5. 如资料改变了对课程的理解，再编辑 `docs/courses/math-analysis/index.md` 中对应章节；
6. 点击 **Contribute → Open pull request**，在清单中勾选版权与隐私确认项。

推荐文件名：`年份-学期-类型-简述.ext`，例如：

```text
2025-秋-笔记-极限与连续.pdf
2024-春-复习-多元微积分.md
2023-秋-试卷-期末-已脱敏.pdf
```

同一文件不要使用“最终版”“最新版”这类会过期的名称。扫描件请先旋转、裁边、压缩并确认文字可读；单文件建议不超过 25 MB。

## 方法二：命令行更新

```bash
git clone https://github.com/<你的账号>/<仓库名>.git
cd <仓库名>
git switch -c add/math-analysis-<资料简称>
```

把资料复制到对应分类后，编辑资源清单，再执行：

```bash
python scripts/check_resources.py
python -m mkdocs build --strict
python scripts/check_site_links.py
git add docs/courses/math-analysis
git commit -m "docs(math-analysis): add <资料简称>"
git push -u origin add/math-analysis-<资料简称>
```

然后在 GitHub 发起 Pull Request。一次 PR 尽量只处理一门课程或一组紧密相关的资料，便于审核和撤回。

## 怎样登记一份资料

在课程的 `resources/index.md` 表格中新增一行：

```markdown
| [文件名](notes/文件名.pdf) | 笔记 | 2025 秋 | 张三（已同意署名） | 作者原创，CC BY-NC-SA 4.0 | 第一至三章 |
```

如果作者希望匿名，可写“匿名贡献者”；但维护者仍需能从 PR/Issue 记录确认授权。若材料来自公开网页，请链接原页面并写明页面展示的开放许可；“网上找到的”不是有效来源。

## 更新课程攻略

课程攻略优先记录跨学期仍有价值的信息：

- 课程内容的知识结构与先修要求；
- 不同章节的常见困难和学习方法；
- 教材/参考书的使用方式，而不是上传书本身；
- 考核构成的历史记录，必须标明学期和适用范围；
- 已失效信息的更正记录。

评价教师时，应聚焦可核验的教学安排和个人学习体验，注明学期，不做人身评价。涉及负面或主观评价时使用教师姓名拼音首字母，并避免让描述可用于骚扰个人。

## 新建一门课程

1. 复制 `templates/course/` 为 `docs/courses/<英文短名>/`；
2. 把模板中的占位文字替换为课程真实信息；
3. 在 `docs/catalog.md` 增加课程；
4. 在 `mkdocs.yml` 的 `nav → 课程目录` 下增加课程名称、课程页与资料清单；
5. 执行本地检查后提交 PR。

英文短名只用于稳定网址，页面标题和文件名可以使用中文。课程名称、代码或院系不确定时请保留“待核验”，不要猜测。

!!! warning "课程不要占用顶部标签"
    所有课程必须作为 `课程目录` 的子项。不要把课程名称添加为 `nav` 的顶层项目，否则课程增多后顶部标签会溢出。

## 管理员首次发布

1. 在 GitHub 创建空仓库，并把本目录推送到 `main` 分支；
2. 修改 `mkdocs.yml`，补上真实的 `site_url` 与 `repo_url`；
3. 打开仓库 **Settings → Pages**，在 **Build and deployment** 中选择 **GitHub Actions**；
4. 推送后查看 **Actions → Deploy course guide**；部署完成后把网站地址加到仓库 About；
5. 在 **Settings → General → Pull Requests** 中启用合并前审核，并为 `main` 配置分支保护（推荐但非必需）。

工作流会在每个 PR 上执行资源登记、严格构建和站内链接检查；只有推送到 `main` 时才发布网站。
