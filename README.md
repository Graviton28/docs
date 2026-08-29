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
│   └── okf_validate.py        # OKF v0.2 conformance checker (run in CI)
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

## Content sources

- [UNM-CARC/QuickBytes](https://github.com/UNM-CARC/QuickBytes) — tutorials
  (migrated by `scripts/migrate_quickbytes.py`)
- [UNM-CARC/webinfo](https://github.com/UNM-CARC/webinfo) — systems tables,
  storage and fairshare policy
- [carc.unm.edu](https://carc.unm.edu) — getting started, policies, facilities

## Deployment

Pushing to `main` runs OKF validation and deploys to GitHub Pages via
`.github/workflows/docs.yml` (set the repository's Pages source to
"GitHub Actions"). **TODO:** update `site_url` and `repo_url` in
`zensical.toml` when the final repository location is decided, and replace the
MESA link in `docs/about/partners.md` when the project site is live.
