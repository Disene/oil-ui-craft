"""Focused positive and negative checks for optional UX extension; no network calls."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ux_gate
import ux_journey


class VerdictTests(unittest.TestCase):
    def test_no_issues_does_not_claim_ux_pass(self):
        result = ux_gate.summarize([{"file": "desktop.png", "issues": [], "lint": []}], None)
        self.assertEqual(result["status"], "no_automated_findings")
        self.assertEqual(result["visual_review"], "not_performed")

    def test_browser_errors_do_not_get_hidden(self):
        j = {"status": "attention", "execution_status": "pass", "browser_errors": ["console-error"], "steps": [{"status": "pass"}]}
        result = ux_gate.summarize([{"file": "capture.png", "issues": []}], j)
        self.assertEqual(result["status"], "attention")

    def test_tool_failure_is_not_pass(self):
        self.assertEqual(ux_gate.summarize([{"file": "x.png", "error": "navigation failed"}], None)["status"], "fail")
        self.assertEqual(ux_gate.summarize([], None)["status"], "fail")
        self.assertEqual(ux_gate.summarize(None, {"status": "pass", "steps": []})["status"], "fail")
        self.assertEqual(ux_gate.summarize([{}], None)["status"], "fail")

    def test_bad_journey_rejected_before_browser(self):
        with self.assertRaises(ValueError):
            ux_journey.validate({"steps": [{"action": "eval", "source": "alert(1)"}]})
        with self.assertRaises(ValueError):
            ux_journey.validate({"viewport": "100x90", "steps": [{"action": "screenshot"}]})

    def test_url_query_credentials_are_masked(self):
        u = ux_journey.clean_url("https://example.test/x?token=foo&x=bar#private")
        self.assertNotIn("foo", u)
        self.assertNotIn("private", u)
        self.assertIn("x=bar", u)


class BrowserTests(unittest.TestCase):
    def setUp(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest("Playwright not installed (optional dependency)")
        try:
            with sync_playwright() as pw:
                browser, _ = ux_journey.launch(pw, None)
                browser.close()
        except Exception as exc:
            self.skipTest(f"browser unavailable: {type(exc).__name__}")

    def test_async_focus_and_overflow(self):
        html = """<!doctype html><meta charset="utf-8"><button id="open">Open</button>
        <dialog id="dlg"><button id="close">Close</button><p id="status">Initial</p></dialog>
        <script>
        document.querySelector('#open').onclick=()=>{
          document.querySelector('#dlg').showModal();
          document.querySelector('#close').focus();
          setTimeout(()=>document.querySelector('#status').textContent='Ready',100);
        };
        document.querySelector('#close').onclick=()=>{
          document.querySelector('#dlg').close();
          document.querySelector('#open').focus();
        };
        </script>"""
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture.html"; fixture.write_text(html, encoding="utf-8")
            spec = {"viewport": "390x844", "steps": [
                {"action": "loadHtml", "file": str(fixture)},
                {"action": "click", "target": "#open"},
                {"action": "expectFocused", "target": "#close"},
                {"action": "expectText", "target": "#status", "value": "Ready"},
                {"action": "expectNoDocumentOverflow"},
                {"action": "click", "target": "#close"},
                {"action": "expectFocused", "target": "#open"},
            ]}
            result = ux_journey.run(spec, Path(tmp) / "pass")
            self.assertEqual(result["status"], "pass", result)

    def test_injected_errors_never_return_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "broken.html"
            fixture.write_text("""<div style="width:1800px">wide</div>
            <script>console.error('secret customer text')</script>""", encoding="utf-8")
            result = ux_journey.run({"viewport": "390x844", "steps": [
                {"action": "loadHtml", "file": str(fixture)},
                {"action": "expectNoDocumentOverflow"},
            ]}, Path(tmp) / "fail")
            self.assertEqual(result["status"], "fail", result)
            self.assertEqual(result["steps"][-1]["status"], "fail")
            saved = (Path(tmp) / "fail" / "result.json").read_text(encoding="utf-8")
            self.assertNotIn("secret customer text", saved)

    def test_console_error_demotes_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "console.html"
            fixture.write_text('<button id="x">Go</button><script>console.error("not logged raw")</script>', encoding="utf-8")
            result = ux_journey.run({"steps": [
                {"action": "loadHtml", "file": str(fixture)},
                {"action": "expectVisible", "target": "#x"},
            ]}, Path(tmp) / "attention")
            self.assertEqual(result["execution_status"], "pass")
            self.assertEqual(result["status"], "attention")
            self.assertNotIn("not logged raw", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
