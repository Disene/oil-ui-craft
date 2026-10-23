"""Full static example browser tests. Memory loading is explicit; never claims HTTP validation."""
from pathlib import Path
import json
import os
import re
import shutil
import unittest
try:
    from playwright.sync_api import sync_playwright, expect
except ImportError:
    sync_playwright = expect = None

ROOT = Path(__file__).resolve().parents[1]
ART = Path(os.environ.get('CRAFT_ARTIFACTS', str(ROOT / 'artifacts' / 'extended')))


def inline(folder: str) -> str:
    path = ROOT / 'examples' / folder
    html = (path / 'index.html').read_text(encoding='utf-8')
    def css(m):
        return '<style>' + (path / m[1]).read_text(encoding='utf-8') + '</style>'
    scripts = []
    def js(m):
        scripts.append((path / m[1]).read_text(encoding='utf-8'))
        return ''
    html = re.sub(r'<link rel="stylesheet" href="([^"/:]+)">', css, html)
    html = re.sub(r'<script src="([^"/:]+)" defer></script>', js, html)
    return html.replace('</body>', '\n<script>' + '\n'.join(scripts) + '</script></body>')


class ExtendedExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sync_playwright is None:
            raise unittest.SkipTest('Optional Playwright not installed; browser tests not performed')
        cls.pw = sync_playwright().start()
        path = os.environ.get('CHROME_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
        if not path:
            cls.pw.stop(); raise unittest.SkipTest('No installed Chromium; no browser tests performed')
        cls.browser = cls.pw.chromium.launch(executable_path=path, headless=True)
        ART.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close(); cls.pw.stop()

    def setUp(self):
        self.pages = []
        self.errors = []
        self.requests = []

    def tearDown(self):
        for p in self.pages:
            p.close()
        self.assertFalse(self.errors, self.errors)
        self.assertFalse(self.requests, self.requests)

    def page(self, folder='craft-patterns', width=1440, reduced='reduce'):
        p = self.browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion=reduced)
        p.on('pageerror', lambda e: self.errors.append(str(e)))
        p.on('request', lambda r: self.requests.append((r.method, r.url)))
        self.pages.append(p)
        p.set_content(inline(folder), wait_until='load')
        return p

    def test_thirteen_patterns_and_all_layouts(self):
        for width in (320, 390, 768, 1440):
            p = self.page(width=width)
            expect(p.locator('[data-pattern]')).to_have_count(13)
            for zoom in ('100%', '200%'):
                p.evaluate('z => document.body.style.zoom=z', zoom)
                value = p.evaluate('Math.max(document.body.scrollWidth,document.documentElement.scrollWidth)-innerWidth')
                self.assertLessEqual(value, 3, (width, zoom, value))
            p.evaluate('document.body.style.zoom="100%"')
            p.screenshot(path=str(ART / f'patterns-{width}.png'), full_page=True, animations='disabled')

    def test_metrics_quota_and_calculator(self):
        p = self.page()
        p.locator('[data-period=month]').click()
        expect(p.locator('#trendValue')).to_have_text('6,280')
        p.locator('#quotaRange').fill('100')
        expect(p.locator('#quotaHint')).to_have_text('容量已满')
        p.locator('#seats').fill('20'); p.locator('#annual').check()
        expect(p.locator('#price')).to_have_text('¥384.00')
        expect(p.locator('#priceDescription')).to_contain_text('4608.00')

    def test_booking_task_undo_and_inline_drawer(self):
        p = self.page(width=390)
        expect(p.locator('#book')).to_be_disabled()
        p.locator('[data-slot="14:00"]').click(); p.locator('#book').click()
        expect(p.locator('#bookingStatus')).to_contain_text('未创建真实预约')
        p.locator('#advance').click(); p.locator('#advance').click()
        expect(p.locator('#advance')).to_be_disabled()
        p.locator('#undo').click(); expect(p.locator('#taskState')).to_contain_text('制作')
        p.locator('#drawerToggle').click(); expect(p.locator('#inlineDrawer')).to_be_visible()
        p.locator('#drawerClose').click(); expect(p.locator('#inlineDrawer')).to_be_hidden()
        expect(p.locator('#drawerToggle')).to_be_focused()

    def test_comparison_carousel_file_validation_and_checklist(self):
        p = self.page()
        p.locator('#compareRange').fill('75'); expect(p.locator('#compareValue')).to_have_text('75%')
        p.locator('#artNext').click(); expect(p.locator('#artTitle')).to_have_text('窗边的光')
        p.locator('#artPrev').click(); expect(p.locator('#artTitle')).to_have_text('山与圆')
        p.locator('#csvFile').set_input_files({'name':'bad.txt','mimeType':'text/plain','buffer':b'test'})
        expect(p.locator('#csvFile')).to_have_attribute('aria-invalid','true')
        p.locator('#csvFile').set_input_files({'name':'demo.csv','mimeType':'text/csv','buffer':b'name\nexample'})
        expect(p.locator('#fileStatus')).to_contain_text('未上传')
        p.locator('#clearFile').click(); expect(p.locator('#csvFile')).to_be_focused()
        for c in p.locator('[data-ready]').all(): c.check()
        p.locator('#confirmReady').click(); expect(p.locator('#readyStatus')).to_contain_text('没有发布内容')
        p.locator('details summary').first.click(); self.assertTrue(p.locator('details').first.evaluate('e=>e.open'))

    def test_combobox_keyboard_composition_and_save_failure(self):
        p = self.page()
        q = p.locator('#place'); q.fill('阅读'); q.press('ArrowDown')
        q.evaluate("e=>{e.dispatchEvent(new CompositionEvent('compositionstart')); e.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',isComposing:true,bubbles:true}));}")
        expect(q).to_have_attribute('aria-expanded','true')
        q.evaluate("e=>e.dispatchEvent(new CompositionEvent('compositionend'))")
        q.press('ArrowDown'); q.press('Enter')
        expect(p.locator('#placeStatus')).to_have_text('已选择：阅读空间')
        p.locator('#notification').check(); p.locator('#failSave').check(); p.locator('#savePreferences').click()
        expect(p.locator('#preferenceStatus')).to_contain_text('失败')
        expect(p.locator('#notification')).to_be_checked(); expect(p.locator('#savePreferences')).to_be_enabled()
        p.locator('#savePreferences').click(); expect(p.locator('#preferenceStatus')).to_contain_text('已保存在此演示会话')
        p.locator('#digest').uncheck(); p.locator('#resetPreferences').click(); expect(p.locator('#digest')).to_be_checked()

    def test_effects_reduced_motion_pause_and_renderer(self):
        p = self.page('craft-effects', reduced='reduce')
        expect(p.locator('body')).to_have_attribute('data-running','false')
        expect(p.locator('#motionToggle')).to_be_disabled()
        renderer = p.locator('#shader').get_attribute('data-renderer')
        self.assertIn(renderer, ('webgl','css-fallback'))
        (ART / 'renderer.json').write_text(json.dumps({'renderer':renderer,'browser':self.browser.version,'transport':'memory'},indent=2))
        p.screenshot(path=str(ART/'effects-1440.png'),full_page=True)
        p.emulate_media(reduced_motion='no-preference')
        expect(p.locator('body')).to_have_attribute('data-running','true')
        before = p.locator('#dots').evaluate('e=>e.toDataURL()')
        p.wait_for_function("old => document.getElementById('dots').toDataURL() !== old", arg=before, timeout=2500)
        p.locator('#motionToggle').click(); expect(p.locator('body')).to_have_attribute('data-running','false')
        stopped = p.locator('#dots').evaluate('e=>e.toDataURL()')
        p.wait_for_timeout(120) # Verify a paused effect does not keep updating the canvas.
        self.assertEqual(p.locator('#dots').evaluate('e=>e.toDataURL()'), stopped)
        if renderer == 'webgl':
            lost = p.locator('#shader').evaluate("e=>{const g=e.getContext('webgl'),ext=g.getExtension('WEBGL_lose_context');if(!ext)return false;ext.loseContext();return true;}")
            if lost: expect(p.locator('#shaderStatus')).to_contain_text('上下文丢失')

    def test_effects_and_game_narrow_layouts(self):
        for folder in ('craft-effects','craft-game'):
            p = self.page(folder, width=320)
            for zoom in ('100%','200%'):
                p.evaluate('z=>document.body.style.zoom=z',zoom)
                self.assertLessEqual(p.evaluate('Math.max(document.body.scrollWidth,document.documentElement.scrollWidth)-innerWidth'),3,(folder,zoom))
            p.evaluate('document.body.style.zoom="100%"')
            p.screenshot(path=str(ART/f'{folder}-320.png'),full_page=True)

    def test_game_start_pause_help_win_restart(self):
        p = self.page('craft-game',width=390)
        expect(p.locator('body')).to_have_attribute('data-state','ready')
        p.locator('#start').click(); expect(p.locator('body')).to_have_attribute('data-state','playing'); expect(p.locator('#start')).to_be_hidden()
        p.locator('#pause').click(); expect(p.locator('body')).to_have_attribute('data-state','paused')
        p.locator('#pause').click(); p.locator('#help').click()
        expect(p.locator('#rules')).to_be_visible(); p.keyboard.press('Escape'); expect(p.locator('#help')).to_be_focused()
        p.locator('#pause').click()
        for pair in range(6):
            for b in p.locator(f'.tile[data-pair="{pair}"]').all(): b.click()
        expect(p.locator('body')).to_have_attribute('data-state','won'); expect(p.locator('#outcome')).to_be_focused()
        p.screenshot(path=str(ART/'game-won-390.png'),full_page=True)
        p.locator('#restart').click(); expect(p.locator('#moves')).to_have_text('0 / 18')
        expect(p.locator('.tile[data-matched=true]')).to_have_count(0)

    def test_game_mismatch_pause_resume_and_loss(self):
        p = self.page('craft-game')
        p.locator('#difficulty').select_option('8'); p.locator('#start').click()
        a=p.locator('[data-pair="0"]').first; b=p.locator('[data-pair="1"]').first
        a.click(); b.click(); p.locator('#pause').click()
        p.wait_for_timeout(650) # Deliberately wait past the mismatch timer to prove it is paused.
        expect(p.locator('.tile[aria-pressed=true]')).to_have_count(2)
        p.locator('#pause').click(); expect(p.locator('.tile[aria-pressed=true]')).to_have_count(0)
        for i in range(7):
            a.click(); b.click()
            if i < 6: expect(a).to_be_enabled()
        expect(p.locator('body')).to_have_attribute('data-state','lost'); expect(p.locator('#outcome')).to_contain_text('步数已用完')

if __name__ == '__main__':
    unittest.main(verbosity=2)
