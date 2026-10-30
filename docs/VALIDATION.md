# Craft UX.2：独立实施与聚焦验证

最新候选（2026-10-31）：同步上游 `56240e1` / Oil UI `0.28.0`，Fork 标记为 `craft-ux.3`，保留 Craft 按需增强与更新保护，排除新增 Actions。受影响范围 12/12 定向测试及新版截图工具的列表→详情序列图检查通过；未重跑完整矩阵。本候选尚未合并，本机安装仍为 `craft-ux.2`，77 个文件未变。具体证据与未运行项见文末同步记录；此前 PR #2 的合并/安装记录属于历史基线。

基线：PR #2 的 `a3faa7e257ba39219b45512c519498cd6125e1ec`。本轮不修改 StepWise、不安装用户机器 Skill、不合并或部署、不新增 Actions 或付费服务。

## 可用结果

- 原有 01–06 空间卡片保留；新增 07–19 趋势、容量、预约、计算器、任务撤销、微抽屉、对比、画窗、文件选择、折叠说明、准备清单、中文组合框和失败恢复设置。
- 原创 SVG/Canvas/WebGL 三种材料，支持暂停、减少动态效果和 CSS 降级。
- 一个配对小游戏，含准备、进行、待复位、暂停、胜利、失败、重开与键盘操作。
- 可选盲审截图材料生成/报告校验工具，不调用模型，不伪造独立审阅。
- 工作台在 320/390/1024px 下的 200% CSS 放大溢出已修复；采用内容容器断点，不缩小字号隐藏问题。

## 实际执行

运行环境：Python 3.13.5、Node 22.16.0、Chromium 144.0.7559.96、已安装 Playwright。未安装新依赖。定向复制的已有关联源文件用 Git blob 与远端固定提交核对，不把该工作目录称作完整仓库 checkout。

| 测试文件 | 结果 | 覆盖 |
| --- | --- | --- |
| `test_craft_cards.py` | 5/5 | 原六卡片、展开/Escape/返回焦点、320/390/768/1440、CSS 200%、减少动态效果 |
| `test_craft_workspace.py` | 5/5 | 现有四项补跑，加容器宽度与 CSS 放大回归 |
| `test_fork_update.py` | 1/1 | 原版更新入口不会替换带 Fork 标记的安装 |
| `test_craft_extended.py` | 9/9 | 13 模式交互、IME 合成事件、无网络请求、SVG/Canvas 暂停、特效降级、游戏完整胜败/暂停/重开、布局 |
| `test_review_packet.py` | 3/3 | 去元数据、隐藏来源名、证据引用/文件变更/无效轮次拒绝 |
| **总计** | **23/23；0 跳过** | 不是上游全套测试矩阵 |

所有页面测试装载完整作者 HTML/CSS/JS 到内存，浏览器实际执行事件和状态；不是仅语法分析或替代 DOM。截图实际查看了桌面组件、窄屏游戏和特效降级画面；不声称独立视觉盲审或完整录像验收。

## 发现并修复的反例

1. 原工作台既有四项测试通过，但扩展 CSS 200% 检查后，在 320px 溢出 153px、390px 溢出 83px、1024px 溢出 158px。新增容器断点与局部折行后相同检查通过。
2. 新容量环在 320px / CSS 200% 时超出 34px。限制到可用内容宽度后通过，没有缩小正文。
3. 截图检查发现文件选择器样式与界面不一致、胜利后“开始/重开”重复；已调整，同时保留原生文件选择与可访问焦点。

## Chat 阶段尚未完成

以下是前一执行环境的记录；本机接续结果见下一节。

- **真实 HTTP 载入**：本机临时合成 HTTP 页面被 Chromium 返回 `ERR_BLOCKED_BY_ADMINISTRATOR`，已停止该路径，不更换端口/地址或修改策略绕过。该项不能由内存测试替代。
- **WebGL 实际渲染**：本环境 `getContext('webgl')` 不可用，实际走 `css-fallback`。着色器源码已实现，不能报告真实 GPU/WebGL 通过；上下文恢复分支也未实跑。
- **真正的独立 Agent 多轮评审**：当前没有可调用的隔离视觉执行者。已完成材料和方法；本轮只有主执行者自查。
- 真实业务、触屏、屏幕阅读器、原生浏览器缩放与生产运行未验证，不把它们扩大成本批所有普通开发的前置门槛。

