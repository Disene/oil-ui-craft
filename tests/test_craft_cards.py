"""Synthetic local-browser contract for six independent card layouts."""
from __future__ import annotations
from pathlib import Path
import os
import unittest
import shutil
import tempfile
try:
    from playwright.sync_api import sync_playwright, expect
except ImportError:
    sync_playwright = None
    expect = None

ROOT=Path(__file__).resolve().parents[1]/'examples'/'craft-cards'
ART=Path(os.getenv('CRAFT_CARD_ARTIFACTS', str(Path(tempfile.gettempdir()) / 'oil-craft-cards')))
ART.mkdir(parents=True, exist_ok=True)

def inline_fixture():
    """Run the complete authored HTML/CSS/JS in memory when localhost is blocked."""
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    css=(ROOT/'cards.css').read_text(encoding='utf-8')
    js=(ROOT/'cards.js').read_text(encoding='utf-8')
    assert '<link rel="stylesheet" href="cards.css">' in html
    assert '<script src="cards.js" defer></script>' in html
    html=html.replace('<link rel="stylesheet" href="cards.css">', '<style>'+css+'</style>')
    return html.replace('<script src="cards.js" defer></script>','').replace('</body>', '<script>'+js+'</script></body>')

class Cards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sync_playwright is None:
            raise unittest.SkipTest('optional Playwright not installed')
        cls.html=inline_fixture()
        cls.pw=sync_playwright().start()
        browser_path=os.getenv('CHROME_PATH') or next((path for name in ('chromium','chromium-browser','google-chrome','microsoft-edge') if (path:=shutil.which(name))), None)
        if not browser_path:
            cls.pw.stop()
            raise unittest.SkipTest('Chromium/Chrome/Edge not installed')
        try:
            cls.browser=cls.pw.chromium.launch(headless=True,executable_path=browser_path)
        except Exception as exc:
            cls.pw.stop()
            raise unittest.SkipTest(f'Browser unavailable: {type(exc).__name__}')

    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop()

    def page(self,width=1440,height=900, reduced_motion=None):
        p=self.browser.new_page(viewport={'width':width,'height':height},reduced_motion=reduced_motion or 'no-preference')
        p.set_content(self.html,wait_until='load',timeout=15000)
        return p

    def test_six_distinct_cards_and_no_unintended_requests(self):
        p=self.page()
        messages=[]
        p.on('pageerror',lambda e:messages.append(str(e)))
        expect(p.locator('article.design-card')).to_have_count(6)
        assert p.locator('[data-card]').count()==6
        assert p.locator('article.design-card').evaluate_all("els=>new Set(els.map(x=>x.className.split(' ')[1])).size")==6
        self.assertFalse(messages)
        p.close()

    def test_modal_each_card_keyboard_close_focus_and_no_stale_data(self):
        p=self.page(1440,900)
        problems=[]
        p.on('pageerror',lambda e:problems.append(str(e)))
        for name in ['signal','ledger','route','atelier','dispatch','people']:
            source=p.locator(f'button[data-card="{name}"]')
            source.click()
            expect(p.locator('#cardDialog')).to_be_visible()
            expect(p.locator('#closePanel')).to_be_focused()
            expect(p.locator('.sheet-stat')).to_have_count(3)
            assert p.locator('#panelTitle').inner_text().strip()
            p.keyboard.press('Tab')
            # Native modal maintains focus inside dialog
            assert p.evaluate("document.activeElement.closest('dialog')!==null")
            p.keyboard.press('Escape')
            expect(p.locator('#cardDialog')).to_be_hidden()
            expect(source).to_be_focused()
        self.assertFalse(problems,problems)
        p.close()

    def test_mobile_and_desktop_layout_and_screenshots(self):
        for width,height in [(1440,900),(390,844),(768,900),(320,700)]:
            p=self.page(width,height)
            overflow=p.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-window.innerWidth")
            self.assertLessEqual(overflow,3,(width,overflow))
            boxes=p.locator('article.design-card').evaluate_all('els=>els.map(e=>({x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}))')
            self.assertGreater(min(b['width'] for b in boxes), min(310,width-35))
            self.assertGreater(min(b['height'] for b in boxes),320)
            p.screenshot(path=str(ART/f'cards-{width}.png'),full_page=True,animations='disabled')
            p.locator('button[data-card="atelier"]').click()
            expect(p.locator('#cardDialog')).to_be_visible()
            assert p.evaluate("document.activeElement.closest('dialog')!==null")
            p.screenshot(path=str(ART/f'expanded-{width}.png'),animations='disabled')
            p.close()

    def test_css_200_percent_zoom(self):
        for width in (390, 1440):
            p=self.page(width,844)
            p.evaluate('document.body.style.zoom="200%"')
            overflow=p.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-window.innerWidth")
            self.assertLessEqual(overflow,3,(width,overflow))
            p.close()

    def test_reduced_motion_and_modal_has_no_api_writes(self):
        p=self.page(390,844,'reduce')
        outgoing=[]
        p.on('request',lambda req:outgoing.append((req.method,req.url)))
        p.locator('button[data-card="people"]').click()
        expect(p.locator('#cardDialog')).to_be_visible()
        self.assertEqual(p.locator('#cardDialog').evaluate('el=>el.getAnimations().length'),0)
        self.assertFalse([x for x in outgoing if x[0]!='GET'],outgoing)
        p.locator('#donePanel').click()
        expect(p.locator('button[data-card="people"]')).to_be_focused()
        p.close()

if __name__=='__main__':unittest.main(verbosity=2)
