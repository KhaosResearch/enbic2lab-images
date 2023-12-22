#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  n_types <- 15
  y_start <- NULL
  y_end <- NULL
  interpolation <- TRUE
  int_method <- "lineal"
  col_bar <- "#E69F00"
  exclude <- ""
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--nTypes") {
      n_types <- as.numeric(args[i + 1])
    } else if (args[i] == "--yStart" && args[i + 1] != "None" && args[i + 1] != "") {
      y_start <- as.numeric(args[i + 1])
    } else if (args[i] == "--yEnd" && args[i + 1] != "None" && args[i + 1] != "") {
      y_end <- as.numeric(args[i + 1])
    } else if (args[i] == "--interpolation") {
      interpolation <- as.logical(args[i + 1])
    } else if (args[i] == "--intMethod") {
      int_method <- args[i + 1]
    } else if (args[i] == "--colBar") {
      col_bar <- args[i + 1]
    } else if (args[i] == "--exclude") {
      exclude <- as.character(unlist(strsplit(args[i + 1], ",")))
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
      cat("   --filepath=CHARACTER      Input file name\n")
      cat("   --nTypes=NUMERIC          Number of most abundant pollen types to be represented in the plot of the relative abundance (default: 15)\n")
      cat("   --yStart=NUMERIC          Start year for calculating relative abundances of pollen types (default: NULL)\n")
      cat("   --yEnd=NUMERIC            End year for calculating relative abundances of pollen types (default: NULL)\n")
      cat("   --interpolation=LOGICAL   Apply interpolation to complete gaps with no data (default: TRUE)\n")
      cat("   --intMethod=CHARACTER     Interpolation method (options: lineal, movingmean, spline or tseries, default: lineal)\n")
      cat("   --colBar=CHARACTER        Color of the bars for the plot (default: #E69F00)\n")
      cat("   --exclude=CHARACTER       Names of pollen types to be excluded from the plot\n")
      cat("   --delimiter=CHARACTER     Dataframe delimiter (default: ,)\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER       Library from which to import the packages (default: NULL)\n")
      # Quit the script
      quit(status = 0)
    }
  }

  # Check if input file is missing
  if (is.null(input_file)) {
    stop("Error: argument --filepath is mandatory")
  }

  # Check if y_start and y_end are valid
  if (is.numeric(y_start) && is.numeric(y_end) && y_end < y_start) {
    stop("y_start must be lower than y_end")
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
  data <- readFile(input_file, delimiter)

  # Call the function iplot_abundance with the specified parameters
  iplot_abundance(data = data,
                n.types = n_types,
                y.start = y_start,
                y.end = y_end,
                interpolation = interpolation,
                int.method = int_method,
                col.bar = col_bar,
                export.plot = TRUE,
                exclude = exclude
                )

  # List files that match the pattern
  pdf_files <- list.files(path = "./plot_AeRobiology/", pattern = "abundance_plot.*\\.pdf", full.names = TRUE)

  # Check if there are files to copy
  if (length(pdf_files) == 1) {
    file.copy(pdf_files[1], paste0(output_folder, "output.pdf"), overwrite = TRUE)
    file.remove(pdf_files[1])
  } else {
    print("No files matching the pattern were found.")
  }
}
