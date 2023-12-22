#######################
# Command line config #
#######################
# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  method <- "percentage"
  n_types <- 15
  th_day <- 100
  perc <- 95
  def_season <- "natural"
  reduction <- FALSE
  red_level <- 0.90
  derivative <- 5
  man <- 11
  th_ma <- 5
  n_clinical <- 5
  window_clinical <- 7
  window_grains <- 5
  th_pollen <- 10
  th_sum <- 100
  type <- "none"
  interpolation <- TRUE
  int_method <- "lineal"
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--method") {
      method <- args[i + 1]
    } else if (args[i] == "--nTypes") {
      n_types <- as.numeric(args[i + 1])
    } else if (args[i] == "--thDay") {
      th_day <- as.numeric(args[i + 1])
    } else if (args[i] == "--perc") {
      perc <- as.numeric(args[i + 1])
    } else if (args[i] == "--defSeason") {
      def_season <- args[i + 1]
    } else if (args[i] == "--reduction") {
      reduction <- as.logical(args[i + 1])
    } else if (args[i] == "--redLevel") {
      red_level <- as.numeric(args[i + 1])
    } else if (args[i] == "--derivative") {
      derivative <- as.numeric(args[i + 1])
    } else if (args[i] == "--man") {
      man <- as.numeric(args[i + 1])
    } else if (args[i] == "--thMa") {
      th_ma <- as.numeric(args[i + 1])
    } else if (args[i] == "--nClinical") {
      n_clinical <- as.numeric(args[i + 1])
    } else if (args[i] == "--windowClinical") {
      window_clinical <- as.numeric(args[i + 1])
    } else if (args[i] == "--windowGrains") {
      window_grains <- as.numeric(args[i + 1])
    } else if (args[i] == "--thPollen") {
      th_pollen <- as.numeric(args[i + 1])
    } else if (args[i] == "--thSum") {
      th_sum <- as.numeric(args[i + 1])
    } else if (args[i] == "--type") {
      type <- args[i + 1]
    } else if (args[i] == "--interpolation") {
      interpolation <- as.logical(args[i + 1])
    } else if (args[i] == "--intMethod") {
      int_method <- args[i + 1]
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
      cat("   --method=CHARACTER         Method for calculating the pollen season\n")
      cat("   --nTypes=NUMERIC           Number of abundant pollen types in the calendar\n")
      cat("   --thDay=NUMERIC            Threshold for counting days when pollen level is exceeded\n")
      cat("   --perc=NUMERIC             Percentage of total annual pollen for pollen season\n")
      cat("   --defSeason=CHARACTER      Method for selecting annual period (natural, interannual, peak)\n")
      cat("   --reduction=LOGICAL        Reduce peaks in pollen data (only for logistic method)\n")
      cat("   --redLevel=NUMERIC         Percentile for reducing peaks (only for logistic method)\n")
      cat("   --derivative=NUMERIC       Derivative for logistic method\n")
      cat("   --man=NUMERIC              Order of moving average (only for moving method)\n")
      cat("   --thMa=NUMERIC             Threshold for moving method\n")
      cat("   --nClinical=NUMERIC        Number of days for clinical method\n")
      cat("   --windowClinical=NUMERIC   Time window for clinical method\n")
      cat("   --windowGrains=NUMERIC     Time window for grains method\n")
      cat("   --thPollen=NUMERIC         Threshold for clinical and grains methods\n")
      cat("   --thSum=NUMERIC            Pollen threshold for sum in clinical method\n")
      cat("   --type=CHARACTER           Pollen type for clinical method (birch, grasses, cypress, olive, ragweed)\n")
      cat("   --interpolation=LOGICAL    Apply interpolation to fill gaps (default: TRUE)\n")
      cat("   --intMethod=CHARACTER      Interpolation method (lineal, movingmean, spline, tseries)\n")
      cat("   --delimiter=CHARACTER      Dataframe delimiter\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER        Library for importing packages\n")
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

  # Read input file
  data <- readFile(input_file, delimiter)

  # Call the function iplot_pheno with the specified parameters
  iplot_pheno(
      data = data,
      method = method,
      n.types = n_types,
      th.day = th_day,
      perc = perc,
      def.season = def_season,
      reduction = reduction,
      red.level = red_level,
      derivative = derivative,
      man = man,
      th.ma = th_ma,
      n.clinical = n_clinical,
      window.clinical = window_clinical,
      window.grains = window_grains,
      th.pollen = th_pollen,
      th.sum = th_sum,
      type = type,
      interpolation = interpolation,
      int.method = int_method,
      export.plot = TRUE)

  # List files that match the pattern
  pdf_files <- list.files(path = "./plot_AeRobiology/", pattern = "pheno_plot.*\\.pdf", full.names = TRUE)

  # Check if there are files to copy
  if (length(pdf_files) == 1) {
    file.copy(pdf_files[1], paste0(output_folder, "output.pdf"), overwrite = TRUE)
    file.remove(pdf_files[1])
  } else {
    print("No files matching the pattern were found.")
  }
}