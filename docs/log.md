# Documentation update log

## 2026-08-29

* **Creation**: Added the Interactive computing section ([Open OnDemand](interactive/open-ondemand.md), [JupyterHub](interactive/jupyterhub.md)) and the FAQ section ([General FAQ](faq/general.md), [Troubleshooting](faq/troubleshooting.md)).
* **Creation**: Added [Contributing to these docs](about/contributing.md) — the OKF frontmatter contract, verification workflow, and local build instructions for CARC staff.
* **Update**: Added machine-readable `llms.txt` and `llms-full.txt` indexes generated from OKF frontmatter (`scripts/gen_llms_txt.py`, enforced in CI); moved the page table of contents into the left sidebar.

* **Initialization**: Created this documentation bundle with [Zensical](https://zensical.org){target=_blank}, structured as an Open Knowledge Format (OKF v0.2) knowledge bundle.
* **Migration**: Migrated 56 tutorials and guides from [UNM-CARC/QuickBytes](https://github.com/UNM-CARC/QuickBytes){target=_blank} and [UNM-CARC/webinfo](https://github.com/UNM-CARC/webinfo){target=_blank} with provenance frontmatter (`generated`, `sources`, per-file `last_modified` from git history). All migrated pages are unverified pending CARC staff review.
* **Creation**: Wrote the [Getting started overview](getting-started/overview.md), [Good Neighbor Use Policy](getting-started/good-neighbor-policy.md), [Systems overview](systems/overview.md), [Video tutorials](training/videos.md), [Getting help](support/help.md), [Acknowledging CARC](support/acknowledging-carc.md), [Mission and vision](about/mission.md), [Facilities description](about/facilities.md), and [Partner cyberinfrastructure](about/partners.md) pages from carc.unm.edu content.
* **Deprecation**: Marked [Cluster specifications](systems/cluster-specifications.md) (retired Wheeler, Taos, and Gibbs systems) and [R batch jobs with PBS](software/r-pbs-jobs.md) as deprecated; both are kept for history and links.
