#######################
# Command line config #
#######################

# Check that the script is not being tested
if (!exists("test")) {
  # Get the command line arguments
  args <- commandArgs(trailingOnly = TRUE)

  # Initialize variables
  input_file <- NULL
  year <- NULL
  delimiter <- ","
  output_folder <- "/mnt/shared/"
  lib <- NULL

  # Loop through the arguments
  for (i in seq_along(args)) {
    if (args[i] == "--filepath") {
      input_file <- args[i + 1]
    } else if (args[i] == "--year") {
      year <- as.numeric(args[i + 1])
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
      cat("   --year=NUMERIC         An integer value specifying the year to display. This is a mandatory argument\n")
      cat("   --delimiter=CHARACTER  Dataframe delimiter (default: ,)\n")
      cat("   --output-folder=CHARACTER  Output folder path (default: /mnt/shared/)\n")
      cat("   --library=CHARACTER    Library from which to import the packages (default: NULL)\n")
      # Quit the script
      quit(status = 0)
    }
  }

  # Check if year is missing
  if (is.null(year)) {
    stop("Error: argument --year is mandatory")
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

# This function reads a CSV file and converts the date column to a Date format
# Parameters:
#   file: The path to the CSV file
#   delimiter: The delimiter used in the CSV file
# Returns:
#   A data frame with the contents of the CSV file
readFile <- function(file, delimiter) {
  data <- read.csv(file, sep = delimiter)
  data$date <- as.Date(data$date)

  return(data)
}

# This function processes the data read by the readFile function
# Parameters:
#   data: The data frame read by the readFile function
#   year: The year to filter the data by
# Returns:
#   A list containing the filtered data by year and the pollens column names
processData <- function(data, year) {
  colnames <- colnames(data)
  pollens <- colnames[! colnames %in% c("date", "X")]

  data2 <- data %>%
    mutate(years = format(data$date, "%Y")) %>%
    mutate(month = format(data$date, "%m")) %>%
    group_by(years)

  data_by_year <- data2[data2$years == year,]

  return(list(data_by_year = data_by_year, pollens = pollens))
}

# This function creates a plot using the plotly library
# Parameters:
#   data_by_year: The data frame containing the data for a specific year
#   pollens: The column names of the pollens
# Returns:
#   A plotly object representing the plot
createPlot <- function(data_by_year, pollens) {
  fig <- plot_ly(type = "scatter", mode= "lines")

  for (p in pollens) {
    data3 <- data.frame(data_by_year["date"], data_by_year[p], data_by_year["years"], data_by_year["month"])
    data3[is.na(data3)] <- 0
    fig <- fig %>% add_trace(x = data3$date, y = data3[[p]], mode = "markers", fill = "tozeroy", name = p)
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
  result <- processData(data, year)
  
  # Create a plot using the processed data and pollens
  fig <- createPlot(result$data_by_year, result$pollens)

  # Save the plot as a self-contained HTML file
  saveWidget(fig, paste0(output_folder, "output.html"), selfcontained = TRUE, libdir = NULL)
}
