---
title: "Gurobi optimizer with R"
description: "Use the Gurobi optimization solver from R on CARC clusters."
type: Guide
tags:
  - R
  - Optimization
generated:
  by: "claude/fable-5"
  at: "2026-08-29T00:00:00Z"
sources:
  - id: quickbytes
    resource: "https://github.com/UNM-CARC/QuickBytes/blob/master/Gurobi%20optimizer%20with%20R.md"
    title: "UNM-CARC QuickBytes: Gurobi optimizer with R.md"
    author: "team:unm-carc"
    last_modified: "2021-02-17T14:09:22-07:00"
---

# Gurobi optimizer with R

[Gurobi optimizer](https://www.gurobi.com/products/gurobi-optimizer/){target=_blank} is a problem solving software that can be used within R. It can solve integer, linear, and quadratic
programming optimizations. These techniques can help to find the answers to complex models. 


## Example of running Gurobi optimizer with R at CARC

There are modules for both Gurobi and R on the CARC clusters. All you need to do is load them, and then start an R
session. This command is for version 8.1.0, however there are other versions of gurobi available (enter `module avail gurobi` to see a full list).
```
username@hopper:~$ module load gurobi/8.1.0
username@hopper:~$ module load r-3.6.0-gcc-7.3.0-python2-7akol5t
username@hopper:~$ R
```
Once you have started an R session, you can install packages just as you would in R. If you ever run into issues loading 
packages in R at CARC, you can reach out for assistance by emailling help@carc.unm.edu. One piece of advice if you are using 
JupyterHub to run an R notebook at CARC is you may need to install packages from ther terminal window on JupyterHub because 
the notebook will not let you interactiively answer questions installs may need. 

Start by installing the gurobi package:
```
> install.packages('/opt/local/gurobi/8.1.0/linux64/R/gurobi_8.1-0_R_3.5.0.tar.gz')
Installing package into '/users/username/R/x86_64-pc-linux-gnu-library/3.6'
* installing *binary* package 'gurobi' ...
* DONE (gurobi)
```
You should now be able to load the gurobi library in an R session:
```
> library(gurobi)
Loading required package: slam
```
Note that if you get an error regarding slam, you can install it using the command:
```
install.packages("slam", repos = "https://cloud.r-project.org")
```
Now let's runs a quick model as an example of what Gurobi can do and to see if everything is working properly: 
```
> model <- list()
> model$A          <- matrix(c(1,2,3,1,1,0), nrow=2, ncol=3, byrow=T)
> model$obj        <- c(1,1,2)
> model$modelsense <- 'max'
> model$rhs        <- c(4,1)
> model$sense      <- c('<', '>')
> model$vtype      <- 'B'
> params <- list(OutputFlag=0)
> result <- gurobi(model, params)
> print('Solution:')
[1] "Solution:"
> print(result$objval)
[1] 3
> print(result$x)
[1] 1 0 1
```

<p class="carc-provenance" markdown>Migrated from [UNM-CARC QuickBytes](https://github.com/UNM-CARC/QuickBytes/blob/master/Gurobi%20optimizer%20with%20R.md){target=_blank} (last source update 2021-02-17). Spotted a problem? [Open an issue or pull request](https://github.com/UNM-CARC/QuickBytes){target=_blank}.</p>
