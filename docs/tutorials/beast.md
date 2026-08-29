---
title: "Bayesian phylogenetics with BEAST"
description: "Run BEAST Bayesian evolutionary analyses on CARC clusters."
type: Tutorial
tags:
  - Bioinformatics
  - Phylogenetics
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/Beast_at_CARC.md"
    title: "UNM-CARC QuickBytes: Beast_at_CARC.md"
    author: "team:unm-carc"
    last_modified: "2019-10-15T10:51:40-06:00"
---

# Bayesian phylogenetics with BEAST

!!! note "Legacy content"
    This page mentions retired CARC systems (Wheeler, Taos, or Gibbs). The workflow remains a useful example, but verify cluster names, partitions, and module versions against the [current systems](../systems/overview.md).

Bayesian Evolutionary Analysis by Sampling Trees [(BEAST)](https://beast.community/index.html){target=_blank} is a software package that performs
phylogenetic tree analysis with user specified molecular clock models using the widely popular Bayesian Markov chain Monte Carlo 
(MCMC) methods. BEAST has its origins in modeling pathogen evolution in near real time but is also popular for other phylogenetic 
applications. BEAST is a well documented and flexible tool for modeling phylogenetics. Using BEAST at CARC offers more power for 
rigorous computations.

## Generating BEAST imput files: BEAUti

BEAST uses .xml files which contain sequences and model parameters. Because BEAST is capable of incorporating a diverse range of 
meta data and specific time modeling parameters, the graphical user interface [BEAUTi](https://beast.community/first_tutorial){target=_blank} 
allows users to upload nexus files and create .xml files with ease. Make sure that the version of beast in the module you load 
matches the version of BEAUTi used to generate the .xml files. 

## Running BEAST on Wheeler

Once a .xml file is generated, beast can be easily run on CARC. An example .pbs script is as follows: 

```
#!/bin/bash

#PBS -q default
#PBS -N BEASTjob
#PBS -l nodes=1:ppn=8
#PBS -l walltime=24:00:00
#PBS -j oe

cd $PBS_O_WORKDIR

module load beast2-2.5.2-intel-19.0.4-hcnoysj

beast my_data.xml
```

The output should be a job log (joined with any potential error file), and a .tree file for your downstream analysis. For more assistance 
with BEAST at CARC please email help@carc.unm.edu.

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/Beast_at_CARC.md){target=_blank} (last source update 2019-10-15). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes){target=_blank}.</p>
