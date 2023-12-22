#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  method <- "heatplot"
  n_types <- 15
  start_month <- 1
  y_start <- NULL
  y_end <- NULL
  perc1 <- 80
  perc2 <- 99
  th_pollen <- 1
  average_method <- "avg_before"
  period <- "daily"
  method_classes <- "exponential"
  n_classes <- 5
  classes <- c(25, 50, 100, 300)
  color <- "green"
  interpolation <- TRUE
  int_method <- "lineal"
  na_remove <- TRUE
  result <- "plot"
  legend_name <- "Pollen / m3"
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
    } else if (args[i] == "--startMonth") {
      start_month <- as.numeric(args[i + 1])
    } else if (args[i] == "--yStart" && args[i + 1] != "None" && args[i + 1] != "") {
      y_start <- as.numeric(args[i + 1])
    } else if (args[i] == "--yEnd" && args[i + 1] != "None" && args[i + 1] != "") {
      y_end <- as.numeric(args[i + 1])
    } else if (args[i] == "--perc1") {
      perc1 <- as.numeric(args[i + 1])
    } else if (args[i] == "--perc2") {
      perc2 <- as.numeric(args[i + 1])
    } else if (args[i] == "--thPollen") {
      th_pollen <- as.numeric(args[i + 1])
    } else if (args[i] == "--averageMethod") {
      average_method <- args[i + 1]
    } else if (args[i] == "--period") {
      period <- args[i + 1]
    } else if (args[i] == "--methodClasses") {
      method_classes <- args[i + 1]
    } else if (args[i] == "--nClasses") {
      n_classes <- as.numeric(args[i + 1])
    } else if (args[i] == "--classes") {
      classes <- as.numeric(unlist(strsplit(args[i + 1], ",")))
    } else if (args[i] == "--color") {
      color <- args[i + 1]
    } else if (args[i] == "--interpolation") {
      interpolation <- as.logical(args[i + 1])
    } else if (args[i] == "--intMethod") {
      int_method <- args[i + 1]
    } else if (args[i] == "--naRemove") {
      na_remove <- as.logical(args[i + 1])
    } else if (args[i] == "--result") {
      result <- args[i + 1]
    } else if (args[i] == "--legendName") {
      legend_name <- args[i + 1]
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
      cat("   --method=CHARACTER         Method to calculate and generate the pollen calendar (options: heatplot, violinplot or phenological, default: heatplot)\n")
      cat("   --nTypes=INTEGER           Number of most abundant pollen types to be represented in the pollen calendar (default: 15)\n")
      cat("   --startMonth=INTEGER        Month (1-12) when the pollen calendar starts (default: 1)\n")
      cat("   --yStart=INTEGER           Start year for the pollen calendar (default: NULL)\n")
      cat("   --yEnd=INTEGER             End year for the pollen calendar (default: NULL)\n")
      cat("   --perc1=DOUBLE             Percentage (0-100) for main pollination period (default: 80)\n")
      cat("   --perc2=DOUBLE             Percentage (0-100) for early/late pollination period (default: 99)\n")
      cat("   --thPollen=DOUBLE          Minimum threshold of average pollen concentration (default: 1)\n")
      cat("   --averageMethod=CHARACTER  Moment of the application of the average (options: avg_before or avg_after, default: avg_before)\n")
      cat("   --period=CHARACTER         Interval time for the pollen calendar (options: daily or weekly, default: daily)\n")
      cat("   --methodClasses=CHARACTER  Method to define classes for classifying average pollen concentrations (default: exponential)\n")
      cat("   --nClasses=INTEGER         Number of classes for classifying average pollen concentrations (default: 5)\n")
      cat("   --classes=CHARACTER        Thresholds for defining different classes (comma-separated)\n")
      cat("   --color=CHARACTER          Color palette for the pollen calendar plot (options: green, red, blue, purple or black, default: green)\n")
      cat("   --interpolation=LOGICAL    Apply interpolation to complete gaps in the pollen data (default: TRUE)\n")
      cat("   --intMethod=CHARACTER      Interpolation method (options: lineal, movingmean, spline or tseries, default: lineal)\n")
      cat("   --naRemove=LOGICAL         Remove NA values for the pollen calendar (default: TRUE)\n")
      cat("   --result=CHARACTER         Output type for the function (options: plot or table, default: plot)\n")
      cat("   --legendName=CHARACTER     Title of the legend in the plot (default: Pollen / m3)\n")
      cat("   --delimiter=CHARACTER      Dataframe delimiter (default: ,)\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER        Library from which to import the packages (default: NULL)\n")
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

  # Call the function pollen_calendar with the specified parameters
  pollen_calendar(data = data,
                  method = method,
                  n.types = n_types,
                  start.month = start_month,
                  y.start = y_start,
                  y.end = y_end,
                  perc1 = perc1,
                  perc2 = perc2,
                  th.pollen = th_pollen,
                  average.method = average_method,
                  period = period,
                  method.classes = method_classes,
                  n.classes = n_classes,
                  classes = classes,
                  color = color,
                  interpolation = interpolation,
                  int.method = int_method,
                  na.remove = na_remove,
                  result = result,
                  export.plot = TRUE,
                  legendname = legend_name)

  # Copy the plot file
  pdf_output <- paste0("./plot_AeRobiology/pollen_calendar_", method, ".pdf")
  file.copy(pdf_output, paste0(output_folder, "output.pdf"), overwrite = TRUE)
  file.remove(pdf_output)
}