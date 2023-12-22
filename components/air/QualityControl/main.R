#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  window <- 2
  perc_miss <- 20
  ps_method <- "percentage"
  perc <- 95
  result <- "plot"
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--window") {
      window <- as.numeric(args[i + 1])
    } else if (args[i] == "--perc_miss") {
      perc_miss <- as.numeric(args[i + 1])
    } else if (args[i] == "--ps_method") {
      ps_method <- args[i + 1]
    } else if (args[i] == "--perc") {
      perc <- as.numeric(args[i + 1])
    } else if (args[i] == "--result") {
      result <- args[i + 1]
    } else if (args[i] == "--delimiter") {
      delimiter <- args[i + 1]
    } else if (args[i] == "--output-folder") {
      output_folder <- args[i + 1]
    } else if (args[i] == "--library") {
      lib <- args[i + 1]
    } else if (args[i] == "--help") {
      # Print usage information
      cat("Usage: Rscript main.R [options]\n")
      cat("\n")
      cat("Options:\n")
      cat("   --filepath=CHARACTER   Input file path\n")
      cat("   --window=INTEGER       A numeric (integer) value bigger or equal to 1 (default: 2)\n")
      cat("   --perc_miss=INTEGER    A numeric (integer) value between 0 and 100 (default: 20)\n")
      cat("   --ps_method=CHARACTER  A character string specifying the method applied to calculate the pollen season (default: 'percentage')\n")
      cat("   --perc=INTEGER         A numeric (integer) value between 0 and 100 (default: 95)\n")
      cat("   --result=CHARACTER     A character string specifying the format of the results (table or plot, default: 'plot')\n")
      cat("   --delimiter=CHARACTER  Dataframe delimiter (default: ,)\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER    Library from which to import the packages (default: NULL)\n")
      # Quit the script
      quit(status = 0)
    }
  }

  # Check if input file is missing
  if (is.null(input_file)) {
    stop("Error: argument --filepath is mandatory")
  }
}

##################
# load libraries #
##################

# Check that the script is not being tested
if (!exists("test")) {
  if (!is.null(lib)) .libPaths(lib)
  library(AeRobiology)
  library(ggplot2)
}


#############
# Functions #
#############

# Reads a CSV file and converts the date column to a Date object
# Arguments:
#   file: The path to the CSV file
#   delimiter: The delimiter used in the CSV file
# Returns:
#   A data frame with the contents of the CSV file, where the date column has been converted to a Date object
readFile <- function(file, delimiter) {
  data <- read.csv(file, sep = delimiter)
  data$date <- as.Date(data$date)

  return(data)
}


########
# MAIN #
########

# Check that the script is not being tested
if (!exists("test")) {

  # Read the input file
  data <- readFile(input_file, delimiter)

  # Create a PDF document
  pdf(paste0(output_folder, "output.pdf")) 

  # Perform quality control on the data
  qc <- quality_control(data = data,
                        int.window = window,
                        perc.miss = perc_miss,
                        ps.method = ps_method,
                        perc = perc,
                        result = result)

  # Plot the quality control results
  plot(qc)

  # Close the PDF document
  dev.off()  

  # Extract the plot data from the quality control object
  pg <- ggplot_build(qc)

  # Write the plot data to a CSV file
  write.csv(pg$plot$data, paste0(output_folder, "output.csv"))
}