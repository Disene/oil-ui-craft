#!/usr/bin/env python3
"""Summarize existing Oil UI screenshots and optional journey without a false UX PASS."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


def summarize(shot: object | None, journey: object | None) -> dict:
    if shot is None and journey is None:
        raise ValueError("Provide --shoot and/or --journey")
    findings = []
    failed = []
    evidence = []
    if shot is not None:
        if not isinstance(shot, list) or not shot:
            failed.append("shoot report is empty or is not an array")
        else:
            evidence.append("oil-ui shoot report")
            for index, item in enumerate(shot, 1):
                if not isinstance(item, dict):
                    failed.append(f"shoot[{index}] invalid item")
                    continue
                if not item.get("file") and not item.get("motion"):
                    failed.append(f"shoot[{index}] has no evidence entry")
                if item.get("error") or item.get("status") in {"error", "fail", "failed"}:
                    failed.append(f"shoot[{index}] tool error")
                for key in ("issues", "lint", "warnings"):
                    if item.get(key):
                        findings.append(f"shoot[{index}] {key}: review required")
    if journey is not None:
        if not isinstance(journey, dict):
            failed.append("journey report is not an object")
        else:
            evidence.append("ux-journey result")
            if journey.get("execution_status") != "pass" or journey.get("status") not in {"pass", "attention"}:
                failed.append("journey did not execute cleanly")
            elif journey.get("status") == "attention" or journey.get("browser_errors"):
                findings.append("journey captured browser errors")
            if not journey.get("steps"):
                failed.append("journey did not execute any steps")
    status = "fail" if failed else ("attention" if findings else "no_automated_findings")
    return {"status": status, "execution_status": "fail" if failed else "pass",
            "checked": evidence, "findings": findings, "failures": failed,
            "visual_review": "not_performed", "business_review": "not_performed",
            "note": "No automated findings is NOT a visual, UX or production acceptance result."}


def main() -> int:
    parser = argparse.ArgumentParser(description="Conservative evidence summary, not a UX score")
    parser.add_argument("--shoot", help="report.json from upstream scripts/shoot.mjs")
    parser.add_argument("--journey", help="result.json from optional ux_journey.py")
    parser.add_argument("--out", default="artifacts/ux-summary.json")
    args = parser.parse_args()
    try:
        if not args.shoot and not args.journey:
            parser.error("provide --shoot and/or --journey")
        shot = json.loads(Path(args.shoot).read_text(encoding="utf-8")) if args.shoot else None
        journey = json.loads(Path(args.journey).read_text(encoding="utf-8")) if args.journey else None
        result = summarize(shot, journey)
    except (ValueError, OSError) as exc:
        print(f"ux-gate: input error: {exc}", file=sys.stderr)
        return 1
    result["created_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ux-gate: {result['status']} / {target}")
    return 0 if result["status"] == "no_automated_findings" else 1


if __name__ == "__main__":
    sys.exit(main())
