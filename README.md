English · [中文](README.zh-CN.md)

# Oil UI Craft

An MIT-licensed fork of [Oil UI](https://github.com/oil-oil/oil-ui), preserving upstream design exploration, comparison, screenshot/recording and review workflows. **Not official Oil UI Pro**, with no private Pro source or claim of one-to-one equivalence.

Upstream version `0.34.5` with independent extension `craft-ux.5`. Installation uses the merged `main` branch.

The update at `b706300` adds a shorter design workflow, improved screenshot diagnostics and image-request recovery guidance. Craft examples and Fork update protection remain available. Screenshot warnings use 3:1 for normal text and 2.5:1 for large text, including 3:1 for small text and placeholders. The effect of the upstream 4.5:1 exception was measured on the workbench and component gallery. [Validation](docs/VALIDATION.md#2026-11-21-上游-0345-同步候选)

## Available work

- Task-scoped existing-product, workbench, interaction and bounded review guidance.
- **19 original patterns**: six spatial card compositions and thirteen interactive studies with real local state changes.
- SVG flow, Canvas dot field and WebGL gradient implementation, including pause, reduced motion and static CSS fallback. Prior browser verification covered WebGL rendering, context recovery and CSS fallback; this synchronization reuses that evidence.
- A playable memory game with ready, playing, mismatch, pause, win, loss and restart states.
- Optional filename/metadata-blinded screenshot packets and evidence-linked review validation. The tool **does not call a model or certify reviewer independence**.
- Optional browser journeys, conservative evidence summaries and a guard against replacing this fork with an upstream in-place update.

[Example index](examples/index.html) · [Component reference](references/craft-components.md) · [Effects and game](references/craft-effects-games.md) · [Validation](docs/VALIDATION.md)

All demo content is synthetic. No remote assets, model calls, payments or real account writes. Adapt only the relevant pattern to a project's existing design system and business contracts.

## Installation and updates

```sh
npx skills add Disene/oil-ui-craft
```

The Skill remains named `oil-ui`; avoid simultaneously enabling duplicate installations. Review upstream changes inside this fork before updating installed copies. The retained updater refuses the official CLI's `--update` when fork metadata is present.

## Verification

Python 3.10+; Playwright and an approved Chromium installation are optional test dependencies. Do not bypass browser or organizational policies.

```sh
python -m unittest discover -s tests -p 'test_craft*.py' -v
python -m unittest discover -s tests -p 'test_fork_update.py' -v
python -m unittest discover -s tests -p 'test_review_packet.py' -v
```

Historical evidence includes **23 focused tests** and the later **7/7 workbench tests** with overlapping coverage, plus HTTP/WebGL and independent visual checks at their recorded commits. The 0.34.5 sync verifies the affected screenshot and image generation tools. [Validation](docs/VALIDATION.md#2026-11-21-上游-0345-同步候选)

## Attribution

The upstream engine and methods remain credited to [oil-oil/oil-ui](https://github.com/oil-oil/oil-ui). Public capability references: [upstream comparison](https://github.com/oil-oil/oil-ui/blob/main/README.zh-CN.md#开源版和-pro) and [official introduction](https://ui.oiloil.org/intro/). New workbench categories, components, effects and game examples are independent implementations, not copies of proprietary Pro assets.

[MIT license](LICENSE); upstream copyright notice is preserved.