这三项环境/执行者缺口是下一阶段的具体接续对象；其余本轮开发和定向测试已在 Chat 完成，不需要让 Codex 重写或重跑已验证的整个项目。

## 2026-10-24 本机接续：浏览器权限受限

本轮固定验证对象为 `b9eed5673a5dce1b28d9a67ed3a853fa24665ce0`。已核对本地干净 checkout 与 PR #2 原分支 `feat/pro-level-workbench-ux` 的远端 HEAD 一致。本次只补充验证记录，不修改示例实现，不重跑 23 项聚焦测试或完整测试矩阵，不新增工作包、依赖或 Actions。

| 项目 | 状态 | 证据与范围 |
| --- | --- | --- |
| 固定提交及原 PR 分支 | 已通过 | 接续开始时，本地 `git rev-parse HEAD`、远端 `git ls-remote` 与 PR 元数据均为上述 SHA；后续接续提交只更新本验证记录，示例实现未变；PR 为 open / Draft |
| 23/23 聚焦测试、6 页的 22 处本地资源引用无缺失 | 已通过（Chat 既有结果） | 接续用户已确认；本轮未重跑，不能据此宣称 HTTP 加载通过 |
| 本机 Chrome HTTP 完整静态资源加载 | 环境受限，未通过完整验证 | 已启动仅监听 `127.0.0.1:8765`、以 `examples/` 为根的临时 HTTP 服务；用户手动打开入口后，服务日志记录 `GET /` 为 200、浏览器标签清单显示正确标题。但浏览器工具仍拒绝读取现有页面，未取得其余页面及完整资源加载证据 |
| 代表性交互 | 未运行（受上述限制） | 没有获准载入的 HTTP 页面，未执行本轮交互；前一轮内存装载测试仍只作为历史结果 |
| WebGL 渲染及上下文恢复 | 未运行（受上述限制） | 没有进入页面，不能判断本机 WebGL 能力；没有强制软件渲染或更改 GPU/安全策略 |
| CSS 降级 | 保留实现；本轮未运行验证 | 前一 Chat 环境的 `css-fallback` 记录保留，不冒充本机复验 |
| 独立视觉 Agent 审阅及主执行者同路径复核 | 未运行（受上述限制） | 本轮有隔离 Agent 能力，但没有可供审阅的实际渲染页面/截图，因此未启动无实渲染证据的视觉审阅，也没有可复核的问题路径 |

浏览器授权的实际顺序：首次访问被门禁拒绝，返回用户拒绝授权；随后用户明确选择“授权该本机地址继续验证”，再次访问同一 origin 仍被拒绝，返回 `A saved user permission setting blocks this action`，并说明保存权限或托管策略禁止访问。用户随后说明“目前已授权为完全访问”，在重启同一本机服务后，对同一 Chrome、同一 origin 的重试仍返回相同的保存权限/托管策略拒绝。这里的限制来自浏览器工具授权门禁，不能误报为当前页面返回了 `ERR_BLOCKED_BY_ADMINISTRATOR`。

用户又手动打开了该地址。工具能列出已有 Chrome 标签页，其 URL 为同一 origin，标题为“Oil UI Craft · 交互参考”；尝试连接该用户标签页时，门禁仍以相同保存权限/托管策略原因拒绝 `observe page content`。标签标题与服务端入口 200 不等于页面实渲染、其余静态资源或交互通过。另有浏览器默认请求 `/favicon.ico` 的 404，该路径未在页面声明，不作为组件实现缺陷或完整资源验证结论。

随后文件系统权限实际切换为完全访问，用户要求重试。本轮重启同一服务，检查同一 Chrome 的标签清单后，对 `http://127.0.0.1:8765/index.html` 的导航仍被 origin 门禁以 `A saved user permission setting blocks this action` 拒绝；未取得新的页面、资源或交互证据，以上状态不变。

用户随后重启 Chrome 和桌面客户端，并提供了客户端 Google Chrome 权限管理页面截图。截图明确显示 `http://127.0.0.1:8765` 的“浏览”为“始终允许”。按用户要求再次连接原页面，浏览器工具仍在读取内容前以相同的保存权限/托管策略原因拒绝访问。**已确认界面许可与工具判定不一致；不能继续归因于用户尚未授权，也没有证据确定是状态同步问题或托管策略覆盖。** 截图只用于本次诊断，不上传整张权限列表到 PR。

