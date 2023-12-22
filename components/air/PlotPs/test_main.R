# Extract the location of the library, if not specified, the default is taken
args <- commandArgs(trailingOnly = TRUE)
lib <- if (length(args) > 0) args[[1]] else NULL

# Load the main script
test <- TRUE
if (!is.null(lib)) .libPaths(lib)
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