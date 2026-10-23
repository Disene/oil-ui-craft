#!/usr/bin/env python3
"""Optional Playwright journey assertions for Oil UI. No production writes by default."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import sys
import time
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

ACTIONS = {
    "loadHtml", "goto", "click", "fill", "press", "selectOption", "check", "uncheck",
    "expectVisible", "expectHidden", "expectText", "expectValue", "expectCount",
    "expectAttribute", "expectUrl", "expectFocused", "expectNoDocumentOverflow", "screenshot",
}


def clean_url(url: str) -> str:
    """Avoid leaking common credentials in query strings and fragments."""
    try:
        p = urlsplit(url)
        query = [(k, "REDACTED" if re.search(r"token|secret|key|password|session|auth|code", k, re.I) else v)
                 for k, v in parse_qsl(p.query, keep_blank_values=True)]
        return urlunsplit((p.scheme, p.netloc, p.path, urlencode(query), ""))
    except ValueError:
        return "[invalid URL]"


def validate(spec: dict) -> tuple[dict, list[dict]]:
    if not isinstance(spec, dict):
        raise ValueError("spec must be an object")
    steps = spec.get("steps")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 100:
        raise ValueError("spec.steps must contain 1–100 steps")
    for i, step in enumerate(steps, 1):
        if not isinstance(step, dict) or step.get("action") not in ACTIONS:
            raise ValueError(f"step {i}: unsupported action")
        if step["action"] in {"click", "fill", "selectOption", "check", "uncheck", "expectVisible",
                              "expectHidden", "expectText", "expectValue", "expectCount", "expectAttribute",
                              "expectFocused"} and not isinstance(step.get("target"), str):
            raise ValueError(f"step {i}: target selector required")
    vp = spec.get("viewport", "1280x800")
    if not isinstance(vp, str) or not re.fullmatch(r"\d{3,4}x\d{3,4}", vp):
        raise ValueError("viewport must be WIDTHxHEIGHT, e.g. 390x844")
    width, height = map(int, vp.split("x"))
    if not (240 <= width <= 4096 and 240 <= height <= 4096):
        raise ValueError("viewport out of bounds (240–4096)")
    return {"width": width, "height": height}, steps


def launch(playwright, browser_path: str | None):
    if browser_path:
        return playwright.chromium.launch(headless=True, executable_path=browser_path), "configured"
    try:
        return playwright.chromium.launch(headless=True), "playwright-chromium"
    except Exception as original:
        executable = next((x for name in ("chromium", "chromium-browser", "google-chrome", "microsoft-edge")
                           if (x := shutil.which(name))), None)
        if not executable:
            raise RuntimeError("Chromium unavailable; install Playwright Chromium or pass --browser-path") from original
        return playwright.chromium.launch(headless=True, executable_path=executable), "system-browser"


def perform(page, step: dict, index: int, output: Path, base_url: str) -> str | None:
    from playwright.sync_api import expect

    action = step["action"]
    target = step.get("target")
    locator = page.locator(target) if target else None
    timeout = min(30000, max(200, int(step.get("timeout", 6500))))
    if action == "loadHtml":
        path = Path(step["file"])
        if path.stat().st_size > 3 * 1024 * 1024:
            raise ValueError("HTML fixture larger than 3 MiB")
        page.set_content(path.read_text(encoding="utf-8"), wait_until="domcontentloaded", timeout=timeout)
    elif action == "goto":
        address = step.get("url", step.get("path"))
        if not isinstance(address, str) or not address:
            raise ValueError("goto requires url or path")
        address = urljoin(base_url, address)
        if urlsplit(address).scheme not in {"http", "https"}:
            raise ValueError("goto supports http(s) only; use loadHtml for isolated fixtures")
        response = page.goto(address, wait_until="domcontentloaded", timeout=timeout)
        if response and response.status >= 400:
            raise AssertionError(f"Navigation HTTP {response.status}")
    elif action == "click":
        locator.click(timeout=timeout)
    elif action == "fill":
        locator.fill(str(step.get("value", "")), timeout=timeout)
    elif action == "press":
        key = str(step["key"])
        (locator if locator else page.keyboard).press(key)
    elif action == "selectOption":
        locator.select_option(str(step["value"]))
    elif action == "check":
        locator.check()
    elif action == "uncheck":
        locator.uncheck()
    elif action == "expectVisible":
        expect(locator.first).to_be_visible(timeout=timeout)
    elif action == "expectHidden":
        expect(locator.first).to_be_hidden(timeout=timeout)
    elif action == "expectText":
        expect(locator).to_contain_text(str(step["value"]), timeout=timeout)
    elif action == "expectValue":
        expect(locator).to_have_value(str(step["value"]), timeout=timeout)
    elif action == "expectCount":
        expect(locator).to_have_count(int(step["value"]), timeout=timeout)
    elif action == "expectAttribute":
        expect(locator).to_have_attribute(str(step["attribute"]), str(step["value"]), timeout=timeout)
    elif action == "expectUrl":
        expect(page).to_have_url(re.compile(re.escape(str(step["value"]))), timeout=timeout)
    elif action == "expectFocused":
        expect(locator).to_be_focused(timeout=timeout)
    elif action == "expectNoDocumentOverflow":
        overflow = page.evaluate("Math.max(document.documentElement.scrollWidth, document.body?.scrollWidth || 0) - window.innerWidth")
        if overflow > int(step.get("tolerance", 4)):
            raise AssertionError(f"Document horizontal overflow: {overflow}px")
    elif action == "screenshot":
        filename = f"step-{index:02d}.png"
        page.screenshot(path=str(output / filename), animations="disabled", full_page=bool(step.get("fullPage", False)))
        return filename
    return None


def run(spec: dict, output: Path, browser_path: str | None = None) -> dict:
    """Browser and accessibility checks need a real browser; missing tools never produce PASS."""
    output.mkdir(parents=True, exist_ok=True)
    result = {"tool": "ux-journey", "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "execution_status": "fail", "status": "fail", "steps": [], "browser_errors": [],
              "visual_review": "not_performed", "business_review": "not_performed"}
    try:
        viewport, steps = validate(spec)
        result.update({"name": spec.get("name", "unnamed"), "viewport": viewport,
                       "base_url": clean_url(spec.get("baseUrl", ""))})
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser, engine = launch(pw, browser_path)
            result["browser"] = engine
            try:
                page = browser.new_page(viewport=viewport)
                # Deliberately do not save full console messages: customer data can appear in logs.
                page.on("pageerror", lambda _: result["browser_errors"].append("uncaught-pageerror"))
                page.on("console", lambda m: result["browser_errors"].append("console-error") if m.type == "error" else None)
                for index, step in enumerate(steps, 1):
                    started = time.monotonic()
                    record = {"index": index, "action": step["action"], "status": "pass"}
                    try:
                        shot = perform(page, step, index, output, spec.get("baseUrl", ""))
                        if shot:
                            record["screenshot"] = shot
                    except Exception as exc:
                        record.update({"status": "fail", "reason": f"{type(exc).__name__} during {step['action']}"})
                        try:
                            filename = f"failed-step-{index:02d}.png"
                            page.screenshot(path=str(output / filename), animations="disabled")
                            record["screenshot"] = filename
                        except Exception:
                            pass
                    record["duration_ms"] = round((time.monotonic() - started) * 1000)
                    record["url"] = clean_url(page.url)
                    result["steps"].append(record)
                    if record["status"] != "pass":
                        break
                result["execution_status"] = "pass" if len(result["steps"]) == len(steps) and all(
                    s["status"] == "pass" for s in result["steps"]) else "fail"
                result["status"] = "fail" if result["execution_status"] != "pass" else (
                    "attention" if result["browser_errors"] else "pass")
            finally:
                browser.close()
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: browser or specification failure"
    (output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Optional real-browser UI journey checks (requires Playwright)")
    parser.add_argument("--spec", required=True, help="JSON with viewport, baseUrl and steps")
    parser.add_argument("--out", default="artifacts/ux-journey")
    parser.add_argument("--browser-path")
    args = parser.parse_args()
    try:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        parser.error(f"cannot read spec: {exc}")
    result = run(spec, Path(args.out).resolve(), args.browser_path)
    print(f"ux-journey: {result['status']} / execution={result['execution_status']} / {Path(args.out) / 'result.json'}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