前面各次受限检查后曾停止临时服务；按用户要求已重新启动并保持运行。最新检查确认仅 `127.0.0.1:8765` 处于监听状态。服务启停造成的连接拒绝与浏览器工具的访问拒绝分别记录。没有换地址、端口、浏览器、原始 CDP 或其他调用方式绕过门禁；没有取得可证明实际缺陷的渲染或交互证据，因此没有实现修复。

**交接状态：保留 PR #2 为 Draft。** 完整 HTTP 加载与本轮交互尚无证据，不能据此判定达到 Ready 标准。继续前需排查客户端显示“始终允许”而工具仍拒绝同一 origin 的不一致；用户已完成站点许可设置和重启，不能再以重复授权或重启替代定位。若为组织策略覆盖，应由管理员确认；否则需向客户端/Browser Use 支持提供本轮的界面状态与拒绝信息。工具恢复后仍只补上述 HTTP、代表性交互、可用时的 WebGL 渲染/恢复或 CSS 降级，以及一次独立视觉与同路径复核；不重复已完成开发。未合并、安装或部署。

## 2026-10-24 最新接续：HTTP 实渲染完成与局部修复

起始工作目录及原 PR 分支 HEAD 为 `5cc91799e8722abec399ce77d45681e4a5ef4349`；与用户指定的 `b9eed5673a5dce1b28d9a67ed3a853fa24665ce0` 比较，仅 `docs/VALIDATION.md` 有变化，示例实现完全一致。先对该固定实现完成验证，再按用户本轮实际发现的三项视觉问题修复；修复后的实现提交为 `8ca4f76a9b6692f7df3537163b4c6ce2e26f12e0`。没有重新开发十九套组件、整理设计规范、运行全量矩阵或新增工作包、Actions、依赖。

本轮使用 IN-APP 浏览器，访问现有仅监听 `127.0.0.1:8765`、以 `examples/` 为根的 HTTP 服务。该浏览器正常读取页面；没有改地址、端口或安全策略。此前 Chrome 工具门禁不一致的原因本轮未诊断，也不宣称 Chrome 路径已修复。

