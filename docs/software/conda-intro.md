---
title: "Conda and Anaconda: introduction"
description: "What conda is, how environments work, and how to use Anaconda/Miniconda on CARC systems."
type: Guide
tags:
  - Python
  - Conda
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/anaconda_general_intro.md"
    title: "UNM-CARC QuickBytes: anaconda_general_intro.md"
    author: "team:unm-carc"
    last_modified: "2020-01-28T10:52:07-07:00"
---

# Conda and Anaconda: introduction

### What is Anaconda?

At a basic level Anaconda is a distribution of Python and R, although there is an emphasis on working with python, that provides access collections of associated packages optimized specifically for data science maintained in repositories. The installation and management of these packages is handled with the Anaconda package manager Conda. While initially focused mainly on python packages the repositories hosted by Anaconda and others now house a large collection of non-python packages.  

Conda is more than just a package manager however, it also creates and manages the environments that packages are installed in to. The use of environments to isolate software means you can have multiple versions of the same software installed in different environments and avoid conflicts or incompatibilities between software or dependencies. This is accomplished by installing packages into a separate directory which is then appended to your `PATH` when that environment is activated.

The next couple of pages will provide a brief introduction on how to use Conda to create and maintain locally administered environments on the CARC machines. 

For more information on the usage and various features of Conda, please visit their website at this [link](https://conda.io/docs/).

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/anaconda_general_intro.md) (last source update 2020-01-28). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes).</p>
