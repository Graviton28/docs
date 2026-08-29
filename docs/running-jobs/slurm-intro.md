---
title: "Introduction to Slurm"
description: "Slurm basics on CARC clusters: partitions, interactive jobs, and your first batch script."
type: Guide
tags:
  - Slurm
  - Jobs
  - New users
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/Intro_to_slurm.md"
    title: "UNM-CARC QuickBytes: Intro_to_slurm.md"
    author: "team:unm-carc"
    last_modified: "2026-07-06T13:37:22-06:00"
---

# Introduction to Slurm

## Getting Started

For a general introduction to Slurm — including an overview of its architecture, key commands (`sinfo`, `squeue`, `srun`, `sbatch`, `scancel`, `scontrol`), and basic job submission examples — refer to the **[official Slurm Quick Start User Guide](https://slurm.schedmd.com/quickstart.html){target=_blank}**. The guide is well-maintained and covers the core concepts you need to get up and running.

The sections below supplement that guide with information specific to CARC Easley at the University of New Mexico.

---

## CARC Easley Partitions

When you run `sinfo` on Easley, you will see output similar to the following:

```bash
[username@easley ~]$ sinfo
```

```
PARTITION   AVAIL  TIMELIMIT  NODES  STATE NODELIST
general*       up 2-00:00:00      1   comp easley002
general*       up 2-00:00:00      4   mix- easley[008,015,018,044]
general*       up 2-00:00:00      8    mix easley[003-004,012-014,016,020,023]
general*       up 2-00:00:00     34  alloc easley[001,005-007,009-011,017,019,021-022,024-043,046-048]
general*       up 2-00:00:00      1   down easley045
bigmem         up 2-00:00:00      1    mix easley050
bigmem         up 2-00:00:00      1  alloc easley049
h100           up 2-00:00:00      1   mix- easley051
h100           up 2-00:00:00      1   plnd easley054
h100           up 2-00:00:00      2  alloc easley[052-053]
l40s           up 2-00:00:00      1    mix easley055
l40s           up 2-00:00:00      2  alloc easley[056-057]
interactive    up    4:00:00      1   comp easley002
interactive    up    4:00:00      5   mix- easley[008,015,018,044,051]
interactive    up    4:00:00      1   plnd easley054
interactive    up    4:00:00     10    mix easley[003-004,012-014,016,020,023,050,055]
interactive    up    4:00:00     39  alloc easley[001,005-007,009-011,017,019,021-022,024-043,046-049,052-053,056-057]
interactive    up    4:00:00      1   down easley045
debug          up    1:00:00      1   comp easley002
debug          up    1:00:00      5   mix- easley[008,015,018,044,051]
debug          up    1:00:00      1   plnd easley054
debug          up    1:00:00     10    mix easley[003-004,012-014,016,020,023,050,055]
debug          up    1:00:00     39  alloc easley[001,005-007,009-011,017,019,021-022,024-043,046-049,052-053,056-057]
debug          up    1:00:00      1   down easley045
scavenger      up 2-00:00:00      1   comp easley002
scavenger      up 2-00:00:00      9   mix- easley[008,015,018,044,051,060-063]
scavenger      up 2-00:00:00      1   plnd easley054
scavenger      up 2-00:00:00     10    mix easley[003-004,012-014,016,020,023,050,055]
scavenger      up 2-00:00:00     41  alloc easley[001,005-007,009-011,017,019,021-022,024-043,046-049,052-053,056-059]
scavenger      up 2-00:00:00      1   down easley045
```

Key partitions you may have access to:

- **general** — The default community partition. Maximum wall time of 2 days. Use this if you are not a member of a specific condo group.
- **debug** — Short jobs only (4-hour limit). Useful for testing scripts before submitting long runs.
- **condo** — Purchased nodes available to specific research groups. If you are a member of a condo group, you likely already know your partition name. Check with your PI if you are unsure.
- **scavenger** - Whenever a purchased/reserved node is not in use, this partition grabs them and allows them to be used by the public, but be warned you will be kicked off if the owner begins a job on it.

To see detailed node information including CPU count, memory, and disk:

```bash
sinfo -N -l
```

If you omit `--partition` (or `-p`) from your job submission, your job will be submitted to the `general` partition by default.

---

## Useful `squeue` Flags

The official guide covers `squeue` basics. A few flags that are especially handy on a shared cluster:

```bash
squeue --me              # Show only your jobs
squeue -p general        # Show only jobs in the general partition
squeue -u <username>     # Show jobs for a specific user
```

---

## Canceling Jobs

```bash
scancel <JOBID>          # Cancel a specific job
scancel --me             # Cancel all of your jobs
```

---

## Notes on Resource Requests

- The more constraints you add to a job (e.g., requiring all tasks on the same node with `--ntasks-per-node`), the longer your queue time may be. Requesting resources spread across nodes often results in faster scheduling.
- Memory is specified per CPU with `--mem-per-cpu` (in MB) or for the whole job with `--mem`.
- Time limits use the format `D-HH:MM:SS` (e.g., `1-12:00:00` for 1 day and 12 hours) or `MM:SS` / `HH:MM:SS` for shorter jobs.

---

## Additional Resources

- [Official Slurm Quick Start Guide](https://slurm.schedmd.com/quickstart.html){target=_blank}
- [CARC at UNM Documentation](https://carc.unm.edu){target=_blank}
- For help, contact the CARC support team or visit the CARC user portal.


*This quickbyte was validated on 6/22/2026.*

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/Intro_to_slurm.md){target=_blank} (last source update 2026-07-06). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes){target=_blank}.</p>