| 项目 | 状态 | 本轮实际证据与边界 |
| --- | --- | --- |
| 六页完整 HTTP 静态资源加载 | 已通过 | 入口、卡片、07–19 组件、特效、游戏、工作台六个 HTML，以及四组 CSS/JS，共 14 个唯一 HTTP URL；浏览器 Network 响应均 200、MIME 正确，逐一匹配 `loadingFinished`，无 `loadingFailed`；下拉箭头另为两个内联 SVG data URL，无外部依赖 |
| 控制台及运行异常 | 已通过 | 本次标签采集的 warn/error 日志为空，已启用的 Runtime 异常事件未发现未捕获异常；不把旧轮次的 favicon 请求扩展为本轮组件缺陷 |
| 卡片与组件代表性交互 | 已通过 | 信号详情展开、Escape 关闭及焦点返回；14:00 预约确认；任务前进及撤销；中文“阅读”搜索、方向键/Enter 选择并关闭候选；设置模拟失败后保留更改并重试成功 |
| 游戏代表性交互 | 已通过 | 开始、方向键移动到第二张及 Enter 翻牌、暂停遮挡、继续、打开规则自动暂停、Escape 关闭并返回规则入口、重新开始清零；难度切到 8 步后 HUD 同步；未重跑本轮胜败全流程，前轮聚焦测试结果保留 |
| 工作台代表性交互 | 已通过 | 390px 列表进入长账号详情、返回原账号焦点；搜索 support-lin、勾选并进入批量区域、返回批量入口；状态筛选停用后只保留一个账号 |
| WebGL 实际绘制及上下文恢复 | 已通过 | 取得真实 WebGL context，读取到 RGBA 像素；运行中两次帧缓冲采样摘要由 265978375 变为 3345857971。使用 `WEBGL_lose_context` 主动触发丢失，随后 restore；恢复后 renderer=webgl、canvas 可见、isContextLost=false、getError=0，中心像素为 [76,69,113,255]。验证浏览器 WebGL 路径，不宣称物理 GPU/驱动故障恢复 |
| CSS 降级与减少动态效果 | 已通过 | 丢失时 renderer=css-fallback、canvas hidden=true，实际可见静态 CSS 径向渐变和状态说明；系统减少动态效果下显示静态画面且暂停按钮禁用。临时模拟 no-preference 后手动暂停/继续正常；最终清除模拟覆盖 |
| 焦点间隙修复 | 已通过 | 工作台 select 实际复现 3px 间隙；六页七处显式 outline-offset 3/4px 改为 0，保留原轮廓颜色/宽度。六页键盘焦点均实际复查 `:focus-visible` 且 computed offset=0px；独立视觉补核仍清晰可辨 |
| 上传区同排修复 | 已通过 | 原 grid 导致图标/按钮分行；改为 flex 同排居中。390/320px 下图标与按钮中心 Y 相等，无横向溢出；选择 21 字节合成 CSV 后显示文件名与“未上传”，清除后状态恢复；没有上传或读取文件正文 |
| 下拉箭头边距修复 | 已通过 | 工作台/游戏两处原生 select 保留；用内联装饰 SVG 将箭头定位到 right 12px，文字 padding-right=36px。桌面/390px 无文字重叠，筛选和难度切换正常；游戏强制颜色模拟下退回 appearance=auto、background-image=none，随后复原 |
| 独立视觉审阅与同路径复核 | 已通过 | 隔离视觉 Agent 查看实际 HTTP 截图，主执行者沿发现路径复核；一张全页截图疑似窄屏详情收缩，按 390px 列表→长账号详情重新操作，实际 body/main=390px、详情=358px，当前视口截图正常，审阅者撤回 P1 候选。个别截图采集缩放异常不作为产品缺陷。三项用户反馈修复后视觉补核通过，无剩余已证实阻塞缺陷 |
| 23/23 聚焦测试及 22 处本地引用检查 | 已有通过结果，本轮未重跑 | 保留 Chat 既有结果；本轮以上是增补的 HTTP/浏览器验证，不将既有测试冒充修复后重跑 |
| 原生浏览器 200% 缩放、读屏、触屏真机、生产业务、真实硬件故障、WebGL 启动即不可用分支 | 未运行 | CSS 200% 等前轮结果仍仅为历史覆盖；本轮启动时 WebGL 可用，CSS 降级通过真实 context loss 进入验证 |

本轮关键本地证据文件：`http-summary.json`（14 项 HTTP 状态/完成事件匹配）、`focus-before.jpg` / `focus-after.jpg`、`patterns-focus-after.jpg`、`upload-desktop-after.jpg` / `upload-mobile-after.jpg` / `upload-320-after.jpg`、`select-workspace-mobile-recheck.jpg`、`select-game-after.jpg`、`effects-context-loss.jpg` / `effects-restored.jpg`、`workspace-mobile-detail-recheck.jpg`。它们保存在本次聊天本地截图目录，未新建仓库证据包或上传机器路径、权限设置截图及个人文件。截图异常的旧图不作为验收依据。

`git diff --check` 通过。实现修复限定在六个现有文件的焦点、上传排列及下拉装饰样式，未改变应用状态机。临时视口、动态效果、强制颜色与缓存覆盖均已复原。**可用标准已达到，原 PR #2 可转 Ready 供整合判断；不自动合并、安装或部署。**
### 同轮追加：账号权限列排版

用户截图确认权限列将两项权限串成单段，换行拆开“账号管理”。实现提交 `9a2d5cc42d6f75487343c4087b129aac4ed83fc1` 将列表权限改为语义 `dl`：内容发布、账号管理各占一行，名称列固定 4em，结果列对齐；极窄有效容器保留堆叠与折行能力。没有改权限值、筛选或状态机。

**已通过**：桌面与 390px 实渲染截图，320px 下十个权限块均 clientWidth=scrollWidth=216、文档 clientWidth=scrollWidth=305；检查内容维护者、管理员的两项权限值及详情一致，详情返回、勾选管理员、批量入口与返回均正常。隔离视觉 Agent 查看 `permissions-desktop-after.jpg`、`permissions-mobile-after.jpg`，确认无拆词、裁切、重叠或错位；主执行者沿相同路径复核通过。`permissions-column-after.jpg` 保留修复后的列局部截图。

