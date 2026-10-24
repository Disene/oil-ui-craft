/* Original local interaction studies. No network requests, payments or persistent writes. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  document.querySelectorAll('[data-period]').forEach(button => button.addEventListener('click', () => {
    const month = button.dataset.period === 'month';
    document.querySelectorAll('[data-period]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    $('trendValue').textContent = month ? '6,280' : '1,432';
    $('trendDelta').textContent = month ? '比上月 +8.1%' : '比上周 +12.4%';
    $('trendCaption').textContent = (month ? '本月 6,280' : '本周 1,432') + ' 次阅读 · 合成数据';
    $('trendLine').setAttribute('d', month ? 'M0 88 L40 75 L80 55 L120 61 L160 33 L200 38 L250 15 L300 4' : 'M0 80 L40 65 L80 70 L120 40 L160 48 L200 25 L250 34 L300 8');
  }));
  $('quotaRange').addEventListener('input', e => {
    const v = Number(e.target.value); $('quotaRing').style.setProperty('--amount', v + '%');
    $('quotaCenter').textContent = v + '%'; $('quotaText').textContent = v + ' / 100 GB';
    $('quotaHint').textContent = v >= 100 ? '容量已满' : v >= 90 ? '即将达到容量上限' : '空间充足';
  });
  let slot = null;
  document.querySelectorAll('[data-slot]').forEach(b => b.addEventListener('click', () => {
    slot = b.dataset.slot; document.querySelectorAll('[data-slot]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    $('book').disabled = false; $('bookingStatus').textContent = '已选择 ' + slot + '，等待确认。';
  }));
  $('book').addEventListener('click', () => { if (slot) $('bookingStatus').textContent = '已确认演示时段 ' + slot + '；未创建真实预约。'; });
  function price() {
    const n = Number($('seats').value), annual = $('annual').checked, monthly = n * 24 * (annual ? 0.8 : 1);
    $('seatCount').value = String(n); $('price').textContent = '¥' + monthly.toFixed(annual ? 2 : 0);
    $('priceDescription').textContent = annual ? n + ' 席 · 年度合计 ¥' + (monthly * 12).toFixed(2) : n + ' 席 × ¥24 / 月';
  }
  $('seats').addEventListener('input', price); $('annual').addEventListener('change', price);
  let stage = 0; const stages = ['准备：整理素材与方向', '制作：形成完整封面', '核对：检查内容与尺寸'];
  function task() {
    document.querySelectorAll('[data-stage]').forEach((el, i) => { if (i === stage) el.setAttribute('aria-current', 'step'); else el.removeAttribute('aria-current'); });
    $('taskState').textContent = stages[stage]; $('advance').disabled = stage === 2; $('undo').disabled = stage === 0;
    $('advance').textContent = ['进入制作', '进入核对', '已到核对阶段'][stage];
  }
  $('advance').addEventListener('click', () => { stage = Math.min(2, stage + 1); task(); });
  $('undo').addEventListener('click', () => { stage = Math.max(0, stage - 1); task(); });
  function drawer(open) { $('inlineDrawer').hidden = !open; $('drawerToggle').setAttribute('aria-expanded', String(open)); $('drawerToggle').textContent = open ? '收起使用条件' : '展开使用条件'; }
  $('drawerToggle').addEventListener('click', () => drawer($('inlineDrawer').hidden));
  $('drawerClose').addEventListener('click', () => { drawer(false); $('drawerToggle').focus(); });
  $('compareRange').addEventListener('input', e => { $('compareFront').style.clipPath = `inset(0 ${100 - Number(e.target.value)}% 0 0)`; $('compareValue').value = e.target.value + '%'; });
  let art = 0; const titles = ['山与圆', '窗边的光', '不对称的静物'];
  function showArt(delta) { art = (art + delta + 3) % 3; $('artwork').dataset.art = String(art); $('artwork').setAttribute('aria-label', '合成几何作品：' + titles[art]); $('artTitle').textContent = titles[art]; $('artIndex').textContent = '0' + (art + 1) + ' / 03'; }
  $('artPrev').addEventListener('click', () => showArt(-1)); $('artNext').addEventListener('click', () => showArt(1));
  $('csvFile').addEventListener('change', () => {
    const f = $('csvFile').files[0]; $('clearFile').disabled = !f;
    const valid = f && /\.csv$/i.test(f.name) && f.size <= 1024 * 1024;
    $('csvFile').setAttribute('aria-invalid', String(!!f && !valid));
    $('fileStatus').textContent = !f ? '尚未选择文件' : valid ? '已选择 ' + f.name + ' · ' + f.size + ' 字节；未上传。' : '请选择不超过 1 MB 的 CSV 文件。';
  });
  $('clearFile').addEventListener('click', () => { $('csvFile').value = ''; $('csvFile').removeAttribute('aria-invalid'); $('clearFile').disabled = true; $('fileStatus').textContent = '选择已清除；未上传任何文件。'; $('csvFile').focus(); });
  const checks = [...document.querySelectorAll('[data-ready]')];
  checks.forEach(c => c.addEventListener('change', () => { const n = checks.filter(x => x.checked).length; $('readiness').value = n; $('checkProgress').textContent = n + ' / 3'; $('confirmReady').disabled = n !== 3; $('readyStatus').textContent = n === 3 ? '全部勾选，等待确认。' : '还有 ' + (3 - n) + ' 项待核对 · 不会发布任何内容'; }));
  $('confirmReady').addEventListener('click', () => { if (checks.every(c => c.checked)) $('readyStatus').textContent = '演示核对已完成；没有发布内容。'; });
  const places = ['阅读空间', '制作工坊', '展示长廊']; let matches = [], active = -1, composing = false;
  function closeList() { $('placeList').hidden = true; $('place').setAttribute('aria-expanded', 'false'); $('place').removeAttribute('aria-activedescendant'); active = -1; }
  function setActive(i) { active = i; [...$('placeList').children].forEach((el, n) => el.setAttribute('aria-selected', String(n === i))); if (i >= 0) $('place').setAttribute('aria-activedescendant', 'place-option-' + i); }
  function choose(i) { if (!matches[i]) return; $('place').value = matches[i]; $('placeStatus').textContent = '已选择：' + matches[i]; closeList(); }
  function findPlaces() {
    matches = places.filter(x => x.includes($('place').value.trim())); $('placeList').replaceChildren(); active = -1;
    $('place').removeAttribute('aria-activedescendant');
    matches.forEach((name, i) => { const li = document.createElement('li'); li.role = 'option'; li.id = 'place-option-' + i; li.textContent = name; li.setAttribute('aria-selected', 'false'); li.addEventListener('pointerdown', e => e.preventDefault()); li.addEventListener('click', () => choose(i)); $('placeList').append(li); });
    $('placeList').hidden = matches.length === 0; $('place').setAttribute('aria-expanded', String(matches.length > 0));
    $('placeStatus').textContent = matches.length ? '找到 ' + matches.length + ' 个候选。' : '没有匹配空间。';
  }
  $('place').addEventListener('input', () => { if (!composing) findPlaces(); });
  $('place').addEventListener('focus', findPlaces); $('place').addEventListener('blur', closeList);
  $('place').addEventListener('compositionstart', () => { composing = true; });
  $('place').addEventListener('compositionend', () => { composing = false; findPlaces(); });
  $('place').addEventListener('keydown', e => {
    if (composing || e.isComposing || e.keyCode === 229) return;
    if (e.key === 'Escape') { e.preventDefault(); closeList(); return; }
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); if ($('placeList').hidden) findPlaces(); if (matches.length) setActive((active + (e.key === 'ArrowDown' ? 1 : -1) + matches.length) % matches.length); }
    if (e.key === 'Enter' && !$('placeList').hidden && active >= 0) { e.preventDefault(); choose(active); }
  });
  let saved = { digest: true, notification: false };
  function preferences() { const dirty = $('digest').checked !== saved.digest || $('notification').checked !== saved.notification; $('savePreferences').disabled = !dirty; $('resetPreferences').disabled = !dirty; $('preferenceStatus').textContent = dirty ? '有未保存的更改' : '未修改 · 仅限本演示会话'; }
  ['digest', 'notification'].forEach(id => $(id).addEventListener('change', preferences));
  $('savePreferences').addEventListener('click', () => { if ($('failSave').checked) { $('failSave').checked = false; $('preferenceStatus').textContent = '模拟保存失败：更改已保留，可以重试或还原。'; return; } saved = { digest: $('digest').checked, notification: $('notification').checked }; preferences(); $('preferenceStatus').textContent = '已保存在此演示会话；刷新后重置。'; });
  $('resetPreferences').addEventListener('click', () => { $('digest').checked = saved.digest; $('notification').checked = saved.notification; preferences(); });
})();
