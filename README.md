# Cloudera Data Science Workbench demos
Basic tour of Cloudera Data Science Workbench.

NOTE THAT A WORKAROUND IS REQUIRED UNTIL CDSW 1.1.0 ... 

## WORKAROUND
Do NOT setup this project using CDSW's git mechanism. Instead: 
+ Create a BLANK project
+ Start a session
+ Start a terminal
+ In the terminal execute the following:
```sh
git clone https://github.com/TobyHFerguson/cdsw-demo-short
```
This will create a directory called `cdsw-demo-short`

Go into your workbench and, on the left hand side, hit the 'refresh circle' to sync the workbench with the updated filesystem. You'll now see all your files listed in the workbench. 

## Workbench
There are 4 scripts provided which walk through the interactive capabilities of Cloudera Data Science Workbench.

1. **Basic Python visualizations (Python 2).** Demonstrates:
  - Markdown via comments
  - Jupyter-compatible visualizations
  - Simple console sharing
2. **PySpark (Python 2).** Demonstrates:
  - Easy connectivity to (kerberized) Spark in YARN client mode.
  - Access to Hadoop HDFS CLI (e.g. `hdfs dfs -ls /`).
3. **Tensorflow (Python 2).** Demonstrates:
  - Ability to install and use custom packages (e.g. `pip search tensorflow`)
4. **R on Spark via Sparklyr (R).** Demonstrates:
  - Use familiar dplyr with Spark using [Sparklyr](http://spark.rstudio.com)
  - *Note: Be sure to run `4a.R` first to create your Spark session!*

## Jobs
We recommend setting up a **"Nightly Analysis"** job to illustrate how data scientists can easily automate their projects.


## Setup instructions
Note: You only need to do this once.

1. In a Python Session:
```Python
! pip install -r /home/cdsw/cdsw-demo-short/requirements.txt
```
*Close* this python session and open a new one (this is to workaround a bug in
the tensorflow libraries)

2. In an R Session:
```R
library("devtools")
devtools::install_github('rstudio/sparklyr')
install.packages('plotly')
install.packages("nycflights13")
install.packages("Lahman")
install.packages("mgcv")
```

3. Stop all sessions, then proceed.

4. WORKAROUND 
