# Contents courtesy of http://spark.rstudio.com/

## Installation
# Due to a patch that's not yet in the official CRAN build, install Sparklyr from Github:

# ```
# library("devtools")
# devtools::install_github("rstudio/sparklyr")
# ```

## Connecting to Spark
# You can connect to both local instances of Spark as well as remote Spark clusters. Here we’ll connect to an existing Spark cluster in YARN client mode via the spark_connect function:

library(sparklyr)
system.time(sc <- spark_connect(master = "yarn-client"))

# The returned Spark connection (sc) provides a remote dplyr data source to the Spark cluster.

## Reading Data
# You can copy R data frames into Spark using the dplyr copy_to function (more typically though you’ll read data within the Spark cluster using the spark_read family of functions). For the examples below we’ll copy some datasets from R into Spark (note that you may need to install the nycflights13 and Lahman packages in order to execute this code):

# ```
# # If needed, install the sample data sets:
# install.packages("nycflights13")
# install.packages("Lahman")
# install.packages("mgcv")
# ```

library(dplyr)
iris_tbl <- copy_to(sc, iris, overwrite = TRUE)
flights_tbl <- copy_to(sc, nycflights13::flights, "flights", overwrite = TRUE)
batting_tbl <- copy_to(sc, Lahman::Batting, "batting", overwrite = TRUE)

# You can list all of the available tables (including those that were already pre-loaded within the cluster) using the dplyr src_tbls function:

src_tbls(sc)

## Using dplyr
# We can now use all of the available dplyr verbs against the tables within the cluster. Here’s a simple filtering example:

# # filter by departure delay
flights_tbl %>% filter(dep_delay == 2)

# Introduction to dplyr provides additional dplyr examples you can try. For example, consider the last example from the tutorial which plots data on flight delays:
delay <- flights_tbl %>% 
  group_by(tailnum) %>%
  summarise(count = n(), dist = mean(distance), delay = mean(arr_delay)) %>%
  filter(count > 20, dist < 2000, !is.na(delay)) %>%
  collect()

# plot delays
library(ggplot2)
ggplot(delay, aes(dist, delay)) +
  geom_point(aes(size = count), alpha = 1/2) +
  geom_smooth() +
  scale_size_area(max_size = 2)

## Window Functions
# dplyr window functions are also supported, for example:

batting_tbl %>%
  select(playerID, yearID, teamID, G, AB:H) %>%
  arrange(playerID, yearID, teamID) %>%
  group_by(playerID) %>%
  filter(min_rank(desc(H)) <= 2 & H > 0)

## Using SQL
# It’s also possible to execute SQL queries directly against tables within a Spark cluster. The spark_connection object implements a DBI interface for Spark, so you can use dbGetQuery to execute SQL and return the result as an R data frame:

library(DBI)
iris_preview <- dbGetQuery(sc, "SELECT * FROM iris LIMIT 10")
iris_preview

## Machine Learning
# You can orchestrate machine learning algorithms in a Spark cluster via the machine learning functions within sparklyr. These functions connect to a set of high-level APIs built on top of DataFrames that help you create and tune machine learning workflows.

# In this example we’ll use ml_linear_regression to fit a linear regression model. We’ll use the built-in mtcars dataset, and see if we can predict a car’s fuel consumption (mpg) based on its weight (wt) and the number of cylinders the engine contains (cyl). We’ll assume in each case that the relationship between mpg and each of our features is linear.

# copy mtcars into spark
mtcars_tbl <- copy_to(sc, mtcars)

# transform our data set, and then partition into 'training', 'test'
partitions <- mtcars_tbl %>%
  filter(hp >= 100) %>%
  mutate(cyl8 = cyl == 8) %>%
  sdf_partition(training = 0.5, test = 0.5, seed = 1099)

# fit a linear model to the training dataset
fit <- partitions$training %>%
  ml_linear_regression(response = "mpg", features = c("wt", "cyl"))

# For linear regression models produced by Spark, we can use summary() to learn a bit more about the quality of our fit, and the statistical significance of each of our predictors.

summary(fit)

### Connection Tools
# You can view the Spark web UI via the spark_web function, and view the Spark log via the spark_log function:

spark_web(sc)
spark_log(sc)

# You can disconnect from Spark using the spark_disconnect function:
spark_disconnect(sc)