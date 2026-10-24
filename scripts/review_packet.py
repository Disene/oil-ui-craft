#!/usr/bin/env python3
"""Prepare a local, filename-blinded screenshot packet; validate evidence-linked review JSON.

No model is called. No upload, score generation, or claim of reviewer independence occurs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import struct
import sys
import zlib

PNG = b'\x89PNG\r\n\x1a\n'
META = {b'tEXt', b'zTXt', b'iTXt', b'eXIf', b'tIME'}


def clean_png(data: bytes) -> bytes:
    """Retain image data but remove textual/EXIF metadata; validate all input CRCs."""
    if not data.startswith(PNG) or len(data) > 20 * 1024 * 1024:
        raise ValueError('A PNG screenshot of at most 20 MiB is required')
    output = bytearray(PNG); cursor = 8; first = True; ended = False
    while cursor + 12 <= len(data):
        length = struct.unpack('>I', data[cursor:cursor+4])[0]
        kind = data[cursor+4:cursor+8]; stop = cursor + 12 + length
        if stop > len(data) or (first and kind != b'IHDR'):
            raise ValueError('Invalid PNG chunk')
        payload = data[cursor+8:cursor+8+length]
        crc = struct.unpack('>I', data[cursor+8+length:stop])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError('PNG CRC mismatch')
        if kind not in META:
            output.extend(data[cursor:stop])
        cursor = stop; first = False
        if kind == b'IEND':
            ended = True; break
    if not ended or cursor != len(data):
        raise ValueError('Incomplete PNG or unexpected trailing data')
    return bytes(output)


def prepare(images: list[Path], task: str, out: Path) -> dict:
    if not task.strip() or not 1 <= len(images) <= 16:
        raise ValueError('Provide a task and 1–16 screenshots')
    if out.exists():
        raise ValueError('Output already exists; choose a fresh task evidence directory')
    entries = []
    for image in images:
        if image.is_symlink() or not image.is_file():
            raise ValueError('Screenshots must be regular files, not symlinks')
        original = image.read_bytes()
        entries.append((image, clean_png(original), hashlib.sha256(original).hexdigest()))
    random.SystemRandom().shuffle(entries)
    reviewer = out / 'reviewer'
    reviewer.mkdir(parents=True)
    evidence = []; mapping = []
    for index, (path, clean, original_hash) in enumerate(entries, 1):
        key = f'E{index:02d}'; name = key + '.png'
        (reviewer / name).write_bytes(clean)
        evidence.append({'id': key, 'file': name, 'sha256': hashlib.sha256(clean).hexdigest()})
        mapping.append({'id': key, 'source': str(path.resolve()), 'source_sha256': original_hash})
    manifest = {'format': 'craft-review/1', 'task': task, 'evidence': evidence,
                'note': 'Image filenames and metadata are hidden, not the visual content itself.'}
    (reviewer / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'author-map.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')
    prompt = '''# 独立画面审阅\n\n只向新的评审上下文提供本 reviewer 目录，不提供 author-map.json、作者过程或预期评分。\n\n读取 manifest.json 中的任务与实际 PNG。先描述可观察事实，再按影响列问题；每个问题引用 evidence ID。不要猜业务规则、不要为了达到 9 分修改结论。\n\n输出 JSON：round（1–3）、review_type（self / independent）、issues（数组）。每项包含 severity（major / minor / info）、finding、evidence（ID 数组）；交互问题补原始操作路径，修复后沿同一路径复核。可附 0–10 的主观 score，但它不是业务通过证书。\n\n此工具没有调用评审者。review_type 只是提交者声明，不证明实际独立性。视觉截图无法证明交互已经执行。\n'''
    (reviewer / 'REVIEW.md').write_text(prompt, encoding='utf-8')
    return manifest


def validate(manifest_path: Path, report: dict) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('format') != 'craft-review/1':
        raise ValueError('Unsupported packet format')
    evidence = manifest.get('evidence', [])
    if not evidence:
        raise ValueError('No evidence in packet')
    ids = set()
    for item in evidence:
        name = item.get('file', '')
        if Path(name).name != name or not name.endswith('.png'):
            raise ValueError('Unsafe evidence file')
        path = manifest_path.parent / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != item.get('sha256'):
            raise ValueError('Evidence bytes changed')
        ids.add(item['id'])
    if not isinstance(report, dict) or type(report.get('round')) is not int or not 1 <= report['round'] <= 3:
        raise ValueError('Review round must be an integer from 1 to 3')
    if report.get('review_type') not in {'self', 'independent'}:
        raise ValueError('Declare self or independent review')
    issues = report.get('issues')
    if not isinstance(issues, list):
        raise ValueError('issues must be an array')
    for item in issues:
        if not isinstance(item, dict) or item.get('severity') not in {'major', 'minor', 'info'}:
            raise ValueError('Invalid issue severity')
        if not isinstance(item.get('finding'), str) or not item['finding'].strip():
            raise ValueError('Each issue needs an observed finding')
        refs = item.get('evidence')
        if not isinstance(refs, list) or not refs or any(not isinstance(i,str) or i not in ids for i in refs):
            raise ValueError('Each issue must cite existing evidence IDs')
    score = report.get('score')
    if score is not None and (type(score) not in (int,float) or not 0 <= score <= 10):
        raise ValueError('Optional subjective score must be between 0 and 10')
    return {'format_valid': True, 'evidence_integrity': 'matched', 'issues': len(issues),
            'independence': 'not_verified_by_tool', 'business_acceptance': 'not_performed'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('prepare'); p.add_argument('--image', type=Path, action='append', required=True)
    p.add_argument('--task', required=True); p.add_argument('--out', type=Path, required=True)
    v = commands.add_parser('validate'); v.add_argument('--manifest', type=Path, required=True); v.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.image, args.task, args.out) if args.command == 'prepare' else validate(args.manifest, json.loads(args.report.read_text(encoding='utf-8')))
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'review-packet: {exc}', file=sys.stderr); return 1

if __name__ == '__main__':
    raise SystemExit(main())
