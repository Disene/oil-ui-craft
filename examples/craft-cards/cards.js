// Independent demonstration only. Static content, no external requests or writes.
(() => {
  'use strict';
  const data = {
    signal: { kicker: '01 / SIGNAL MONITOR', title: '系统信号 · 一周概览', lead: '把重要健康指标放在第一眼，异常事件作为需要时才展开的第二层。', columns: [['当前可用率', '99.2%'], ['恢复事件', '2 次'], ['最后检查', '08:42']], rows: [['周一 — 周三', '总体稳定'], ['周四', '一次短暂延迟'], ['周五 — 周日', '恢复正常']] },
    ledger: { kicker: '02 / EDITORIAL LEDGER', title: '刊期结算 · 九月', lead: '金额是这张卡的重心；付款前必须能看清资料不足的部分。', columns: [['应结算', '¥8,640.00'], ['资料齐备', '2 / 3'], ['待补', '1 笔']], rows: [['周予 · 长文', '¥3,200 · 可核对'], ['林禾 · 摄影', '¥2,880 · 可核对'], ['陈川 · 插画', '¥2,560 · 待补资料']] },
    route: { kicker: '03 / JOURNEY', title: '从想法，到交付', lead: '进度状态和下一步紧邻，避免一次跳过多个任务层级。', columns: [['完成步骤', '2 / 4'], ['当前节点', '原型验证'], ['下一节点', '交付']], rows: [['01 · 梳理目标', '完成'], ['02 · 设计方向', '完成'], ['03 · 原型验证', '进行中'], ['04 · 交付上线', '未开始']] },
    atelier: { kicker: '04 / EDITORIAL STORY', title: '器物与日常之光', lead: '让故事的主视觉在静态卡片内自成一幅画，详情只承载真正需要读的内容。', columns: [['展览日期', '11.14 — 02.28'], ['展厅', '二号展厅'], ['形式', '预约参观']], rows: [['第一章', '器物里的晨光'], ['第二章', '木台与手作'], ['第三章', '日常的时间']] },
    dispatch: { kicker: '05 / PRIORITY STACK', title: '今日任务 · 工作队列', lead: '用任务优先级而不是一堆同权重卡片引导处理顺序。', columns: [['待办事项', '6 项'], ['优先处理', '1 项'], ['下一检查', '16:00']], rows: [['核对待反馈问题', '优先 · 需要人工判断'], ['整理知识库变更', '草稿可用'], ['检查更新结果', '16:00']] },
    people: { kicker: '06 / ACCESS MODEL', title: '成员权限 · 示例', lead: '角色说明、当前状态和显式否定权限分别展示。没有权限不能靠空白推断。', columns: [['账号状态', '已启用'], ['内容发布', '允许'], ['账号管理', '不允许']], rows: [['M · 内容维护者', '可发布 · 不可管理'], ['R · 审阅者', '可发布 · 不可管理'], ['L · 管理员', '可发布 · 可管理']] }
  };
  const dialog = document.getElementById('cardDialog');
  const openerSelector = '[data-card]';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let opener = null;
  let animation = null;
  function addTextNode(parent, tag, value, cls) {
    const el = document.createElement(tag);
    el.textContent = value;
    if (cls) el.className = cls;
    parent.append(el);
    return el;
  }
  function draw(key) {
    const card = data[key];
    document.getElementById('panelKicker').textContent = card.kicker;
    document.getElementById('panelTitle').textContent = card.title;
    document.getElementById('panelLead').textContent = card.lead;
    const body = document.getElementById('panelBody');
    body.replaceChildren();
    const stats = addTextNode(body, 'div', '', 'sheet-stats');
    for (const [name, val] of card.columns) {
      const block = addTextNode(stats, 'div', '', 'sheet-stat');
      addTextNode(block, 'span', name);
      addTextNode(block, 'strong', val);
    }
    addTextNode(body, 'h3', '相关信息', 'sheet-subtitle');
    const list = addTextNode(body, 'ul', '', 'sheet-list');
    for (const [name, val] of card.rows) {
      const row = addTextNode(list, 'li', '', 'sheet-list-row');
      addTextNode(row, 'span', name);
      addTextNode(row, 'b', val);
    }
  }
  function expand(trigger) {
    const key = trigger.dataset.card;
    if (!data[key] || dialog.open) return;
    opener = trigger;
    draw(key);
    const origin = trigger.closest('.design-card').getBoundingClientRect();
    dialog.showModal();
    const target = dialog.getBoundingClientRect();
    // FLIP-style position/scale from the trigger's card into a focused sheet.
    if (!prefersReducedMotion.matches && target.width > 0 && target.height > 0) {
      const dx = origin.left + origin.width / 2 - (target.left + target.width / 2);
      const dy = origin.top + origin.height / 2 - (target.top + target.height / 2);
      const scale = Math.max(.35, Math.min(1, origin.width / target.width));
      animation = dialog.animate([
        { transform: `translate(${dx}px, ${dy}px) scale(${scale})`, opacity: .65, borderRadius: '22px' },
        { transform: 'translate(0, 0) scale(1)', opacity: 1, borderRadius: '14px' }
      ], { duration: 330, easing: 'cubic-bezier(.2,.78,.2,1)', fill: 'none' });
      animation.finished.catch(() => {});
    }
    document.getElementById('closePanel').focus({ preventScroll: true });
  }
  document.querySelectorAll(openerSelector).forEach(btn => btn.addEventListener('click', () => expand(btn)));
  document.getElementById('closePanel').addEventListener('click', () => dialog.close());
  document.getElementById('donePanel').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    if (animation) { animation.cancel(); animation = null; }
    if (opener?.isConnected && !opener.disabled) opener.focus({ preventScroll: true });
  });
  // Disallow outside-click accidental closes: explicit close/Escape only.
})();
