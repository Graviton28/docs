---
title: "Submitting jobs"
description: "Submit, monitor, and cancel batch and interactive jobs with Slurm."
type: Guide
tags:
  - Slurm
  - Jobs
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/submitting_jobs.md"
    title: "UNM-CARC QuickBytes: submitting_jobs.md"
    author: "team:unm-carc"
    last_modified: "2025-12-03T11:52:10-07:00"
---

# Submitting jobs

There are two ways you can run your jobs, namely submitting a Slurm script and running a job interactively. Either way, jobs are submitted to CARC by the command `sbatch`. For more information on available options type `man sbatch`
### Submitting the Slurm Script to the Batch Scheduler
In order to run our simple Slurm script, we will need to submit it to the batch scheduler using the command `sbatch` followed by the name of the script we would like to run. For more information please see our page on writing a [Slurm batch script](https://github.com/UNM-CARC/QuickBytes/blob/master/pbs_scripts2.md).
In the following example, we submit our simple `hello.sbatch` script to the batch scheduler using `sbatch`. Note that it returns the job identifier when the job is successfully submitted. You can use this job identifier to query the status of your job from your shell.  
For example:

```bash
sbatch hello.sbatch
Submitted batch job 156452
```
### Interactive Slurm Jobs
Normally a job is submitted for execution on a cluster or supercomputer using the command `sbatch script.sbatch`. CARC recommends that all jobs are submitted this way as job submission fails if there are errors in resources requested. However, at times, such as when debugging, it can be useful to run a job interactively. To run a job in this way type `salloc` followed by resources requested, and the batch manager will log you into a node where you can directly run your code.  
For example, here is the output from an interactive session running our simple `helloworld_paralell.sbatch` script:

```bash
salloc --nodes=1 --ntasks=8 --time=00:05:00

salloc: Granted job allocation 156469
salloc: Nodes easley004 are ready for job

module load openmpi

bash  helloworld_parallel.sbatch
Job 156469 running on easley004
Hello World from host easley004
Hello World from host easley004
Hello World from host easley004
Hello World from host easley004
Hello World from host easley004
Hello World from host easley004
Hello World from host easley004
Hello World from host easley004
```
Three commands were executed here. The first,

```bash
salloc --nodes=1 --ntasks=8 --time=00:05:00
```
asked the batch manager to provide one node of easley with all 8 of that node’s cores for use. It is good practice to request all available processors on a node to avoid multiple users being assigned to the same node. The walltime was specified as 5 minutes, since this was a simple code that would execute quickly. The second command, 

```bash
module load openmpi
```
loaded the openMPI software module to parallelize our script across all 8 processors; this ensures that the necessary MPI libraries would be available during execution. The third command, 

```bash
bash  helloworld_parallel.sbatch
```
ran the commands found within our `helloworld_parallel.sbatch` script.

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/submitting_jobs.md) (last source update 2025-12-03). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes).</p>
