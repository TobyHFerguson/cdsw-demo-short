# Contents courtesy of http://spark.rstudio.com/

## Connecting to Spark

library(sparklyr)
system.time(sc <- spark_connect(master = "yarn-client"))

# The returned Spark connection (sc) provides a remote dplyr data source to the Spark cluster.

## Reading Data
library(dplyr)
flights_tbl <- copy_to(sc, nycflights13::flights, "flights", overwrite = TRUE)