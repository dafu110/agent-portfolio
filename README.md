# AI Agent Portfolio

这是一个静态作品集网页，用于展示傅孟涵面向 AI Agent 产品、AI 应用工程与 AI 解决方案岗位的产品判断、工程实现和可验证交付能力。

## 教育

人工智能与大数据工学硕士  
拟于 2027 年 9 月毕业

内蒙古科技大学 | 建筑学本科 | 2010 - 2015

## 本地查看

安装生成脚本所需依赖：

```powershell
python -m pip install -r requirements.txt
```

然后直接打开 `index.html`，或在项目目录启动本地服务：

```powershell
python -m http.server 8765
```

然后访问：

```text
http://127.0.0.1:8765/
```

生成两份定向 PDF 简历：

```powershell
python make_chinese_resume_pdf.py --variant product
python make_chinese_resume_pdf.py --variant engineer
```

- 产品与解决方案版：`assets/resume.pdf`
- Agent 工程版：`assets/resume-agent-engineer.pdf`

## GitHub Pages 发布

目标仓库：`https://github.com/dafu110/agent-portfolio`

项目内置 `.github/workflows/pages.yml`。首次将代码推送到 `main` 后，在仓库 `Settings → Pages` 中将发布源设置为 **GitHub Actions**；工作流会只打包网页运行所需的 HTML、CSS、JavaScript、案例、证据与资源文件，并发布到：

```text
https://dafu110.github.io/agent-portfolio/
```

可在仓库的 `Actions` 页面查看部署状态，成功后 `Deploy portfolio to GitHub Pages` 会显示绿色通过标记。

## 页面结构

- 首屏：统一呈现 Agent 产品与应用工程定位、三项核心证据和双版本 PDF 入口
- 旗舰案例：使用全幅产品界面和简短案例说明建立第一视觉焦点
- 项目：首页以角色、关键决策与结果摘要展示 4 个专项案例，服务招聘方快速扫描
- 证据页：`cases/index.html`，集中展示技术边界、完整验证口径、失败案例、GitHub 与复现入口
- PeopleOps 演示：在首页项目履历与证据页内嵌 90 秒 WebM 产品视频，展示制度问答、引用、受控动作、审批与记录
- 项目证据：四个项目均公开当前仓库实现周期与个人关键决策；PeopleOps 另提供带日期、配置模型、样本量、失败案例和复现命令的机器可读评测记录
- 方法：按问题定义、系统设计、风险控制、验证交付四个阶段呈现
- 背景：建筑设计经验迁移价值与教育信息介绍
- 联系：公开邮箱、GitHub、产品版与 Agent 工程版简历入口

## 视觉策略

- 编辑式案例作品集，而不是招聘信息面板或 SaaS 卡片墙
- Codex 式浅色工作区：暖灰画布、黑色证据带、开放式项目档案与低对比细线；通过大尺度留白、强标题和连续索引建立层级
- 首屏不堆放指标，产品界面本身承担主视觉
- 只在头像、产品界面和评测记录等真实内容容器上使用圆角；项目与能力采用开放式分区，避免卡片墙
- 头像作为身份签名，传统项目经历仅作为复杂协同与结果交付的迁移证据

## 设计系统

- 颜色：暖灰画布、白色内容面、近黑正文、两级中性边框；不使用装饰性品牌色和渐变
- 字体：系统无衬线负责正文与标题，系统等宽字体负责索引、状态和证据标签
- 间距：以 4px 为基础单位，常用间距通过 CSS token 统一管理
- 组件：主按钮使用近黑实底，次按钮使用白底细边；真实内容容器使用 7–14px 分级圆角
- 交互：统一焦点环、悬停反馈、移动导航关闭逻辑与 reduced-motion 支持

## 最终展示截图

- 首屏：`output/playwright/portfolio-final-first-impression.png`
- 项目履历：`output/playwright/portfolio-final-projects-hero.png`
- PeopleOps 证据：`output/playwright/portfolio-final-peopleops-evidence.png`
- 移动端首屏：`output/playwright/portfolio-final-mobile-first-impression.png`
- 分享预览：`assets/portfolio-social-preview.png`（1200 × 630）

## 内容口径

- 页面中的测试、轨迹与评测指标用于证明当前实现可复核，不等同于真实线上业务成效
- 满分指标必须与样例集范围一起阅读，详细口径以对应 GitHub 仓库为准
- ResearchOps 分别列示 `pytest` 与 32 条离线评测案例，不将两类验证汇总为单一测试数
- KnowFlow 以 README 规定的门槛表述：主评测集与 holdout 集的 Recall@k、引用准确性等指标均要求 `>= 0.95`
- PeopleOps、ResearchOps、KnowFlow 与 Data Analyst 均为个人项目原型，基于本地样例或离线评测，不宣称生产成效
- PeopleOps 的 2026-07-13 记录包含 47 项单元测试与 25 条离线案例；fixture 模式不调用生成模型，配置模型只作为运行环境上下文
- 当前项目均按独立项目呈现；周期取自对应本地 Git 仓库，关键决策取自项目 ADR、README 或实现边界
- 公开页面只展示邮箱与 GitHub，手机号保留在定向投递材料中

## 后续增强

- 为旗舰项目增加在线只读 Demo 或 60–120 秒演示视频
- 用经批准的代表性数据补充真实生成模型质量、线上用户效果与外部连接器评测
- 发布地址默认为 `https://dafu110.github.io/agent-portfolio/`；若改用其他域名，需同步替换两张页面、`robots.txt` 与 `sitemap.xml` 中的 canonical URL
- 将正式作品集链接放在 PDF 简历顶部

## 发布前检查

- 公开部署时发布 `index.html`、`cases/`、`evidence/`、`site.js`、`base.css`、`components.css`、`home.css`、`responsive.css`、`robots.txt`、`sitemap.xml` 与必要的 `assets/`（包括 PeopleOps WebM、MP4 与字幕轨）
- `.gitignore` 已排除 `output/`、`tmp/`、Python 缓存与本地环境文件
- 证据页中的测试、评测、评审材料链接应在 GitHub 仓库公开后逐一点击确认
- 桌面端、移动端、平板与笔记本截图已经通过 Playwright 生成；发布前仍应确认线上字体与资源加载一致

## 验证

```powershell
python -m unittest discover -s tests -v
python -m py_compile extract_pdf_text.py generate_cover_assets.py make_chinese_resume_pdf.py
node --check site.js
```

站点审计覆盖本地链接、锚点、公开隐私信息、图片固有尺寸、加载策略、移动导航、分享元数据与新窗口链接安全属性。

## 内容更新原则

- 项目时间、模型版本、评测运行日期、实测分数和失败样例只能在对应仓库存在可复核记录后加入，不使用占位数据或推测数据。
- `>= 0.95` 是 KnowFlow 的质量门禁，不是公开页面宣称的实测成绩。
- Data Analyst 的隔离执行与导出能力按“可复核范围”描述，不等同于真实业务质量结果。
