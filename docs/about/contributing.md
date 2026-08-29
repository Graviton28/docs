---
title: "Contributing to these docs"
description: "How to edit pages, the OKF frontmatter contract, verifying migrated content, and building the site locally."
type: Guide
tags:
  - About
  - Contributing
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: okf-spec
    resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
    title: "Open Knowledge Format (OKF) v0.2 specification"
    author: "team:google-cloud"
---

# Contributing to these docs

This documentation is a git repository of Markdown files, built with
[Zensical](https://zensical.org){target=_blank} and structured as an
[Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md){target=_blank}
knowledge bundle — every page is readable by people *and* consumable by AI
agents, with provenance and trust signals in its frontmatter.

## Small fixes

Every page has an **edit button** (:material-pencil:) in the upper right that
opens the source file on GitHub. Fix the text, propose the change, and CI
validates and deploys it once merged.

## The frontmatter contract

Every content page starts with YAML frontmatter. `type` is required by OKF;
the rest make the page trustworthy and discoverable:

```yaml
---
title: "Page title"
description: "One sentence used by search, cards, indexes, and agents."
type: Guide            # Guide | Tutorial | Reference | Policy
tags:
  - Slurm
generated:
  by: "human:yournetid"          # who/what wrote the current content
  at: "2026-08-29T00:00:00Z"
sources:                          # where the content came from (optional)
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/..."
    title: "Original source"
    author: "team:unm-carc"
status: stable          # draft | stable | deprecated (default: stable)
---
```

Section `index.md` files are OKF directory listings and carry **no
frontmatter**; `log.md` is the bundle's dated change log — add an entry when
you make a meaningful change.

## Verifying migrated pages

Pages migrated from QuickBytes were produced by an agent and are
intentionally **unverified**. When you review one and confirm it is correct
for current systems, record it:

```yaml
verified: { by: "human:yournetid", at: "2026-09-15T00:00:00Z" }
```

If a page is obsolete, don't delete it — set `status: deprecated`, add a
note pointing at the replacement, and log the change in `log.md`.

## Building locally

```bash
git clone <this repository> && cd carc_documentation
python3 -m venv .venv && source .venv/bin/activate
pip install zensical pyyaml
zensical serve                      # live preview at localhost:8000
python3 scripts/okf_validate.py docs   # OKF conformance check (runs in CI)
python3 scripts/gen_llms_txt.py        # regenerate llms.txt indexes
```

## The pipeline scripts

* `scripts/migrate_quickbytes.py` — the reproducible migration from
  [UNM-CARC/QuickBytes](https://github.com/UNM-CARC/QuickBytes){target=_blank} and
  [webinfo](https://github.com/UNM-CARC/webinfo){target=_blank}. It owns the page mapping
  and regenerates every section `index.md`; if you add a page, add it to the
  mapping there so the indexes stay complete.
* `scripts/okf_validate.py` — fails CI if any page breaks OKF conformance
  (missing frontmatter, missing `type`, malformed `log.md`, frontmatter on a
  section index).
* `scripts/gen_llms_txt.py` — builds `docs/llms.txt` (a linked site outline
  per [llmstxt.org](https://llmstxt.org){ target=_blank }) and
  `docs/llms-full.txt` (the full corpus with frontmatter) so AI assistants
  can consume the documentation directly.

## Style notes

* One `#` H1 per page, matching the frontmatter `title`.
* Relative links between pages (`../section/page.md`) — CI warns on broken ones.
* Admonitions (`!!! note`, `??? question`) for asides; content tabs for
  OS-specific instructions.
* Put images in `docs/assets/images/` and downloadable files in
  `docs/assets/files/`.
