---
title: "Open OnDemand"
description: "Use CARC clusters from your browser: files, shells, job management, and interactive apps."
type: Guide
tags:
  - Interactive
  - Open OnDemand
  - New users
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: carc-web
    resource: "https://carc.unm.edu/index.html"
    title: "CARC website (carc.unm.edu)"
    author: "team:unm-carc"
  - id: ood-docs
    resource: "https://osc.github.io/ood-documentation/latest/"
    title: "Open OnDemand documentation (OSC)"
    author: "team:osc"
---

# Open OnDemand

[Open OnDemand](https://openondemand.org){ target=_blank } (OOD) gives you a
complete web interface to CARC clusters — no SSH client, no X11 setup, just a
browser. It is the easiest way to work on CARC systems if you are new to HPC
or away from your usual machine.

[:material-monitor-dashboard: Open the CARC OnDemand portal](https://ood.alliance.unm.edu){ .md-button .md-button--primary target=_blank }

Log in with your CARC username and password. If you don't have an account yet,
start with [Getting started at CARC](../getting-started/overview.md).

## What you can do in OnDemand

<div class="grid cards" markdown>

-   :material-folder-open:{ .lg .middle } __Files__

    ---

    Browse your home, project, and scratch spaces; upload and download files;
    edit text files in the browser. For large transfers, prefer the
    [command-line tools](../getting-started/transferring-data.md).

-   :material-console:{ .lg .middle } __Cluster shell__

    ---

    Open a login-node terminal in a browser tab — everything you can do over
    SSH, without an SSH client.

-   :material-tray-full:{ .lg .middle } __Jobs__

    ---

    Compose, submit, and monitor [Slurm jobs](../running-jobs/slurm-intro.md)
    from a form-based interface, and inspect their output files when they
    finish.

-   :material-application-brackets:{ .lg .middle } __Interactive apps__

    ---

    Launch graphical and notebook sessions that run on compute nodes. The
    available apps depend on the cluster — check the *Interactive Apps* menu
    in the portal for the current list.

</div>

## How interactive apps work

When you launch an interactive app, OnDemand submits a Slurm job on your
behalf. That means:

* You choose the resources (cores, memory, GPUs, walltime) in the launch
  form — the same considerations as any [batch job](../running-jobs/submitting-jobs.md)
  apply, and the [Good Neighbor Use Policy](../getting-started/good-neighbor-policy.md)
  asks you not to leave hardware idle.
* Your session may wait in the queue until resources are free, just like any
  other job. Small, short requests start faster.
* The session ends when its walltime expires — save your work.
* Usage counts against your project's
  [fairshare](../running-jobs/slurm-accounting.md) like any other job.

!!! tip "When to use OnDemand vs. SSH"

    OnDemand is ideal for file management, quick edits, monitoring jobs, and
    interactive sessions. For long-running automated workflows, scripted
    submission, and bulk data movement, the [command line](../getting-started/logging-in.md)
    remains the more powerful tool.

## Related pages

* [JupyterHub](jupyterhub.md) - a dedicated notebook portal on Hopper and Easley.
* [Introduction to Slurm](../running-jobs/slurm-intro.md) - understand what OnDemand submits for you.
* [Getting help](../support/help.md) - if the portal misbehaves, open a ticket.