本轮共修复四项用户实际指出的视觉问题。以上为定向浏览器回归，仍未重跑 23 项聚焦测试、完整矩阵、读屏或触屏真机；其余状态及限制沿用上表。原 PR #2 满足转 Ready 的验证条件，不自动合并、安装或部署。


## 2026-10-24：账号工作台动效与悬停下划线定向修复

用户反馈：工作台几乎没有动效，账号名称鼠标悬停出现固定下划线。源码确认为设计演示中的真实行为：原先只为按钮背景/边框设置约 150ms 过渡，账号名称虽是 `<button>`，却通过 `.namebtn:hover{text-decoration:underline}` 模仿超链接。

修复限定在 `examples/adaptive-workspace.html` 与对应 `tests/test_craft_workspace.py`：

- 账号名称 hover 改为颜色强调、无下划线；账号行 hover 用低对比背景反馈；真实链接的语义和样式不做全站覆盖。
- 按钮 hover/press、选择后工具栏入场、详情切换与原生 Dialog 展开分别采用约 120–190ms 的微动效；不增加持续循环或装饰性动画。
- `prefers-reduced-motion: reduce` 下关闭新增动画和过渡；键盘焦点轮廓、Escape/返回焦点、批量选择状态保留。

**本轮实际验证**：Python 3.13 + 系统 Chromium + Playwright，完整作者 HTML 用 `set_content` 装载；新增两项测试加原五项，执行 `python -m unittest discover -s tests -p test_craft_workspace.py -v`，**7/7 PASS，0 失败/跳过**。覆盖 390px/1440px、CSS 200% 不溢出、hover 计算样式无 underline、reduce 与普通模式动画开关、详情/弹窗焦点回归、批量勾选操作。实际查看了相同视口的前后截图；这次没有重新做 HTTP 网络加载、原生浏览器缩放、全量上游测试或用户真人体验。

实施版本：工作台 Git blob `acb0df640cc6ec6f23c1a75aa47005677b79d3bc`、聚焦测试 Git blob `43f326e4d14ca1ab72434723bef182facde49727`，与 Chat 中已跑测试源码一致。历史 HTTP/WebGL 验证仍属于先前提交及记录，不能冒充本轮重新执行；未修改真实业务项目、生产环境或其他组件示例。

## 2026-10-24：远端 0c7af40 的 HTTP 定向复核与合并判断

### 对象与反馈

接续时远端 PR #2 HEAD 为 `0c7af400d09bf16e7105c216f61ac3651b30accc`，工作目录干净，已 fast-forward 到该提交。读取了 PR 当前描述、全部讨论及行内审阅线程；最新反馈为账号工作台动效与悬停下划线修复记录，行内审阅线程为空。当前描述中仍将 `bc407d5` 写成最新 HEAD，本轮同步修正文档和 PR 元数据，不修改已通过复核的实现。

工作台 HTML Git blob 为 `acb0df640cc6ec6f23c1a75aa47005677b79d3bc`，测试文件 Git blob 为 `43f326e4d14ca1ab72434723bef182facde49727`，与前节 7/7 的测试对象一致。相对 `bc407d5`，示例运行时代码只有工作台变化，其他五页及其资源未变；历史 WebGL、完整 HTTP 和独立视觉证据继续按原范围使用。

### 本轮实际运行

使用现有本机 origin `http://127.0.0.1:8765` 的真实 HTTP 页面；桌面视口 1207×892，工作台窄屏 390×844，上传区抽查 320×700。没有重跑 Python 聚焦测试或完整矩阵，也没有增加测试体系、功能、Actions 或依赖。

