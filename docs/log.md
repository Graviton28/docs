# Documentation update log

## 2026-08-29

* **Update**: Made the deployed site directly consumable by AI agents: every page's Markdown source (OKF frontmatter intact) is now served at its URL plus `index.md`; rendered pages advertise it via `link rel=alternate` and `okf:*` meta tags (type, status, trust tier, generated-at); `robots.txt` points crawlers at `llms.txt`, the full corpus, and the mirror convention (`scripts/postbuild_agent_surface.py`, wired into CI). Added the [For AI agents](about/ai-agents.md) guide and a repository `AGENTS.md`/`CLAUDE.md` for coding harnesses.

* **Update**: Embedded CARC YouTube recordings across the site: the [Video tutorials](training/videos.md) page now carries the full QuickBytes playlist, CARC Annual Meeting 2025 talks, and research presentations from the UNMCARC channel; ten guide pages (logging in, Slurm intro, storage, transfers, modules, conda, X11, GNU Parallel, SimCov, parallel R) embed their matching walkthrough via the migration pipeline.
* **Creation**: Rebuilt the [Workshops and slides](training/workshops.md) page (previously a stub) as a curated catalog of 33 slide decks: the Introduction to CARC series, domain-focused workshops, course guest lectures, and legacy material.

* **Update**: The Xena cluster has been retired. Removed Xena from the [Systems overview](systems/overview.md), [Facilities description](about/facilities.md), FAQ, and landing page; added it to the retired-systems list in [Cluster specifications](systems/cluster-specifications.md); marked Xena-specific GPU guides (PyTorch, MATLAB GPU/deep learning, deep-learning packages) as `status: draft` with legacy notices pending review against Hopper and Easley GPUs.
* **Update**: Annotated all code across the corpus: tab-indented QuickBytes code now renders as language-fenced blocks with syntax highlighting; restructured [Installing deep learning packages](software/deep-learning-packages.md) (now curated in-repo); annotated inline code references in [Parallel R with the future package](software/parallel-r-future.md).

* **Creation**: Added the Interactive computing section ([Open OnDemand](interactive/open-ondemand.md), [JupyterHub](interactive/jupyterhub.md)) and the FAQ section ([General FAQ](faq/general.md), [Troubleshooting](faq/troubleshooting.md)).
* **Creation**: Added [Contributing to these docs](about/contributing.md) — the OKF frontmatter contract, verification workflow, and local build instructions for CARC staff.
* **Update**: Added machine-readable `llms.txt` and `llms-full.txt` indexes generated from OKF frontmatter (`scripts/gen_llms_txt.py`, enforced in CI); moved the page table of contents into the left sidebar.

* **Initialization**: Created this documentation bundle with [Zensical](https://zensical.org){target=_blank}, structured as an Open Knowledge Format (OKF v0.2) knowledge bundle.
* **Migration**: Migrated 56 tutorials and guides from [UNM-CARC/QuickBytes](https://github.com/UNM-CARC/QuickBytes){target=_blank} and [UNM-CARC/webinfo](https://github.com/UNM-CARC/webinfo){target=_blank} with provenance frontmatter (`generated`, `sources`, per-file `last_modified` from git history). All migrated pages are unverified pending CARC staff review.
* **Creation**: Wrote the [Getting started overview](getting-started/overview.md), [Good Neighbor Use Policy](getting-started/good-neighbor-policy.md), [Systems overview](systems/overview.md), [Video tutorials](training/videos.md), [Getting help](support/help.md), [Acknowledging CARC](support/acknowledging-carc.md), [Mission and vision](about/mission.md), [Facilities description](about/facilities.md), and [Partner cyberinfrastructure](about/partners.md) pages from carc.unm.edu content.
* **Deprecation**: Marked [Cluster specifications](systems/cluster-specifications.md) (retired Wheeler, Taos, and Gibbs systems) and [R batch jobs with PBS](software/r-pbs-jobs.md) as deprecated; both are kept for history and links.
