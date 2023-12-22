#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  pollen <- NULL
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--pollen") {
      pollen <- args[i + 1]
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
      cat("   --pollen=CHARACTER     A character string with the name of the particle to show. This is a mandatory argument\n")
      cat("   --delimiter=CHARACTER  Dataframe delimiter (default: ,)\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER    Library from which to import the packages (default: NULL)\n")
      # Quit the script
      quit(status = 0)
    }
  }

  # Check if pollen is missing
  if (is.null(pollen)) {
    stop("Error: argument --pollen is mandatory")
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
  library(plotly)
  library(dplyr)
  library(htmlwidgets)
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

# Processes the data by removing leap day entries and grouping by year
# Arguments:
#   data: A data frame with a date column and other columns of interest
# Returns:
#   A grouped data frame with one row per year and columns for the year, month, and other columns of interest
processData <- function(data) {
  data <- data[!(format(data$date, "%m") == "02" & format(data$date, "%d") == "29"), , drop = FALSE]

  data_by_year <- data %>%
    mutate(year = format(data$date, "%Y")) %>%
    mutate(month = format(data$date, "%m")) %>%
    group_by(year)

  return(data_by_year)
}

# Creates a plotly plot of the data by year
# Arguments:
#   data_by_year: A grouped data frame with one row per year and columns for the year, month, and other columns of interest
#   pollen: The name of the column to plot
# Returns:
#   A plotly plot with one line for each year, showing the values in the specified pollen column over the course of the year
createPlot <- function(data_by_year, pollen) {

  fig <- plot_ly(type = "scatter", mode= "lines")

  for (y in unique(data_by_year$year)) {
    data <- filter(data_by_year, year == y)
    data[is.na(data)] <- 0
    data$days <- seq(1, 365, by = 1)
    fig <- fig %>% add_trace(x = data$days, y = data[[pollen]], mode = "markers", fill = "tozeroy", name = y)
  }

  fig <- fig %>% layout(
    xaxis = list(title = "DOY"),
    yaxis = list(title = "Pollen grains / m3")
  )

  return(fig)
}


########
# MAIN #
########

# Check that the script is not being tested
if (!exists("test")) {
  # Read the input file and store the data
  data <- readFile(input_file, delimiter)
  
  # Process the data and get the result
  data_by_year <- processData(data)
  
  # Create a plot using the processed data and pollen
  fig <- createPlot(data_by_year, pollen)

  # Save the plot as a self-contained HTML file
  saveWidget(fig, paste0(output_folder, "output.html"), selfcontained = TRUE, libdir = NULL)
}