| 项目 | 状态 | 实际观察 |
| --- | --- | --- |
| 工作台 HTTP 与控制台 | 已通过 | 新载入文档响应 200 / text/html、内联 SVG 正常；本轮采集未出现 loadingFailed、未捕获 Runtime 异常或 warn/error。只称工作台本轮 HTTP 通过，不重报整套 14 URL 已重跑 |
| 普通模式真实动效 | 已通过 | 通过临时浏览器观测记录到 selectedBar 的 craft-selection-in、Dialog 的 craft-dialog-in 及 backdrop 的起止事件；透明度由中间值到 1。详情 WAAPI 实际运行 190ms，transform 从 translateY(7px) 到 none 并完成；不是仅检查 CSS 声明 |
| 悬停与非链接语义 | 已通过 | 实际指针移入账号按钮，:hover=true、文字颜色/行底色变化，textDecorationLine=none；移开后无下划线。减少动效模式下再次 hover 仍无下划线，颜色为 rgb(30,83,197)、transitionDuration=0s。程序聚焦的详情标题也无下划线 |
| 减少动态效果 | 已通过 | 390px reduce 模式下，详情未调用 WAAPI、工具栏及 Dialog animationName=none、按钮 transitionDuration=0s；详情、勾选、弹窗及 Escape/返回焦点照常；观察器没有记录新增 CSS/详情动画 |
| 代表性交互 | 已通过 | 桌面勾选→批量入口→返回焦点到 jump；详情切换→导入 Dialog→Escape 焦点返回导入；390px 列表→长账号详情→返回原账号按钮，详情标题完整、两项权限可读，文档 clientWidth=scrollWidth=390 |
| 焦点轮廓与下拉箭头 | 已通过 | 账号状态 select 经键盘 Tab 获得 :focus-visible；outline-offset=0px，箭头 right 12px、右 padding 36px，未见回退 |
| 权限列视觉 | 已通过 | 桌面与 390px 实际截图中两项权限各占一行、名称和值对齐；长账号详情没有拆词异常、裁切或横向溢出 |
| 上传区视觉 | 已通过 | 未改动的组件页抽查 320px，图标/按钮中心 Y 同为 580.34375，document clientWidth=scrollWidth=305，焦点 offset=0px；视觉确认同排且可辨。选择/清除行为沿用前轮实测证据，本轮未重复选文件 |
| 历史测试/其他示例 | 复用，不重复运行 | 23/23 原聚焦测试、后续工作台 7/7、六页 14 URL 完整 HTTP、WebGL 渲染/恢复和 CSS 降级、游戏胜败、独立视觉审阅均按原记录及源码范围引用；7/7 与原 23 项有重叠，不相加为 30 项 |
| 本轮未运行/环境边界 | 明确保留 | 未重跑 WebGL/context loss、游戏全流程、完整矩阵、CSS 200% 或原生浏览器缩放、触屏真机、读屏及生产业务；Chrome 工具历史授权问题未重新诊断。本轮为主执行者视觉复核，不冒充新增独立 Agent 审阅 |

本轮本地证据：`latest-motion-evidence.json`、`latest-http-events.json`、`latest-workspace-hover.jpg`、`latest-workspace-dialog.jpg`、`latest-workspace-mobile-detail.jpg`、`latest-workspace-reduced.jpg`、`latest-upload-320.jpg`、`latest-workspace-final.jpg`。沿用当前聊天本地证据目录，未创建仓库证据包、上传机器路径或个人文件。临时动画观测包装通过重新载入清除，视口、减少动效及缓存覆盖均已复原。

### 判断

**已具备本次候选的合并条件：未发现已知遗留阻塞缺陷。** GitHub 在受审 HEAD 上返回 Ready（非 Draft）、MERGEABLE、mergeStateStatus=CLEAN；没有未解决行内审阅线程。statusCheckRollup 为空，表示没有报告自动检查，不能表述为 CI 全绿或已有外部批准。既有 7/7 与本轮 HTTP/浏览器证据支持当前判断；本节列出的未运行项仍保留其边界。

本轮仅更新现有验证记录及 PR 摘要。待用户批准后才可合并；未修改 StepWise，未合并、安装或部署。

## 2026-10-31：上游 0.28.0 同步候选（craft-ux.3）

### 基线与整合决定

- Fork 基线：已合并 PR #2 的 `84e67152b1acbff661d35ae75bbece0290982b60`；上游固定为 `56240e1f9600088b6e658c9c2b37acbb91bfb95b`（0.28.0），共同基线为 `a66a177`。同步分支 `codex/sync-oil-ui-0.28.0`。
- 吸收上游主流程、默认单方向/显式探索、只读评审、任务工作区、轻量证据规则，以及截图根目录、序列帧、同比例裁切和图片路径修正。
- `SKILL.md` 人工整合：version=0.28.0 / fork_release=craft-ux.3；保留 Fork 更新保护、Craft 按需路由、可选精修与工程核验，不恢复官方自动检查命令、allowed-tools 或付费推荐入口。已选方向和存量任务仍沿用主入口的局部路径，不强迫重新探索。
- 两份 README 保留 Fork 身份与安装说明，更新候选版本及历史证据范围；不把旧“WebGL 未运行”说明继续当成最新状态。
- 上游新增 `.github/workflows/tests.yml` 从最终合并树排除。本分支保留上游 Git 祖先以便后续同步，但 PR 相对 Fork main 的文件差异不包含 Actions。
- `examples/`、`assets/`、全部 `references/craft-*.md`、工程旅程与更新保护实现保持原样；不新增功能、不改 StepWise、不更新本机安装。

