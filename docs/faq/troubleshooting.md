---
title: "Troubleshooting"
description: "Diagnose the most common problems: login failures, quota errors, pending or failing jobs, and module conflicts."
type: Guide
tags:
  - FAQ
  - Support
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: carc-web
    resource: "https://carc.unm.edu/index.html"
    title: "CARC website (carc.unm.edu)"
    author: "team:unm-carc"
---

# Troubleshooting

Work through the section that matches your symptom. If nothing here fixes it,
[open a ticket](../support/help.md) with the details listed at the bottom of
that page — cluster, job ID, exact command, and full error message.

## I can't log in

1. **Check for maintenance** on the
   [system status page](https://carc.unm.edu/systems/downtime-notices.html){ target=_blank }.
2. **Password or OTP problems** — reset via the steps in
   [password reset](../getting-started/password-reset.md).
3. **`Permission denied (publickey)`** — your SSH key setup is incomplete or
   has wrong permissions; see [SSH keys](../getting-started/ssh-keys.md)
   (`~/.ssh` must be `700`, private keys `600`).
4. **Account exists but no access** — you may not be on an active project
   yet; ask your PI to add you in ColdFront
   ([getting started](../getting-started/overview.md)).

## "Disk quota exceeded"

You've hit a storage limit ([what the limits are](../systems/resource-limits.md)):

```bash
quotas            # show your usage against each quota
du -sh ~/* | sort -rh | head   # find what's using home space
```

Clean up, move bulk data to scratch or project space
([storage layout](../systems/storage.md)), or talk to us about
[purchasing more](https://carc.unm.edu/research/premium-research-computing-services.html){ target=_blank }.
Remember conda environments and pip caches grow quietly — `conda clean --all`
and `pip cache purge` often free gigabytes.

## My job won't start

```bash
squeue -u $USER           # state and reason code
squeue --start --job <id> # predicted start time (fairshare-aware)
sinfo                     # partition and node availability
```

Common reason codes:

| Reason | Meaning | What to do |
| ------ | ------- | ---------- |
| `Priority` | Others are ahead of you (fairshare) | Wait, or request fewer/shorter resources; see [fairshare](../running-jobs/slurm-accounting.md) |
| `Resources` | Not enough free nodes for your request | Reduce cores/memory/GPUs or choose another partition |
| `QOSMax*` / limits | You've hit a partition or account limit | Check [resource limits](../systems/resource-limits.md) |
| `ReqNodeNotAvail` | Nodes down or reserved (often maintenance) | Check the [system status page](https://carc.unm.edu/systems/downtime-notices.html){ target=_blank } |
| `InvalidAccount` | Wrong `--account` | List yours: `sacctmgr show assoc user=$USER format=account` |

## My job failed or was killed

```bash
sacct -j <id> --format=JobID,State,ExitCode,Elapsed,MaxRSS,ReqMem
seff <id>     # efficiency summary after completion
```

* **`OUT_OF_MEMORY` / `oom-kill`** — request more memory (`--mem` or
  `--mem-per-cpu`) or use fewer tasks per node; `seff` shows what you
  actually used.
* **`TIMEOUT`** — raise `--time` within partition limits, or checkpoint and
  restart.
* **Immediate crash** — check the job's `.out`/`.err` files in the submit
  directory; a missing `module load` or unactivated conda environment is the
  usual culprit ([modules](../running-jobs/modules.md),
  [conda](../software/conda-environments.md)).

## Software and environment problems

* **`command not found`** — load the module first (`module spider <name>`
  to find it; [modules guide](../running-jobs/modules.md)).
* **Conda is slow or conflicts** — prefer clean per-project environments and
  the conda-forge channel; see [channels and pip](../software/conda-channels-pip.md).
* **GPU code can't see the GPU** — did you request one in the job
  (`--gres=gpu:1` or the cluster's GPU partition)? Verify with `nvidia-smi`
  inside the job; see [example Slurm scripts](../running-jobs/example-slurm-scripts.md).
* **My kernel is missing in JupyterHub** — register your environment as a
  kernel: [conda in JupyterHub](../software/conda-jupyterhub.md).

## Graphics won't display

X11 applications need forwarding enabled — `ssh -Y` and a local X server;
see [X11 forwarding](../getting-started/x11-forwarding.md). For heavier
visualization, use [ParaView client–server](../software/paraview.md) or an
[Open OnDemand](../interactive/open-ondemand.md) session instead.

## Transfers are slow or failing

Use `rsync` with resume (`rsync -avP`) rather than `scp` for large trees,
and transfer to the right storage tier — see
[transferring data](../getting-started/transferring-data.md).

## Still stuck?

[Open a ticket](../support/help.md) or bring it to office hours — include
your cluster, job ID, command, and the complete error text.
