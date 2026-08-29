---
title: "Cluster specifications (legacy reference)"
description: "Historical hardware tables for CARC clusters, including retired systems such as Wheeler, Taos, and Gibbs."
type: Reference
tags:
  - Systems
  - Hardware
  - Legacy
status: deprecated
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: webinfo
    resource: "https://github.com/UNM-CARC/webinfo/blob/master/systems_information.md"
    title: "UNM-CARC webinfo: systems_information.md"
    author: "team:unm-carc"
    last_modified: "2023-01-23T10:24:36-07:00"
---

# Cluster specifications (legacy reference)

!!! warning "Legacy content"
    This page is kept for history and links. Wheeler, Taos, and Gibbs have been retired — see the [Systems overview](overview.md) for current clusters.

## CARC Supercomputer and Cluster Resources

| **Machine Name** | **Wheeler** | **Taos** | **Gibbs** | **Xena** | **Hopper** |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Model/Type** | SGI AltixXE<br>Xeon X5550<br>2.67 GHz | Dell PowerEdge R630<br>Xeon E5-2698 V4<br>2.20 GHz | Dell PowerEdge R620<br>Intel Xeon E5-2670<br>2.6 GHz | Dell PowerEdge R730<br>Intel Xeon E5-2640<br>2.6 GHz<br>and<br>PowerEdge R930<br>Intel Xeon E7-4809<br>2.0 Ghz | Dell PowerEdge R640<br>Intel Xeon Gold 6226R<br>2.9 GHz<br>and<br>Dell PowerEdge R740<br>Intel Xeon Gold 6242<br>2.8 GHz |
| **Linux Operating<br>System** | CentOS 7 | CentOS 7 | Scientific Linux | CentOS 7 | Rocky Linux |
| **Interconnect** | Mellanox IS5600<br>InfiniScale IV<br>ConnectX-2 IB QDR<br>(MT26428) | Mellanox SX6000<br>ConnectX-3 IB FDR<br>(MT4099) | InfiniBand QDR | InfiniBand FDR | InfiniBand HDR |
| **Nodes** | 304 | 9 | 24 | 32 | 61 |
| **Cores/Node** | 8 | variable | 16 | 16, 32 | 32 |
| **Total Cores** | 2432 | 180 | 384 | 576 | 2176 |
| **RAM/Core** | 6GB | variable | 4 GB | 4 GB, 32 GB, 96 GB | variable |
| **Local disk/node** | Diskless | 1 TB | 1 TB | 1 TB | 448 GB |
| **Peak FLOPS<br>(theoretical),<br>in TFLOPS** | 25 | (TBD) | 3.996 | 18 | (TBD) |
| **Processor Architecture** | Intel Xeon<br>Nehalem EP | Intel Xeon<br>Broadwell | Intel SandyBridge | Intel Xeon E7-2640<br>Intel Xeon E7-4809<br>(Haswell) | Intel Xeon Gold 6226R<br>Intel Xeon Gold 6242<br>(Cascade Lake) |
| **Local Scratch Space<br>(TB)** | 40 | 27 | 6.3 | 73 | (TBD) |


### Xena Cluster Specs

| **Queue Name** | bigmem-1TB | bigmem-3TB | dualGPU | singleGPU |
| :---: | :---: | :---: | :---: | :---: |
| **Nodes** | 2 | 2 | 4 | 24 |
|**Cores/Node** | 32 | 32 | 16 | 16 |
|**Memory/Node** | 1 TB | 3 TB| 64 GB | 64 GB |
| **Total Cores** | 64 | 64 | 64 | 384 |
| **Processor<br>Architecture** | Intel Xeon<br>CPU E7-4809 | Intel Xeon<br>CPU E7-4809 | Intel Xeon<br>CPU E5-2640 | Intel Xeon<br>CPU E5-2640 |
| **CPU GHz** | 2.00 | 2.00 | 2.60 | 2.60 |
| **GPU** | N/A | N/A | 2 x Nvidia Tesla<br>K40M per node | 1 x Nvidia Tesla<br>K40M per node |

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/webinfo/blob/master/systems_information.md){target=_blank} (last source update 2023-01-23). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes){target=_blank}.</p>
