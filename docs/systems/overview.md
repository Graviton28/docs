---
title: "Systems overview"
description: "Current CARC clusters (Easley and Hopper), storage tiers, and web portals such as JupyterHub, Open OnDemand, and XDMoD."
type: Reference
tags:
  - Systems
  - Hardware
stale_after: "2027-08-31T00:00:00Z"
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: carc-facilities
    resource: "https://carc.unm.edu/about-carc/facilities-description.html"
    title: "CARC facilities description (carc.unm.edu)"
    author: "team:unm-carc"
---

# Systems overview

CARC operates several high-performance computing clusters serving disciplines
from traditional scientific computing to data analytics, artificial
intelligence, and machine learning.

## Compute clusters

| Cluster | Nodes | CPU cores | GPUs | Interconnect | Notes |
| ------- | :---: | :-------: | ---- | ------------ | ----- |
| **Easley** | 65 | 4,160 | 36× NVIDIA L40S (AI/ML) + 8× NVIDIA H100 (double precision) | NVIDIA NDR 800 Gbps InfiniBand | Newest cluster; 23.3 TB total RAM |
| **Hopper** | 61 | 2,176 | 37× NVIDIA A100 | NVIDIA HDR 400 Gbps InfiniBand | General and GPU-accelerated workloads |

For queue limits and walltimes, see [resource limits](resource-limits.md).
Historical specifications for retired systems (Wheeler, Taos, Gibbs, and
Xena) are kept in the [legacy cluster reference](cluster-specifications.md).

## Storage

CARC provides multiple tiers of high-performance storage:

* **720 TB** of all-flash IBM Storage Scale (GPFS) scratch
* **2 PB** of BeeGFS working scratch
* **2.4 PB** of NetApp enterprise storage, with automated hourly, daily,
  weekly, and monthly snapshots retained up to four months for user-directed
  recovery

See [storage and backups](storage.md) for how home, project, and scratch
spaces work, and [resource limits](resource-limits.md) for quotas.

In partnership with UNM Libraries, CARC also supports virtual machine
infrastructure for custom research applications, secure data hosting, and
flexible computing environments.

## Web portals

| Portal | URL | Purpose |
| ------ | --- | ------- |
| JupyterHub (Hopper) | [hopper.alliance.unm.edu](https://hopper.alliance.unm.edu){ target=_blank } | Interactive notebooks on Hopper |
| JupyterHub (Easley) | [easley.alliance.unm.edu/jupyter](https://easley.alliance.unm.edu/jupyter){ target=_blank } | Interactive notebooks on Easley |
| Open OnDemand | [ood.alliance.unm.edu](https://ood.alliance.unm.edu){ target=_blank } | Browser-based files, shells, and interactive apps |
| ColdFront | [coldfront.alliance.unm.edu](https://coldfront.alliance.unm.edu){ target=_blank } | Project, allocation, and publication management |
| XDMoD | [xdmod.alliance.unm.edu](https://xdmod.alliance.unm.edu){ target=_blank } | System usage metrics by PI |
| Help desk | [support.alliance.unm.edu](https://support.alliance.unm.edu){ target=_blank } | Create or manage help tickets |

## Status and downtime

Check the live monitors directly:

* [Cluster login & website status](https://stats.uptimerobot.com/kqt0LYLwFd){ target=_blank } — per-system up/down and response times
* [UNM IT alerts](https://italerts.unm.edu/){ target=_blank } — campus-wide IT outage notices
* [Network performance](http://perfsonar.alliance.unm.edu){ target=_blank } — perfSONAR measurements for the CARC network
* [Easley external DNS check](https://dnschecker.org/#A/easley.alliance.unm.edu){ target=_blank } — worldwide resolution of easley.alliance.unm.edu
* [System usage (XDMoD)](https://xdmod.alliance.unm.edu/){ target=_blank } — utilization metrics by system and principal investigator

## Networking

CARC systems connect to campus through multiple 10 Gbps links, including a
dedicated 10 Gbps connection to UNM's Science DMZ research network. External
connectivity includes 100 Gbps connections to ESnet and the Western Regional
Network through the Albuquerque Gigapop.

## Export control

The U.S. Government controls the export of sensitive equipment, software, and
technology. Installation of export-controlled software on CARC systems
requires prior written approval from
[UNM Export Control](https://carc.unm.edu/systems/export-control.html){ target=_blank } —
see the [Good Neighbor Use Policy](../getting-started/good-neighbor-policy.md).
