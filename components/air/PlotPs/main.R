#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  pollen_type <- NULL
  year <- NULL
  days <- 30
  fil_col <- "turquoise4"
  axisname <- "Pollen grains / m ^ 3"
  int_method <- "lineal"
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--pollenType") {
      pollen_type <- args[i + 1]
    } else if (args[i] == "--year") {
      year <- as.numeric(args[i + 1])
    } else if (args[i] == "--days") {
      days <- as.numeric(args[i + 1])
    } else if (args[i] == "--filCol") {
      fil_col <- args[i + 1]
    } else if (args[i] == "--axisname") {
      axisname <- args[i + 1]
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
      cat("   --pollenType=CHARACTER     Name of the pollen type to be plotted\n")
      cat("   --year=INTEGER             Season to be plotted\n")
      cat("   --days=INTEGER             Number of days beyond each side of the main pollen season to be represented (default: 30)\n")
      cat("   --filCol=CHARACTER         Color to fill the main pollen season in the plot (default: turquoise4)\n")
      cat("   --axisname=CHARACTER       Y axis title of the plot (default: Pollen grains / m ^ 3)\n")
      cat("   --intMethod=CHARACTER      Interpolation method (options: lineal, movingmean, spline or tseries, default: lineal)\n")
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

  # Check if pollenType is missing
  if (is.null(pollen_type)) {
    stop("Error: argument --pollenType is mandatory")
  }

  # Check if year is missing
  if (is.null(year)) {
    stop("Error: argument --year is mandatory")
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

  # Open a PDF file for output
  pdf(paste0(output_folder, "output.pdf"))

  # Plot the data
  plt_ps <- plot_ps(
    data = data,
    pollen.type = pollen_type,
    year = year,
    days = days,
    fill.col = fil_col,
    int.method = int_method,
    axisname = axisname
  )

  # Display the plot
  plot(plt_ps)

  # Close the PDF file
  dev.off()
}