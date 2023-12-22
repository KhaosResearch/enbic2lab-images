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
  result <- processData(data, 2022)
  
  # Check if the 'years' column in the 'result' data frame contains the expected values
  expect_equal(result$data_by_year$years, c("2022", "2022"))
})

# Test for the createPlot function
test_that("createPlot returns a plotly object", {
  # Create a sample data frame
  data_by_year <- data.frame(
    date = as.Date(c("2022-01-01", "2022-01-02")),
    pollenA = c(10, 20),
    pollenB = c(30, 10),
    years = c("2022", "2022"),
    month = c("01", "01")
  )
  
  # Create a plot using the createPlot function and store it in the 'fig' variable
  fig <- createPlot(data_by_year, c("pollenA", "pollenB"))
  
  # Check if the 'fig' variable is of type 'plotly'
  expect_true(inherits(fig, "plotly"))
})