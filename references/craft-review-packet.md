# 可选盲审材料工具

仅在已有主 Skill / craft-polish 决定需要独立审阅时使用，不增加默认审阅轮数。独立评审仍由支持隔离上下文、实际看图的宿主执行者完成；本脚本不接模型 API、不产生评分、不调度 Agent。

```sh
python3 <skill>/scripts/review_packet.py prepare --image <任务目录>/desktop.png --image <任务目录>/mobile.png --task "核对主要操作的可发现性与层级" --out <任务目录>/review-round-1
```

只把生成的 `reviewer/` 交给评审者。`author-map.json` 留给主执行者，用于映射回原图；不交作者选型理由、历史过程或目标评分。PNG 文本/EXIF 元数据被去除，原文件名随机映射为 E01 等编号。画面本身可能仍包含作者/品牌信息，因此不能保证完全匿名。

评审 JSON 必须引用现有 evidence ID，并区分观察事实与建议。主观分数可选；最多三轮沿用既有精修约定，没有达到 9 分也真实记录差距。

```sh
python3 <skill>/scripts/review_packet.py validate --manifest <任务目录>/review-round-1/reviewer/manifest.json --report <任务目录>/review.json
```

校验仅检查证据文件完整性和报告结构。`review_type=independent` 是提交者声明，脚本不能认证独立性，亦不能据此宣称交互或真人业务验收通过。修复后仍需沿原来失败的操作路径复核。

无支持的独立执行者时，继续自查能够完成的部分，标明“未独立评审”；不要为了本工具新增 Agent 平台、付费模型或全局流程。
