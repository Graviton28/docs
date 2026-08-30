---
title: "ORCA quantum chemistry"
description: "Run ORCA quantum chemistry calculations in parallel on CARC clusters."
type: Tutorial
tags:
  - Chemistry
status: draft
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/orca_wheeler_taos.md"
    title: "UNM-CARC QuickBytes: orca_wheeler_taos.md"
    author: "team:unm-carc"
    last_modified: "2020-07-15T06:51:46-06:00"
---

# ORCA quantum chemistry

### Submitting an Orca batch script

CARC clusters use Slurm (**S**imple **L**inux **U**tility for **R**esource **M**anagement) to submit jobs and manage resources. Slurm provides greater control over resource management and utilization which means one has to be more explicit in their submission script. Specifically, it is necessary to request sufficient memory for your task when submitting your job. Below is a sample script for submitting an Orca job named `orca_submission.sh`:

```bash
#!/usr/bin/bash

## Set your slurm flags here requesting resources.
#SBATCH --job-name=orca_test
#SBATCH --output=test.out
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
## This depends on which queue you have access to.
#SBATCH --partition=my_partition
#SBATCH --mem-per-cpu=6GB
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-type=fail         # send email if job fails
#SBATCH --mail-user=<YourNetID>@unm.edu

module load openmpi-3.1.5-gcc-5.4.0-f6ikvl6
module load orca/4.2.1

## Set your input and output file names
input_file=my_orca_input.inp
output_file=my_orca_output.log
prefix=$(echo $input_file | cut -f1 -d".")

# Set the scratch directory path
scratch_dir=/carc/scratch/$USER/

# Set the input and output paths on the scratch file system
mkdir $scratch_dir$prefix
TEMP_DIR=$scratch_dir$prefix
output_scratch_path=$TEMP_DIR/$output_file
input_scratch_path=$TEMP_DIR/$input_file

# Create directory for additional files
mkdir $SLURM_SUBMIT_DIR/$prefix
add_files_dir=$SLURM_SUBMIT_DIR/$prefix

# Copy the input file from the submission directory to the scratch directory
cp $SLURM_SUBMIT_DIR/$input_file $TEMP_DIR/

# Orca needs the full path when running in parallel
full_orca_path=$(which orca)

# Run Orca
$full_orca_path $input_scratch_path > $output_scratch_path

# Orca finished so copy the output file on scratch to the submission directory and clean the scratch directory
cp $output_scratch_path $SLURM_SUBMIT_DIR/$output_file
cp $TEMP_DIR/$prefix* $add_files_dir
rm $TEMP_DIR
```
Now you can simply submit your job to the queue with `sbatch orca_submission.sh`.

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/orca_wheeler_taos.md){target=_blank} (last source update 2020-07-15). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes){target=_blank}.</p>
