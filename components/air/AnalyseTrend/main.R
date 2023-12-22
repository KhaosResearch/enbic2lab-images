#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  file_path <- NULL
  interpolation <- TRUE
  int_method <- "lineal"
  method <- "percentage"
  quantil <- 0.75
  significant <- 0.05
  split <- TRUE
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--interpolation") {
      interpolation <- as.logical(args[i + 1])
    } else if (args[i] == "--intMethod") {
      int_method <- args[i + 1]
    } else if (args[i] == "--method") {
      method <- args[i + 1]
    } else if (args[i] == "--quantil") {
      quantil <- as.numeric(args[i + 1])
    } else if (args[i] == "--significant") {
      significant <- as.numeric(args[i + 1])
    } else if (args[i] == "--split") {
      split <- as.logical(args[i + 1])
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
      cat("   --filepath=CHARACTER      Input file path\n")
      cat("   --interpolation=LOGICAL   Apply interpolation to fill gaps in data (default: TRUE)\n")
      cat("   --intMethod=CHARACTER     Interpolation method (options: lineal, movingmean, tseries or spline, default: lineal)\n")
      cat("   --method=CHARACTER        Method for calculating pollen season (options: percentage, logistic, moving, clinical or grains, default: percentage)\n")
      cat("   --quantil=NUMERIC         Quantile of data to display (between 0 and 1, default: 0.75)\n")
      cat("   --significant=NUMERIC     Significance level for linear trends analysis (default: 0.05)\n")
      cat("   --split=LOGICAL           Split the plot based on variable nature (default: TRUE)\n")
      cat("   --delimiter=CHARACTER     Dataframe delimiter (default: ,)\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER       Library from which to import packages (default: NULL)\n")
      # Quit the script
      quit(status = 0)
    }
  }

  # Check if file path is missing
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

  # Call the function analyse_trend with the specified parameters
  analyse_trend(data = data,
              interpolation = interpolation,
              int.method = int_method,
              method = method,
              significant = significant,
              split = split,
              export.plot = TRUE,
              export.result = TRUE)

  # Copy the plot file 
  pdf_output <- "./plot_AeRobiology/analyse_trend_split.pdf"
  dev.off()
  file.copy(pdf_output, paste0(output_folder, "output.pdf"), overwrite = TRUE)
  file.remove(pdf_output)

  # Copy the result file
  xslx_output <- "./table_AeRobiology/summary_of_trends.xlsx"
  file.copy(xslx_output, paste0(output_folder, "output.xlsx"), overwrite = TRUE)
  file.remove(xslx_output)
}
