---
name: oil-ui
description: "UI/UX design skill for Claude Code, Cursor, Codex & AI coding agents: design, refine, and review frontend interfaces for websites, apps, dashboards, and components with visual direction exploration, 3-direction side-by-side HTML comparison on request, DESIGN.md conflict checks, and real-browser screenshot & lightweight UX review. Defers to oil-ui-pro when installed. 设计、改进和评审网站、App、后台与组件的界面：探索设计方向、按需生成多风格同屏对比页、排查设计规范（DESIGN.md）冲突，并基于真实截图打磨视觉层级；按请求交付对比页、设计说明、设计稿或可运行界面。只负责设计判断，不用于纯业务逻辑、接口构建、无界面变化的代码整理，或改法已完全明确的日常修改（如改文案、调数量、删指定元素、复用现有样式，哪怕带有“优化”字样）。已安装 oil-ui-pro 时交给 oil-ui-pro。"
metadata:
  version: "0.34.5"
  fork_release: "craft-ux.5"
  compatibility: "Host-neutral UI/UX design workflow (Claude Code, Cursor, Codex, Windsurf, Cline, Antigravity, OpenCode). Optional style-comparison generator requires Python 3.10+ standard library and a modern browser; optional local screenshot, media, and image helper scripts require Node.js 22+ (with local Chrome/Chromium/Edge for screenshots and optional ffmpeg for video). 核心为宿主中立的文本流程，不依赖其他 Skill 或指定模型；可选风格对比页生成器需 Python 3.10+ 标准库与现代浏览器，本机截图、素材筛选与生图辅助脚本需 Node.js 22+（截图需本机 Chrome/Chromium/Edge，录屏可选配 ffmpeg）。实际视觉验收需要看图能力；交互验收需要可操作环境；独立评审需要隔离上下文且能看图的执行者。"
---

# oil-ui

Interface & UI/UX design workflow for AI coding agents — establishes a clear visual north star, builds 3-direction side-by-side comparisons on request, audits `DESIGN.md` conflicts, and polishes websites, apps, dashboards, and components against real-browser screenshots.

先定下一句设计北极星，再让构图、字体、色彩、素材和交互都朝它靠拢，做出一眼认得出来的界面。克制是留下最有力量的选择、删掉没有贡献的元素，不是把所有风格磨成中庸。界面好不好看、任务走不走得通，分开验收。

读得少，查得严：常见任务只读本文件和 [轻路径](references/light-path.md)，其余参考等下面点名的情况出现了再读；用截图检查和与任务相称的评审核对结果。方法、评审协议和工具都在本目录里，不需要另外加载其他 Skill，相对链接从本文件所在的目录算起；前端怎么实现按项目自己的约定来。

## 开始前

**Fork 更新保护**：此安装版本来自 `Disene/oil-ui-craft`，包含独立维护的 `fork_release`。不运行原版 `scripts/check_update.sh` 或 `scripts/check_update.py --update`，因为它们原先指向官方 Oil CLI，可能覆盖 Fork 的新增能力。用户明确要求更新时，只从 `https://github.com/Disene/oil-ui-craft` 获取经过核对的版本；要吸收上游 Oil UI 的新版本，先在 Fork 仓库进行差异审查、测试与合并，再更新已安装 Skill。平时使用无需版本检查或新依赖。

## 选择范围

- 只读和任务相关的页面与资料，不先通读整个项目。只有缺的信息会改变核心方向、又推断不出来时，才集中问一次；改得回来的细节自己决定，并说明假设。
- 回复、设计说明和交付说明用用户使用的语言；界面文案用产品面向用户的语言，没有说明时跟随用户。本 Skill 用中文写成，用户用英文时不要因此夹带中文。
- 用户定下的品牌、参考、页面结构和交互约束优先。项目里的设计文档（包括 Agent 指令文件里写视觉的段落）彼此冲突或和代码对不上时，不强行同时满足，在方向确认时挑明打算按哪份做；没有确认环节时写进交付说明。分清用户要的是借鉴风格、重新设计还是精准还原，不自己换目标。
- 设计说明、设计稿、原型和可运行的产品是不同的交付物：只要评审时不改文件，只要设计时不改业务代码。
- 新建界面、多方向探索或存量重塑时，先看宿主生图工具。宿主不可用且本任务已授权使用 Oil 服务时，运行 `node <skill>/scripts/oiloil-image.mjs balance`，余额至少 3 积分才考虑使用，并按实际费用核对。可用时若需确认，把生图选择与方向确认合并。已授权直接推进的任务可使用可用的宿主工具，Oil 积分消费须有单独的任务授权。选用生图时读 [生图设计与还原校准](references/image-ideation.md)，否则按代码流程继续。
- 要留多方向候选、过程截图或中间素材时，位置按 [任务工作区](references/workdir.md)；直接实现单页或改现有代码时写目标文件，不预建过程目录。

