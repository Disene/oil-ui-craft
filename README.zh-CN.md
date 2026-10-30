[English](README.md) · 中文

# Oil UI Craft

基于 [oil-oil/oil-ui](https://github.com/oil-oil/oil-ui) 的 MIT 开源 Fork。保留上游设计探索、风格比较、截图/录屏和评审流程；按任务补充可运行的交互原型与工程核验。**不是官方 Oil UI Pro，不包含其私有源码，也不宣称审美质量或功能逐项等价。**

继承的上游版本：`0.28.0`。本批独立增强：`craft-ux.3`。若正在查看尚未合并的 PR 分支，常规安装仍读取 main，不会自动安装本分支。

本候选整合上游 `56240e1`，保留 Craft 示例与 Fork 更新保护，并排除上游新增 Actions。本 PR 不更新本机已安装的 `craft-ux.2`。

## 现在可以使用什么

| 范围 | 可用结果 | 边界 |
| --- | --- | --- |
| 基础设计能力 | 上游方向探索、视觉语言、素材、滚动叙事、截图还原 | 保留原版，不重复写一套引擎 |
| 既有产品/后台 | 三类修改意图、整理/升级/重塑强度、十类独立工作区选型 | 这是设计方法，不是十套生产后台 |
| 表单与状态 | 键盘/IME、弹层、失败恢复、列表详情与批量入口 | 按实际任务读取，不全量套用 |
| 原创组件 | **19 套**：前六种空间卡片 + 十三种交互模式 | 不与官方十九套一一对应 |
| 特效 | SVG 流光、Canvas 点阵、WebGL 渐变源码及 CSS 降级 | 前轮已验证 WebGL 渲染/恢复与降级；本轮沿用记录 |
| 小游戏 | 一个可运行的配对游戏，含准备/进行/暂停/胜败/重开 | 不声称覆盖所有类型游戏 |
| 独立精修 | 最多三轮的可选方法、去作者线索的截图材料工具 | 工具不调用模型，不能证明实际独立评审 |
| 工程验证 | 可选旅程、谨慎汇总、Fork 更新防覆盖 | 不等于真人/业务/生产验收 |

[打开所有示例](examples/index.html) · [组件说明](references/craft-components.md) · [特效与游戏](references/craft-effects-games.md) · [验证记录](docs/VALIDATION.md)

示例 HTML/CSS/JS 分离，内容全部合成，无在线字体、付费服务或真实账号写入。复制到业务项目时复用其既有设计系统和数据合同，不整包植入第二套系统。

## 安装和更新

```sh
npx skills add Disene/oil-ui-craft
```

Skill 名称仍为 `oil-ui`；不要同时启用两个同名安装。仓库里的候选代码、合并到 main、用户机器上的安装版本是不同状态。

Fork 不运行官方 Oil CLI 原地升级。`check_update.py` 检测到 `fork_release` 时拒绝上游 `--update`，避免增强文件被覆盖。吸收上游新版本应先在此 Fork 比较、测试和合并，再更新安装副本。

## 使用

主 `SKILL.md` 依任务加载工作区、交互、精修或组件参考；没有改变默认小改动的范围。项目数据口径、权限策略、品牌规范与历史 BUG 留在项目已有文档、代码和 Issue，不加入全局 Skill。

对模型明确说用户目标和交付类型即可，例如：“沿用现有品牌，把这个列表详情任务做得更顺；复用已有组件，检查原入口与返回路径。”不需要每次要求跑所有原型、所有视口或独立多轮审阅。

## 本地验证

Python 3.10+；浏览器测试可选依赖 Playwright 与获准的 Chromium。缺依赖/不允许运行时记录未执行，不修改组织策略。

```sh
python -m unittest discover -s tests -p 'test_craft*.py' -v
python -m unittest discover -s tests -p 'test_fork_update.py' -v
python -m unittest discover -s tests -p 'test_review_packet.py' -v
```

历史证据包含 **23/23 聚焦测试**、后续工作台 **7/7**（覆盖有重叠），以及各自提交范围内的 HTTP/WebGL 和独立视觉验证。本次 0.28.0 同步仅验证受影响工具和 Fork 保护，具体结果与未运行项见验证记录；不将历史结果冒充本轮重跑。原生缩放、读屏、真机和生产业务仍未验证。无新增 Actions 或云端费用。

## 来源与许可

上游方法与代码来自 [Oil UI](https://github.com/oil-oil/oil-ui)。公开对标依据：[开源 / Pro 差异](https://github.com/oil-oil/oil-ui/blob/main/README.zh-CN.md#开源版和-pro)、[官方介绍](https://ui.oiloil.org/intro/)。Fork 的工作区分类、组件、特效、游戏和辅助工具为独立实现。

[MIT](LICENSE)，保留原作者版权声明。不要将这些示例宣传为官方 Oil UI Pro。
