#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  method <- NULL
  th_day <- 100
  perc <- 95
  def_season <- "natural"
  reduction <- FALSE
  red_level <- 0.9
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
  max_days <- 30
  result <- "table"
  plot <- TRUE
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--method") {
      method <- args[i + 1]
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
    } else if (args[i] == "--maxDays") {
      max_days <- as.numeric(args[i + 1])
    } else if (args[i] == "--result") {
      result <- args[i + 1]
    } else if (args[i] == "--plot") {
      plot <- as.logical(args[i + 1])
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
      cat("   --filepath=CHARACTER     Input file path\n")
      cat("   --method=CHARACTER       Method applied to calculate the pollen season and parameters (options: percentage, logistic, moving, clinical or grains)\n")
      cat("   --thDay=INTEGER           Number of days for pollen concentration calculation (default: 100)\n")
      cat("   --perc=DOUBLE             Percentage of total annual pollen for 'percentage' method (default: 95)\n")
      cat("   --defSeason=CHARACTER     Method for selecting the best annual period (options: natural, interannual or peak, default: natural)\n")
      cat("   --reduction=LOGICAL       Reduction of pollen data for 'logistic' method (default: FALSE)\n")
      cat("   --redLevel=DOUBLE         Percentile level for 'logistic' method (default: 0.9)\n")
      cat("   --derivative=INTEGER      Derivative for 'logistic' method (options: 4, 5 or 6, default: 5)\n")
      cat("   --man=INTEGER             Order of moving average for 'moving' method (default: 11)\n")
      cat("   --thMa=DOUBLE             Threshold for 'moving' method (default: 5)\n")
      cat("   --nClinical=INTEGER       Number of days for 'clinical' method (default: 5)\n")
      cat("   --windowClinical=INTEGER  Time window for 'clinical' method (default: 7)\n")
      cat("   --windowGrains=INTEGER    Time window for 'grains' method (default: 5)\n")
      cat("   --thPollen=DOUBLE         Threshold for 'clinical' or 'grains' methods (default: 10)\n")
      cat("   --thSum=DOUBLE            Pollen threshold for 'clinical' method (default: 100)\n")
      cat("   --type=CHARACTER          Pollen type for 'clinical' method (options: birch, grasses, cypress, olive, ragweed or none, default: none)\n")
      cat("   --interpolation=LOGICAL   Interpolation of pollen data (default: TRUE)\n")
      cat("   --intMethod=CHARACTER     Interpolation method (options: lineal, movingmean, spline or tseries, default: lineal)\n")
      cat("   --maxDays=INTEGER         Maximum consecutive days for interpolation (default: 30)\n")
      cat("   --result=CHARACTER        Output format (options: table or list, default: table)\n")
      cat("   --plot=LOGICAL            Show graphical results (default: TRUE)\n")
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

  # Check if method is missing
  if (is.null(method)) {
    stop("Error: argument --method is mandatory")
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

  # Calculate main parameters of the pollen season
  calculate_ps(
    data = data,
    method = method,
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
    maxdays = max_days,
    result = result,
    plot = plot,
    export.plot = TRUE,
    export.result = TRUE
  )

  # Copy the plot file
  pdf_output <- "./Rplots.pdf"
  dev.off()
  file.copy(pdf_output, paste0(output_folder, "output.pdf"), overwrite = TRUE)
  file.remove(pdf_output)

  # List files that match the pattern
  pdf_files <- list.files(path = "./table_AeRobiology/", pattern = "table_ps_.*\\.xlsx", full.names = TRUE)

  # Check if there are files to copy
  if (length(pdf_files) == 1) {
    file.copy(pdf_files[1], paste0(output_folder, "output.xlsx"), overwrite = TRUE)
    file.remove(pdf_files[1])
  } else {
    print("No files matching the pattern were found.")
  }
}