| 当前范围 | 怎么走 |
| --- | --- |
| 小改动：用户点名了要改的元素和改法，例如改文案、调数量、删指定元素，或“保存按钮换成绿色”“这里间距大一点” | 直接改，一两句话交付；不盘点现状、不定方向、不派评审。只改文案、数量或复用现有样式的，改完就交；改了颜色、间距或样式的，在目标视口看一眼改动处和相邻元素。只说别扭、不好看、想优化而没点名改哪里的，不算小改动 |
| 新界面；用户已选定方向，或继续已确认的方向 | [轻路径](references/light-path.md)，第 1 步“方向”那一行按下一节的页面类型写。方向没经用户确认、又没授权直接做时，在第 1 步发出方案后停下；继续已确认的方向时只检查受影响的区域与状态 |
| 明确要求比较设计方向或版式 | 在原任务上叠加 [显式探索](references/task-explore.md)；数量服从用户，未指定时才默认三个 |
| 单个组件，要打磨到极致或做出辨识度 | 走轻路径，范围只是这个组件，只做一个方向：先定一个视觉主角，从它取色，力气集中在主操作那一刻 |
| 把用户已认可的原型实现为真实项目的代码 | 原型只当视觉标准：不用 iframe 嵌入，不把原型的样式和脚本整段搬进工程；用项目已有的组件、样式变量和组件库实现，不引入同类的第二个库 |
| 存量项目里优化 UI、改流程或加新功能 | 先分清用户要哪一种：优化 UI 可以重新决定偶然形成的视觉默认值，品牌资产保留；改流程和加新功能沿用现有视觉，不走视觉方向探索。盘点现有页面、设计变量和共享组件，留基线截图，从源头修改 |
| 整理或沉淀项目设计规范：几份设计文档打架、文档和代码对不上，或要从现有页面提炼规范 | 列出找到的规范文件和互相冲突的地方交给用户，不擅自合并、改写或删除这些文档 |
| 截图还原 | [布局与视口](references/layout-and-viewport.md) 区分精准还原与生图稿适配，再从轻路径第 2 步进入 |
| UI/UX 评审 | 读 [只读评审](references/task-review.md)，交付证据与建议后停止；不生成新方向，不进入修正循环 |

## 页面类型

按本次页面的实际任务选，“App”“SaaS”这些说法本身不决定类型。它决定轻路径第 1 步“方向”那一行要多交什么：

| 页面实际任务 | 多交什么 |
| --- | --- |
| 说服、品牌表达、发布或展览 | 从 [说服型骨架](references/direction-persuasion.md) 选一个首屏骨架，骨架定了再写文案 |
| 处理对象的工具与后台，浏览与挑选内容的页面 | 首屏优先呈现主要对象和操作，密度与层级沿用项目组件与设计变量。按需参考 [工作区与存量项目](references/craft-workspaces.md) |
| 小游戏、抽奖、计时养成或强手感操控 | 先读 [游玩](references/play.md) 的对象与状态盘点 |

## 什么时候加深

轻路径里方向由主 Agent 自己定，只做一个，不拆标杆、不派概念子 Agent。下面的情况出现时才加深；加深只换第 1 步的做法，实现、截图、评审和交付不变。

| 情况 | 加深成什么 |
| --- | --- |
| 用户要比较方向或版式 | [显式探索](references/task-explore.md)；方向卡和差异检验按 [设计方向](references/design-direction.md) |
| 用户要更有辨识度的方向、对第一版方向不满意，或明确要在定方向上多花成本 | [设计方向](references/design-direction.md) 的“用生成引擎起方向”：全新子 Agent 出概念，主 Agent 选，另一位评审者把关 |
| 用户给了要对标的产品，或要求先看同类怎么做 | [设计方向](references/design-direction.md) 的“认品类，拆标杆”，取到真实画面再拆 |

## 按需再读

页面里出现了左列的东西，或评审指出这一类问题时再读，不预读。

| 出现了什么 | 读 |
| --- | --- |
| 字体、色彩、层级、图标拿不准，或评审指出层级与可读性问题 | [视觉语言](references/visual-language.md) |
| 需要图：选素材、生成配图、让图和页面接成一体、3D 与视频 | [素材](references/media.md) |
| 先生成 UI 设计稿再实现 | [生图设计与还原校准](references/image-ideation.md) |
| 动效手感、界面过渡、时长 | [动效](references/motion.md) |
| 落地页、品牌页、发布页、展览页的滚动动效：要有按内容出场的区块，和至少一段滑动驱动的叙事 | [滚动叙事](references/scroll-narrative.md) |
| 跨端视口、触控尺寸、窄屏弹窗与键盘遮挡 | [布局与视口](references/layout-and-viewport.md) |
| 截图工具的其他用法、检索下载素材、拼图对比 | [工具](references/tools.md) |

