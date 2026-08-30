---
title: "Storage and compute usage policies"
description: "Storage quotas, Slurm fairshare policy, and per-cluster queue limits."
type: Policy
tags:
  - Policy
  - Storage
  - Slurm
stale_after: "2027-08-31T00:00:00Z"
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: webinfo
    resource: "https://github.com/UNM-CARC/webinfo/blob/master/resource_limits.md"
    title: "UNM-CARC webinfo: resource_limits.md"
    author: "team:unm-carc"
    last_modified: "2023-04-21T16:04:29-06:00"
---

# Storage and compute usage policies

Home directories have a soft limit of 100GB and a hard limit of 200GB. Once you exceed the soft limit we will ask you to reduce your usage. You will not be able to write data beyond the hard limit. Project space is limited to 250 GB. Scratch storage is limited to 1 TB. Center-wide project scratch space is limited to 1 TB and user scratch is limited to 100G (`/carc/scratch`). To purchase additional storage please see our [pricing spreadsheet](https://carc.unm.edu/research/premium-research-computing-services.html){target=_blank}.

The `quotas` command shows your quota usage.

## Compute usage policy

To ensure that all research and class projects get their fair share of the clusters and to prevent any one group from using a disproportionate amount of resources, we utilize Slurm’s built-in job accounting and fairshare system.
The cluster is a limited resource and Fairshare allows us to ensure everyone gets a fair opportunity to use it regardless of how big or small the group is.
Your compute resource allocation is shared among everyone in the slurm account you select. 

For more on Slurm accounts see [Slurm accounting](../running-jobs/slurm-accounting.md).
Note that your slurm account is not the same as your CARC login account.

To see the predicted start time of your job based on your fairshare score, use the following command:
`squeue --start --job <job_id>`

## Hopper Configuration


|                Queue: |   General  |    Debug   | Condo    | Private |
|----------------------:|:----------:|:----------:| :---:    | :---:   |
| Number of Processors  |     64     |     8      | 192      | Determined by <br> queue owner |
|      Number of Nodes  |     2      |      2     | 6        |  |
|   Processors per Node |    32      |      8     | 32       |  |
|       Walltime(H:M:S) |  48:00:00  |  04:00:00  | 48:00:00 |  |
|        Memory Limits  |    90 Gb   |    90 Gb   |          |  |

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/webinfo/blob/master/resource_limits.md){target=_blank} (last source update 2023-04-21). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes){target=_blank}.</p>
