# Cloudera Data Science Workbench demos
Simple demonstrations of Cloudera Data Science Workbench.

1. Basic Python visualizations
2. R on Spark via Sparklyr
3. Tensorflow

## To setup (first run only):
1. In a Python Session:
```Python
! pip install pandas_highcharts tensorflow
```

2. In an R Session:
```R
library("devtools")
devtools::install_github("rstudio/sparklyr")
install.packages("nycflights13")
install.packages("Lahman")
install.packages("mgcv")
```

3. Stop all sessions, then proceed.