### 实际验证

Windows 本机 Python 3.10.11、Node 24.0.1、已安装 Google Chrome；未安装新依赖。运行既有用例的选定子集，**共 12/12 通过、0 失败、0 跳过**，一次运行约 29 秒。

| 既有测试范围 | 结果 | 直接覆盖 |
| --- | --- | --- |
| `test_workdir.WorkdirTests` | 5/5 | 过程文件忽略与任务隔离；显式静态服务根和共享 CSS；拒绝越界/过宽根及敏感文件/符号链接泄漏；素材缓存、对比页和正式图片/srcset 输出路径 |
| `test_fork_update.ForkUpdateProtection` | 1/1 | 含 fork_release 的安装拒绝上游 --update，不发起网络/npm，不改 Skill 或写更新状态 |
| `test_shoot.ShootCLITests.test_stitch_scale_crop_forms_and_actionable_errors` | 1/1 | 同比与裁切参数、错误提示 |
| `test_shoot.ShootBrowserTests` 的三个新用例 | 3/3 | 共有元素同比缩放后裁切；--frames 不编码视频（普通及 evidence）；编辑器/面板中的内容卡片 lint |
| `test_prep_image.PrepImageCLITests.test_parse_args_and_windows_file_url` | 1/1 | Windows 路径编码与参数形式；实际图片输出另由工作区用例覆盖 |
| `test_oiloil_image.OiloilImageTests.test_recovery_command_quotes_literal_paths_for_the_shell` | 1/1 | Windows 恢复命令路径/字面量转义；仅使用测试回环服务与假凭据，不调用真实生图服务 |

三个截图浏览器用例为 `test_stitch_normalizes_common_elements_and_crops_after_scaling`、`test_frames_without_record_skips_encoder_for_actions_and_evidence`、`test_lint_allows_content_cards_inside_panels_and_editors`。可从 tests 目录用 unittest 指定上述类/方法复现；没有运行整个截图测试文件或全部 Craft/上游矩阵。

另用新版截图 CLI 对未修改的 `examples/adaptive-workspace.html` 执行一次真实 HTTP 列表→详情：显式 --root 为仓库根，390×844、--frames 6、--hold 300、命名步骤 `detail: click button[data-open=content-reviewer]`。生成六帧带时间序列和起/中/终态图，未编码视频；report issues=[]，工具报告无控制台错误、横向溢出或加载失败图片。主执行者实际查看序列图：列表和详情字段完整、布局正常。序列图只证明状态与变化，不冒充正常速度手感或独立视觉评审。

证据保存在当前聊天本地截图目录的 `upstream-0.28.0/`（motion-detail-sequence.png、起/中/终态和 report.json），不提交截图、机器路径或过程数据到仓库。

静态完整性：主 Skill 37 个本地链接全部有效，版本与 Fork 路由正确，无冲突标记；受保护的示例/增强参考/更新器相对 Fork 基线无差异，最终树不存在新增 workflow。对本机已安装 craft-ux.2 的 77 个文件重新做 Git blob 核对，全部仍匹配 84e6715，没有更新安装。

### 未运行与剩余事项

- 没有复跑十九组件、完整 HTTP 资源矩阵、WebGL/context loss、游戏胜败、读屏、真机或生产业务；示例未变，历史证据按原提交范围保留。
- 没有本轮独立视觉 Agent 评审或新设计评审循环；本次是上游工具与入口规则同步，不重设计示例。
- 已运行用例没有失败或环境跳过；macOS/Linux 执行结果未验证。默认单方向等提示词行为通过文本整合审查，未用真实用户任务证明跨模型执行效果。
- 当前未发现已知阻塞缺陷；PR 供审阅，未经用户批准不合并，不更新本机安装，不部署。本轮没有引入 Actions，因此不以缺少远端 CI 结果伪称 CI 全绿。