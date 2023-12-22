# Extract the location of the library, if not specified, the default is taken
args <- commandArgs(trailingOnly = TRUE)
lib <- if (length(args) > 0) args[[1]] else NULL

# Load the main script
test <- TRUE
if (!is.null(lib)) .libPaths(lib)
library(plotly)
library(dplyr)
library(htmlwidgets)
library(testthat)
source("main.R")

# Test for the readFile function
test_that("readFile returns a data.frame", {

  # Create a temporary CSV file
  csv_content <- "date,pollen1,pollen2\n2023-01-01,100,200\n2023-01-02,150,250"
  temp_file <- tempfile(fileext = ".csv")
  writeLines(csv_content, temp_file)

  # Read the CSV file and store the data in the 'data' variable
  data <- readFile(temp_file, ",")
  
  # Check if the 'data' variable is a data.frame
  expect_true(is.data.frame(data))
})

# Test for the processData function
test_that("processData returns the data grouped by year", {
  # Create a sample data frame
  data <- data.frame(
    date = as.Date(c("2022-01-01", "2022-01-02", "2023-01-01")),
    pollen = c(10, 20, 30)
  )

  # Process the data and store the result in the 'result' variable
  result <- processData(data)
  
  # Check if the 'years' column in the 'result' data frame contains the expected values
  expect_equal(result$year, c("2022", "2022", "2023"))
})

# Test for the createPlot function
test_that("createPlot generates the correct plot", {
  # Test data
  data_by_year <- data.frame(
    year = c(rep(2021, 365), rep(2020, 365)),
    pollenA = rep(1, 365 * 2),
    pollenB = rep(2, 365 * 2)
  )

  # Test createPlot function
  plot <- createPlot(data_by_year, "pollen")

  # Check if plot is generated correctly
  expect_true(inherits(plot, "plotly"))
})