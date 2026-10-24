"""Focused real-browser checks for the independently authored adaptive-workspace example."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ux_journey


class WorkspaceFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = ROOT / "examples" / "adaptive-workspace.html"
        if not cls.fixture.exists():
            raise AssertionError("Example HTML not found")

    def test_fixture_contains_visible_labels(self):
        content = self.fixture.read_text(encoding="utf-8")
        for mark in ('<label for="query">', '<label for="state">', 'id="backList"', 'id="bulkTitle"', 'prefers-reduced-motion'):
            self.assertIn(mark, content)
        self.assertIn("不执行账号修改", content)
        self.assertNotIn("fetch(", content)

    def assert_journey(self, viewport, steps):
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                browser, _ = ux_journey.launch(pw, None)
                browser.close()
        except Exception as exc:
            self.skipTest("Optional Playwright Chromium unavailable: " + type(exc).__name__)
        with tempfile.TemporaryDirectory(prefix="oil-craft-workspace-") as temp:
            report = ux_journey.run({"name": "workbench", "viewport": viewport, "steps": [
                {"action": "loadHtml", "file": str(self.fixture)}, *steps,
            ]}, Path(temp))
            self.assertEqual(report["execution_status"], "pass", report)
            self.assertEqual(report["status"], "pass", report)
            self.assertFalse(report["browser_errors"])

    def test_content_width_at_css_zoom(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest('Optional Playwright not installed')
        with sync_playwright() as pw:
            browser, _ = ux_journey.launch(pw, None)
            try:
                for width in (320, 390, 768, 1024, 1440):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(self.fixture.read_text(encoding="utf-8"))
                    for zoom in ("100%", "200%"):
                        page.evaluate("z => document.body.style.zoom = z", zoom)
                        overflow = page.evaluate("Math.max(document.body.scrollWidth,document.documentElement.scrollWidth)-innerWidth")
                        self.assertLessEqual(overflow, 3, (width, zoom, overflow))
                    page.close()
            finally:
                browser.close()

    def test_mobile_batch_entry_and_focus(self):
        self.assert_journey("390x844", [
            {"action": "expectHidden", "target": "#selectedBar"},
            {"action": "check", "target": 'input[data-select="content-editor"]'},
            {"action": "expectText", "target": "#selectedCount", "value": "已选 1 个"},
            {"action": "click", "target": "#jump"},
            {"action": "expectVisible", "target": "#bulk"},
            {"action": "expectFocused", "target": "#bulkTitle"},
            {"action": "click", "target": "#cancelBatch"},
            {"action": "expectHidden", "target": "#bulk"},
            {"action": "expectFocused", "target": "#jump"},
            {"action": "expectNoDocumentOverflow"},
        ])

    def test_mobile_detail_return(self):
        self.assert_journey("390x844", [
            {"action": "click", "target": 'button[data-open="content-reviewer"]'},
            {"action": "expectVisible", "target": "#detail"},
            {"action": "expectFocused", "target": "#detailTitle"},
            {"action": "expectText", "target": "#permissionInfo", "value": "可发布"},
            {"action": "click", "target": "#backList"},
            {"action": "expectFocused", "target": 'button[data-open="content-reviewer"]'},
            {"action": "expectNoDocumentOverflow"},
        ])

    def test_desktop_compare_without_overflow(self):
        self.assert_journey("1440x900", [
            {"action": "expectVisible", "target": ".headingrow"},
            {"action": "click", "target": 'button[data-open="pilot-admin"]'},
            {"action": "expectText", "target": "#permissionInfo", "value": "可管理"},
            {"action": "click", "target": '[data-demo="导入"]'},
            {"action": "expectVisible", "target": "#infoDialog"},
            {"action": "expectFocused", "target": "#closeDialog"},
            {"action": "press", "key": "Escape"},
            {"action": "expectHidden", "target": "#infoDialog"},
            {"action": "expectFocused", "target": '[data-demo="导入"]'},
            {"action": "expectNoDocumentOverflow"},
        ])


    def test_account_name_hover_is_not_underline(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser, _ = ux_journey.launch(pw, None)
            try:
                for motion in ("no-preference", "reduce"):
                    page = browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion=motion)
                    page.set_content(self.fixture.read_text(encoding="utf-8"))
                    button = page.locator('button[data-open="content-editor"]')
                    original = button.evaluate('(el) => getComputedStyle(el).color')
                    button.hover()
                    # Wait for the cosmetic transition to settle, not for an asynchronous business state.
                    page.wait_for_timeout(210 if motion == "no-preference" else 15)
                    self.assertEqual(button.evaluate('(el) => getComputedStyle(el).textDecorationLine'), 'none')
                    self.assertNotEqual(button.evaluate('(el) => getComputedStyle(el).color'), original)
                    row = page.locator('.accountrow').first
                    self.assertNotEqual(row.evaluate('(el) => getComputedStyle(el).backgroundColor'), 'rgba(0, 0, 0, 0)')
                    page.close()
            finally:
                browser.close()

    def test_interaction_motion_and_reduced_motion(self):
        from playwright.sync_api import sync_playwright, expect
        with sync_playwright() as pw:
            browser, _ = ux_journey.launch(pw, None)
            try:
                for motion in ("no-preference", "reduce"):
                    page = browser.new_page(viewport={"width": 390, "height": 844}, reduced_motion=motion)
                    page.set_content(self.fixture.read_text(encoding="utf-8"))
                    page.evaluate('''() => {
                      window.__detailMotionCalls = 0;
                      const original = Element.prototype.animate;
                      Element.prototype.animate = function(...args) {
                        if (this.id === 'detail') window.__detailMotionCalls++;
                        return original.apply(this, args);
                      };
                    }''')
                    page.locator('button[data-open="content-reviewer"]').click()
                    expect(page.locator('#detailTitle')).to_be_focused()
                    self.assertEqual(page.evaluate('window.__detailMotionCalls'), 1 if motion == 'no-preference' else 0)
                    page.locator('#backList').click()
                    expect(page.locator('button[data-open="content-reviewer"]')).to_be_focused()
                    page.locator('input[data-select="content-editor"]').check()
                    selected_animation = page.locator('#selectedBar').evaluate('(el) => getComputedStyle(el).animationName')
                    self.assertEqual(selected_animation, 'craft-selection-in' if motion == 'no-preference' else 'none')
                    page.locator('[data-demo="导入"]').click()
                    expect(page.locator('#closeDialog')).to_be_focused()
                    dialog_animation = page.locator('#infoDialog').evaluate('(el) => getComputedStyle(el).animationName')
                    self.assertEqual(dialog_animation, 'craft-dialog-in' if motion == 'no-preference' else 'none')
                    page.keyboard.press('Escape')
                    expect(page.locator('[data-demo="导入"]')).to_be_focused()
                    page.close()
            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
