---
title: "Parallel MATLAB: profile setup and batch submission"
description: "Configure a cluster profile and submit parallel MATLAB jobs."
type: Guide
tags:
  - MATLAB
  - Parallel
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/Parallel%20MATLAB%20profile%20setup%20and%20batch%20submission.md"
    title: "UNM-CARC QuickBytes: Parallel MATLAB profile setup and batch submission.md"
    author: "team:unm-carc"
    last_modified: "2022-05-11T10:43:18-06:00"
---

# Parallel MATLAB: profile setup and batch submission

### Setting up the cluster profile
In order to submit a batch script that takes advantage of MATLAB Parallel Server you first need to set up a cluster profile. Thankfully this has already been done and all you need to do as a user is import the profile and that only needs to be done once. If you would like to do this interactively you can start an interactive session with the following:

```bash
hopper:~$ srun --pty bash
```
Once you have a node allocated to you load the MATLAB module and start a MATLAB session:

```bash
wheeler001:~$ module load matlab
wheeler001:~$ matlab

To get started, type doc.
For product information, visit www.mathworks.com.
>>
```
Now simply import the cluster profile available in the root MATLAB folder:

```
>> profile = parallel.importProfile('/opt/local/MATLAB/<cluster>-normal.settings')
```
With the settings imported you can now launch parallel pools for computation using the imported cluster profile. The code below is an example to test parallel computing across two nodes while timing execution:

```
>> poolobj = parpool(profile, 16)
>> tic
>> n = 200
>> A = 500
>> a = zeros(1,n)
>> parfor i = 1:n
>> a(i) = max(abs(eig(rand(A))))
>> end % You may need to hit enter more than once to get the prompt back.
>> toc
>> delete(poolobj);
```
Even better is to do everything using a batch script and avoid the mistakes associated with interactive computing. Below is an example MATLAB script named `parallel_matlab.m` that will import our cluster profile and compare the time of computation for a sequential for loop and a parallel for loop with 16 cores ('workers' in MATLAB speak):

```
profile = parallel.importProfile('/opt/local/MATLAB/<cluster>-normal.settings')

poolobj = parpool(profile, 16);

tic
n = 200;
A = 500;
a = zeros(1,n);
for i=1:n;
    a(i) = max(abs(eig(rand(A))))
end
toc

tic
n = 200;
A = 500;
a = zeros(1,n);
parfor i=1:n;
    a(i) = max(abs(eig(rand(A))))
end
toc
delete(poolobj);
```
Now the PBS script we will call `parallel_matlab.pbs` to submit your sample MATLAB program:

```
#!/bin/bash

#PBS -N parallel_matlab
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=8
#PBS -j oe

cd #PBS_O_WORKDIR

module load matlab/R2019a

matlab -r -nodisplay parallel_matlab > parallel_matlab.out
```
Submit your PBS script with `qsub parallel_matlab.pbs` and hopefully all goes swimmingly. If you require assistance with MATLAB parallel computing please send an email to help@carc.unm.edu.

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/Parallel%20MATLAB%20profile%20setup%20and%20batch%20submission.md){target=_blank} (last source update 2022-05-11). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes){target=_blank}.</p>
