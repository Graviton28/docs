# CARC Documentation

User and researcher documentation for the [UNM Center for Advanced Research
Computing (CARC)](https://carc.unm.edu), built with
[Zensical](https://zensical.org) and structured as an
[Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
knowledge bundle so the content is first-class for both humans and AI agents.

Design inspired by the
[Jetstream2 documentation](https://gitlab.com/jetstream-cloud/jetstream2/docs).

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install zensical
zensical serve          # live preview at http://localhost:8000
zensical build --clean  # static site in ./site
```

## Repository layout

```
├── zensical.toml            # Site configuration (theme, nav, extensions)
├── docs/                    # The OKF knowledge bundle + site content
│   ├── index.md             # Landing page (declares okf_version: "0.2")
│   ├── log.md               # OKF update log (reserved filename)
│   ├── <section>/index.md   # OKF directory listings / section landing pages
│   ├── <section>/*.md       # OKF concept documents (YAML frontmatter + body)
│   ├── assets/              # Images, downloadable files, logos
│   └── stylesheets/         # UNM cherry + turquoise theme (extra.css)
├── scripts/
│   ├── migrate_quickbytes.py  # Reproducible migration from UNM-CARC/QuickBytes
│   ├── okf_validate.py        # OKF v0.2 conformance checker (run in CI)
│   └── gen_llms_txt.py        # Builds docs/llms.txt + docs/llms-full.txt
└── .github/workflows/docs.yml # OKF validation + GitHub Pages deployment
```

## Machine readability (OKF)

Every concept page carries YAML frontmatter with:

- `type` — `Guide`, `Tutorial`, `Reference`, or `Policy` (required by OKF)
- `title`, `description`, `tags` — used by search, social cards, and agents
- `generated: { by, at }` — who/what produced the current content
- `sources` — provenance links back to the original QuickBytes file or
  carc.unm.edu page, with `last_modified` from git history
- `status` / `stale_after` — lifecycle markers (`deprecated` pages are kept
  for history; hardware pages carry an explicit staleness horizon)

Pages migrated by an agent are intentionally left **unverified** (no
`verified` key). When CARC staff review a page, they should add:

```yaml
verified: { by: "human:<netid>", at: "2026-XX-XXT00:00:00Z" }
```

Validate conformance locally:

```bash
python scripts/okf_validate.py docs
```

The deployed site is directly consumable by AI agents:

- `/llms.txt` ([convention](https://llmstxt.org)) — linked outline;
  `/llms-full.txt` — the full corpus with frontmatter in one file.
- **Markdown mirror**: any page URL + `index.md` returns that page's source
  with OKF frontmatter (e.g. `/running-jobs/slurm-intro/index.md`).
- Rendered pages carry `<link rel="alternate" type="text/markdown">` and
  `okf:*` meta tags (type, status, trust tier, generated-at, stale-after).
- `robots.txt` advertises all of the above; `docs/about/ai-agents.md` is the
  human/agent-readable guide, and `AGENTS.md` guides coding agents working
  in this repository.

Regenerate the llms indexes after content changes (CI fails on drift), and
run the agent-surface step after every build:

```bash
python scripts/gen_llms_txt.py
zensical build --clean && python scripts/postbuild_agent_surface.py
```

## Content sources

- [UNM-CARC/QuickBytes](https://github.com/UNM-CARC/QuickBytes) — tutorials
  (migrated by `scripts/migrate_quickbytes.py`)
- [UNM-CARC/webinfo](https://github.com/UNM-CARC/webinfo) — systems tables,
  storage and fairshare policy
- [carc.unm.edu](https://carc.unm.edu) — getting started, policies, facilities

## Deployment

Pushing to `main` on [UNM-CARC/docs](https://github.com/UNM-CARC/docs) runs
OKF validation, checks the llms.txt indexes for drift, builds the site, adds
the agent surface, and deploys to GitHub Pages at
<https://unm-carc.github.io/docs/> via `.github/workflows/docs.yml`. The
workflow enables Pages automatically (`configure-pages` with
`enablement: true`); if the first deploy fails on permissions, set
Settings → Pages → Source to "GitHub Actions" once.
