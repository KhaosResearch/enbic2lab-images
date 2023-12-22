#######################
# Command line config #
#######################
# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input <- NULL
  pollen <- NULL
  mave <- 1
  normalized <- FALSE
  interpolation <- TRUE
  int_method <- "lineal"
  color_plot <- "orange2"
  axis_name <- "Pollen grains / m3"
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input <- args[i + 1]
    } else if (args[i] == "--pollen") {
      pollen <- args[i + 1]
    } else if (args[i] == "--mave") {
      mave <- as.numeric(args[i + 1])
    } else if (args[i] == "--normalized") {
      normalized <- as.logical(args[i + 1])
    } else if (args[i] == "--interpolation") {
      interpolation <- as.logical(args[i + 1])
    } else if (args[i] == "--intMethod") {
      int_method <- args[i + 1]
    } else if (args[i] == "--colorPlot") {
      color_plot <- args[i + 1]
    } else if (args[i] == "--axisname") {
      axis_name <- args[i + 1]
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
      cat("   --filepath=CHARACTER        Input file path\n")
      cat("   --pollen=CHARACTER          Particle name (mandatory)\n")
      cat("   --mave=NUMERIC              Order of the moving average (default: 1)\n")
      cat("   --normalized=LOGICAL        Use normalized data (default: TRUE)\n")
      cat("   --interpolation=LOGICAL     Apply interpolation (default: TRUE)\n")
      cat("   --intMethod=CHARACTER       Interpolation method\n")
      cat("   --colorPlot=CHARACTER       Color plot\n")
      cat("   --axisname=CHARACTER        Y-axis title (default: 'Pollen grains / m3')\n")
      cat("   --delimiter=CHARACTER       Dataframe delimiter\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER         Library for importing packages\n")
      # Quit the script
      quit(status = 0)
    }
  }

  # Check if file path is missing
  if (is.null(input)) {
    stop("Error: argument --filepath is mandatory")
  }

  # Check if pollen is missing
  if (is.null(pollen)) {
    stop("Error: argument --pollen is mandatory")
  }
}

##################
# load libraries #
##################

# Check that the script is not being tested
if (!exists("test")) {
  if (!is.null(lib)) .libPaths(lib)
  library(AeRobiology)
  library(pdftools)
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
  data <- readFile(input, delimiter)

  # Call the function plot_normsummary with the specified parameters
  plot_normsummary(
    data = data,
    pollen = pollen,
    mave = mave,
    normalized = normalized,
    interpolation = interpolation,
    int.method = int_method,
    export.plot = TRUE,
    export.format = "pdf",
    color.plot = color_plot,
    axisname = axis_name
  )
  dev.off()

  # Combine the generated pdfs
  pdf_file1 <- "./Rplots.pdf"
  pdf_file2 <- paste0("./plot_AeRobiology/plot_normsummary_", pollen, ".pdf")
  pdf_combine(c(pdf_file1, pdf_file2), paste0(output_folder, "output.pdf"))

  # Remove original pdfs
  file.remove(pdf_file1, pdf_file2)
}