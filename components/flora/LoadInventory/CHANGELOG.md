# Changelog

## v1.0.0

- Eliminate unnecessary conditionals.

- Save the information in a dataframe
    -   Old version: iteratively creating and filling a dataframe --> very inefficient.
    -   New version: directly save the information in a dictionary and transform it into a dataframe.

- If we do not want to filter by a field, it is not necessary to pass it as "". Now all the parameters are optional
