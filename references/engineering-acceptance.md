# 可选工程交互核验（Fork 增强）

此文档是 `Disene/oil-ui-craft` 的**可选工程增强**，不是 Oil UI 官方 Pro 的代码或功能等价声明。原版负责设计方向、视觉方案、截图与评审；这里仅在**真实交互或状态会影响交付结果**时补充可执行断言与谨慎的证据汇总。

## 什么时候调用

- 新建或修改了列表→详情→编辑→返回、搜索筛选、导入、弹窗/抽屉、跨页导航、异步结果、错误恢复、刷新读回等**真实操作路径**。
- 页面存在焦点逃逸、文字/图表重叠、水平溢出、按钮失效、看上去通过却有 JS 异常等迹象。
- **不调用**：只是出设计方向卡、静态首屏候选，或者指定的低风险文案/颜色小改。只设计、未改代码时也不用假装已做浏览器业务验收。

## 执行方式（工具按需）

1. 遵照主 Skill `references/tools.md`，优先使用已有 `scripts/shoot.mjs` 对受影响视口截图或录屏。**不要重新运行独立截图器**。
2. 关键交互需要可重复验证时，准备一个小 JSON 旅程。首次使用需要用户环境提供 `python3 -m pip install playwright` 和 Chromium，已有浏览器可用 `--browser-path` 指向它。此依赖是**可选**的；如果组织策略禁止安装或启动浏览器，停止并说明“未验证”，不绕过策略。
3. 运行旅程：`python3 <skill>/scripts/ux_journey.py --spec <项目内旅程.json> --out <项目内证据目录>/journey`。`<skill>` 指本 Skill 的**绝对安装路径**，不是业务项目当前目录。旅程使用独立浏览器上下文，不共享用户日常浏览器会话；需要鉴权的真实流程必须在已获授权的测试环境中进行。
4. 选做汇总：`python3 <skill>/scripts/ux_gate.py --shoot <shoot生成目录>/report.json --journey <证据目录>/journey/result.json --out <证据目录>/summary.json`。任一源文件缺失时，不要把缺失当 PASS；只汇总现有且**确实执行过**的任务。

旅程 JSON 示例（选择器需用项目真实界面替换）：

```json
{
  "name": "dialog-keyboard-path",
  "viewport": "390x844",
  "baseUrl": "http://127.0.0.1:8080/",
  "steps": [
    {"action":"goto", "path":"/"},
    {"action":"click", "target":"[data-testid=open-dialog]"},
    {"action":"expectVisible", "target":"[role=dialog]"},
    {"action":"expectFocused", "target":"[data-testid=dialog-close]"},
    {"action":"press", "key":"Escape"},
    {"action":"expectHidden", "target":"[role=dialog]"},
    {"action":"expectFocused", "target":"[data-testid=open-dialog]"},
    {"action":"expectNoDocumentOverflow"},
    {"action":"screenshot"}
  ]
}
```

支持的动作以 `python3 <skill>/scripts/ux_journey.py --help` 和源文件 `ACTIONS` 为准。`expectText / expectValue / expectCount / expectAttribute / expectUrl / expectFocused` 会等待异步状态，避免“点击后立即读取一次”造成假阴性。`loadHtml` 只用于可信的本地小型静态 fixture，不代表真实服务器路由测试。

## 必须明确的结果层级

| 报告字段 | 正确解释 |
| --- | --- |
| 旅程 `execution_status=pass` | 已运行所有指定步骤并满足断言；**不等于**视觉或业务通过 |
| 旅程 `status=attention` | 步骤可能全部成功，但检测到未捕获 JS/Console 错误 |
| 旅程 `status=fail` | 断言失败、工具错误或浏览器未能运行；停止宣称通过 |
| 汇总 `no_automated_findings` | 本次指定证据中无自动发现；**不能写成“UI/UX PASS”** |
| 汇总 `attention` / `fail` | 有待复核问题 / 证据或执行失败，分别处理 |

**最终验收还应由执行者实际查看截图及关键交互结果。** 真实业务数据口径、权限、同步状态、生产发布及历史 BUG 都由各项目自己的规范、测试和 Issue 负责，本 Skill 不储存它们。

## 范围与隐私

- **按实际风险选旅程**：通常只验证一条改动影响的完整路径；改共享组件再检查直接相关页面。不要默认启动多 Agent、多浏览器或全站检查。
- 测试应优先在**合成数据/测试账户**上执行。证据截图可能包含可识别业务数据，留在项目允许的证据目录，不上传公开 Fork。异常报告默认只存错误类别，不保存完整 Console 文本；断言中的目标选择器可能保留。
- 报告只证明执行过的路径和视口，不证明未覆盖的状态。Playwright 未安装、浏览器被组织屏蔽时，明确记录未执行，不下载依赖或尝试绕过限制。
