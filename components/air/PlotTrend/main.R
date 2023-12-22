#######################
# Command line config #
#######################
# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input <- NULL
  interpolation <- TRUE
  int_method <- "lineal"
  export_plot <- TRUE
  export_format <- "pdf"
  export_result <- TRUE
  method <- "percentage"
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input <- args[i + 1]
    } else if (args[i] == "--interpolation") {
      interpolation <- as.logical(args[i + 1])
    } else if (args[i] == "--intMethod") {
      int_method <- args[i + 1]
    } else if (args[i] == "--method") {
      method <- args[i + 1]
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
      cat("   --filepath=CHARACTER       Input file path\n")
      cat("   --interpolation=LOGICAL    Apply interpolation to fill gaps (default: TRUE)\n")
      cat("   --intMethod=CHARACTER      Interpolation method (lineal, movingmean, spline, tseries)\n")
      cat("   --method=CHARACTER         Method for calculating the pollen season\n")
      cat("   --delimiter=CHARACTER      Dataframe delimiter\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER        Library for importing packages\n")
      # Quit the script
      quit(status = 0)
    }
  }

  # Check if file path is missing
  if (is.null(input)) {
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

  # Read input file
  data <- readFile(input, delimiter)

  # Call the function plot_trend with the specified parameters
  plot_trend(
    data = data,
    interpolation = interpolation,
    int.method = int_method,
    export.plot = TRUE,
    export.format = "pdf",
    export.result = TRUE,
    method = method
  )

  # List files that match the pattern
  pdf_files <- list.files(path = "./plot_AeRobiology/trend_plots", pattern = "plot_trend_.*\\.pdf", full.names = TRUE)

  # Check if there are files to zip
  if (length(pdf_files) > 0) {
    zip(zipfile = paste0(output_folder, "output"), files = pdf_files)
    unlink("plot_AeRobiology", recursive = TRUE)
  } else {
    print("No files matching the pattern were found.")
  }

  # Copy the xlsx file
  xslx_output <- "./table_AeRobiology/summary_of_plot_trend.xlsx"
  file.copy(xslx_output, paste0(output_folder, "output.xlsx"), overwrite = TRUE)
  file.remove(xslx_output)
}
