# 中山大学课程攻略共享计划

这是一个由同学共同维护、面向中山大学课程的非官方资料与经验库。我们希望把散落在群聊和个人设备里的笔记、复习经验与获授权资料，整理成公开、可检索、可持续维护的课程档案。

网站：<https://azenann.github.io/sysuclass/>

项目参考了[浙江大学课程攻略共享计划](https://qsctech.github.io/zju-icicles/)的开放协作思路，但目录、资料登记和版权审查规则从零建立。本项目与中山大学官方无隶属关系；所有信息均需读者自行核验。

## 已初始化

- 可搜索的 MkDocs Material 网站；
- GitHub Pages 自动构建与部署；
- 课程目录、课程页和资源登记表；
- 网页端与命令行两套贡献教程；
- Issue、Pull Request 模板及版权/隐私检查；
- “数学分析”示范课程和资料分类目录。

## 本地预览

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m mkdocs serve
```

浏览器打开 <http://127.0.0.1:8000>。提交前运行：

```powershell
python scripts/check_resources.py
python -m mkdocs build --strict
python scripts/check_site_links.py
```

完整投稿步骤见[如何贡献](docs/contributing.md)，第一门示范课程见[数学分析](docs/courses/math-analysis/index.md)。

## 许可

贡献者原创的文字、笔记和整理内容默认采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)；第三方材料仍归原权利人所有，并且只有在许可明确时才可收录。详见[版权与隐私规范](docs/policies/copyright.md)。
