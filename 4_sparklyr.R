## Connecting to Spark

library(sparklyr)
library(dplyr)

system.time(sc <- spark_connect(master = "yarn-client"))

# The returned Spark connection (sc) provides a remote dplyr data source to the Spark cluster.

## Reading Data
library(dplyr)
flights_tbl <- copy_to(sc, nycflights13::flights, "flights", overwrite = TRUE)
# The returned Spark connection (sc) provides a remote dplyr data source to the Spark cluster.
sc

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

# # Plot delays
library(ggplot2)
ggplot(delay, aes(dist, delay)) +
  geom_point(aes(size = count), alpha = 1/2) +
  geom_smooth() +
  scale_size_area(max_size = 2)

## Machine Learning
# You can orchestrate machine learning algorithms in a Spark cluster via the machine learning functions within sparklyr. These functions connect to a set of high-level APIs built on top of DataFrames that help you create and tune machine learning workflows.

# In this example we’ll use ml_linear_regression to fit a linear regression model. We’ll use the built-in mtcars dataset, and see if we can predict a car’s fuel consumption (mpg) based on its weight (wt) and the number of cylinders the engine contains (cyl). We’ll assume in each case that the relationship between mpg and each of our features is linear.

# copy mtcars into spark
mtcars_tbl <- copy_to(sc, mtcars, overwrite = TRUE)

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

# You can disconnect from Spark using the spark_disconnect function:
spark_disconnect(sc)