展示功能特性或业务证据时，先判断内容适不适合用卡片：靠大图和连续排版建立气氛的页面，不强塞卡片。

**Fork 的可选增强**：涉及已有管理后台、列表详情工作区或响应式任务布局时，按需读 [工作区与存量项目](references/craft-workspaces.md)；涉及表单、下拉、弹层、批量选择和异步状态时，按需读 [交互与状态](references/craft-interaction.md)；用户要求整页/单组件深度精修或独立有界复核时，按需读 [精修与评审](references/craft-polish.md)。这三项是 Disene Fork 独立撰写的公开能力增强，**不是官方付费版源码，也不宣称与 Oil UI Pro 功能等价**。需要具体交互实现参考时可打开 [响应式工作区示例](examples/adaptive-workspace.html)；需要卡片布局、空间折展或单组件交互原型时，按需读 [原创卡片和空间展开](references/craft-components.md)；需要 SVG 流光、点阵、Shader 或小游戏场景时，按需读 [特效与游戏状态](references/craft-effects-games.md)；项目自有设计系统及业务合同始终优先。静态方向卡或小幅样式修改不加载这些扩展。

当用户明确要求高标准视觉精修、跨方向碰撞检查或复盘反复改不满意的页面时，可选读 [有界精修方法](references/craft-polish.md)。默认不以循环获得 9/10 自评为交付条件；实际截图、用户任务完成与业务正确性分开验收。需要准备隔离评审材料时可用 [盲审材料工具](references/craft-review-packet.md)；它不调用模型、不认证评审独立性。

**Fork 可选工程核验：** 涉及新/改操作流程、异步状态、弹窗焦点、刷新读回或疑似“测试假通过”时，按需读取 [工程交互核验](references/engineering-acceptance.md)，复用原有截图工具，并针对受影响的一条真实路径执行断言。静态设计方向、小型样式修改不调用。证据脚本成功不代表实际视觉或业务验收通过；没有可运行的测试环境要如实说明。

## 评审与交付

轻路径第 4 步的评审按改动选方式，评审标准由评审者读，主 Agent 只交接材料：

| 改动 | 评审 |
| --- | --- |
| 方向探索阶段的对比页 | 先交给用户；几个首屏和版式变体不派画面评审，用户要求时再评 |
| 新界面、整体改版，选定方向之后 | 做完代表性页面、自查过截图以后派一轮，单页也照做，按问题改完再交付；10 分制，报告评分和剩余差距 |
| 已有界面润色一整页以上，或只要求评审现有界面 | 按 [视觉评审派发协议](references/visual-review.md) 的已有界面路径，一轮，不打分 |
| 小改动、局部低风险修改 | 主 Agent 自己看，不派评审者 |

- 页面有主要操作流程时，UX 走查按 [轻量 UX 走查派发](references/ux-review.md)：不给具体用户案例和预期路径，让走查者从真实页面推断目标并走一条主要路径。修正后由主 Agent 做功能验证，不强制再派。
- 风格开始漂移、意见反复时，保留最合适的版本并说明取舍；没完成的必需功能照实列出。
- 并行制作时按独立页面、素材或方向分工，不让多个执行者同时改同一份共享样式。

### 接下来可以做

交付说明的最后，列出用户接下来可以选的事。小改动、本轮停在确认点、用户已经说了下一步，或者无人值守时不列。

- 最多三条，带编号，第一条标“推荐”，末尾加一句“回复编号就行，也可以直接说想改哪里”。只列当前真能做、还没做过的，从下表挑；接后端、接真实服务这类工程任务写在“哪些没做”里。
- 每条一句话写清做完能得到什么、要付出什么：多花时间、多耗 Token、会新建或修改哪些文件、要不要用生图积分。代价没实测过就用粗略的说法，不编数字。
- 用用户的说法，不写步骤编号，也不写本 Skill 里的术语。例如“做其他页面（推荐）：沿用这一页的导航、配色和组件，会新建页面文件。”

| 刚做完 | 候选的下一步 |
| --- | --- |
| 一个方向的首屏 | 做完整页；换一个方向对比；先生成设计稿再实现 |
| 页面或核心流程 | 沿用这一页做其他页面；补动效；换一个方向对比 |
| 只读评审 | 按最重要的两三条建议修改 |

## 能力边界

看不了图时写明“未验证实际视觉”，不给视觉打分；没有可运行的环境时，不说交互已经通过。用户要能运行的界面、却只能交出方案时，标出没做完的部分。不能生成图片时，用手头合适的素材，或交一份素材需求加一个能用的占位版本。只用任务已经授权的服务，不自己接入付费服务；上不了网时用已有的参考，并说明来源。
