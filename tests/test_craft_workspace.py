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


if __name__ == "__main__":
    unittest.main()
