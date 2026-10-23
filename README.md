English · [中文](README.zh-CN.md)

# Oil UI Craft

An MIT-licensed fork of [Oil UI](https://github.com/oil-oil/oil-ui), preserving upstream design exploration, comparison, screenshot/recording and review workflows. **Not official Oil UI Pro**, with no private Pro source or claim of one-to-one equivalence.

Upstream version: `0.24.2`. Independent extension: `craft-ux.2`. An open PR is not an installed release; normal installation reads `main`.

## Available work

- Task-scoped existing-product, workbench, interaction and bounded review guidance.
- **19 original patterns**: six spatial card compositions and thirteen interactive studies with real local state changes.
- SVG flow, Canvas dot field and WebGL gradient implementation, including pause, reduced motion and static CSS fallback. **The WebGL path has not run successfully in the current test environment.**
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

This batch: **23 focused tests passed, zero skipped**, using complete static pages loaded in memory. Not the full upstream test suite. HTTP navigation was blocked by browser policy; WebGL used the CSS fallback. Native browser zoom, screen readers, real devices, independent-agent review and production usability have not been certified. No new GitHub Actions workflows or paid services.

## Attribution

The upstream engine and methods remain credited to [oil-oil/oil-ui](https://github.com/oil-oil/oil-ui). Public capability references: [upstream comparison](https://github.com/oil-oil/oil-ui/blob/main/README.zh-CN.md#开源版和-pro) and [official introduction](https://ui.oiloil.org/intro/). New workbench categories, components, effects and game examples are independent implementations, not copies of proprietary Pro assets.

[MIT license](LICENSE); upstream copyright notice is preserved.
