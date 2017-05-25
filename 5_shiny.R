# This demo shows how we can use `shiny` to provide an interactive experience to our users

# Load the libraries
suppressPackageStartupMessages(library('cdsw'))
suppressPackageStartupMessages(library('shiny'))
suppressPackageStartupMessages(library('parallel'))

# Now start the Shiny server. Shiny blocks the R process it runs in, so use the parallel 
# package to run it in a separate process.

mcparallel(runApp(host="0.0.0.0", port=8080, launch.browser=FALSE,
    appDir="/home/cdsw", display.mode="auto"))

# Finally, create an IFrame widget in the console and point it at the Shiny server.

service.url <- paste("http://", Sys.getenv("CDSW_ENGINE_ID"), ".", 
Sys.getenv("CDSW_DOMAIN"), sep="") 
Sys.sleep(5)
iframe(src=service.url, width="640px", height="480px")
