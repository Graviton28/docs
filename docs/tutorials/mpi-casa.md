---
title: "Parallel CASA for radio astronomy"
description: "Run mpiCASA for parallel radio astronomy imaging on CARC clusters."
type: Tutorial
tags:
  - Astronomy
  - MPI
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/mpiCASA.md"
    title: "UNM-CARC QuickBytes: mpiCASA.md"
    author: "team:unm-carc"
    last_modified: "2021-03-08T15:51:32-07:00"
---

# Parallel CASA for radio astronomy

### A Bit About CASA

[CASA](https://casa.nrao.edu/) is the premier software for reducing radio data coming off of a variety of telescopes around the world, including the Jansky Very Large Array (VLA) and Atacama Large Millimeter Array (ALMA). 

### Getting Some Data to Play With

Going to use the new [Archive](data.nrao.edu). Find something small and have them download it manually, like a few GB at most.

### Getting Set Up

First off get some nodes

```bash
srun --partition singleGPU --nodes 2 --tasks-per-node 2 --pty bash
```

Do we want singleGPU? Can request more nodes obviously. tasks-per-node we don't need to set unless CASA demands slots

Might want to create aliases for casa and mpi casa, just to make things quick

```bash
alias casa='/users/sbruzew/xena-scratch/casa-blah-blah/bin/casa'
alias mpicasa='/users/sbruzew/xena-scratch/casa-blah-blah/bin/mpicasa'
```

Actually it doesn't like the alias when you run the command

2) It will create a nodefile for us at $PBS_NODEFILE
   If CASA doesn't need slots, we can use this, and all the nodes
   If CASA does need slots, we'll need to make a script that can reference $PBS_NUM_PPN and add slots

3) Run something like 'path_to_casa_bin/mpicasa -hostfile $PBS_NODEFILE path_to_casa_bin/casa <casa options>'
   Probably want to do --nogui and --log2term
   Puts us into a CASA environment

4) Run python script that does all the fun stuff
   Could run mpicasa call with '-c myscript.py'
   Can also do 'exec(open('./filename').read())'
       Shortcut as execfile 'filename.py'

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/mpiCASA.md) (last source update 2021-03-08). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes).</p>
