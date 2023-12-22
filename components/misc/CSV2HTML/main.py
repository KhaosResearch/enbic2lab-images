import argparse
import pandas as pd


def main(filepath: str, output_file: str, delimiter: str = ";") -> None:
    """
    Convert a CSV file to HTML format.

    Args:
        filepath (str): The path to the input CSV file.
        delimiter (str): The delimiter used in the input CSV file.
        output_file (str): The path to the output HTML file.

    Returns:
        None
    """
    # Read the CSV file into a DataFrame
    csv_data = pd.read_csv(filepath, sep=delimiter)

    # Export the DataFrame to an HTML table with inline styles
    html_content = csv_data.to_html(index=False, escape=True, classes='styled-table', 
                                    table_id='my-table',
                                    border=0)

    # Add inline CSS styles for the table
    styled_html_content = f"""
        <div style="font-family: American Typewriter;">
            <style>
                .styled-table {{
                    font-family: 'Arial', sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }}
                .styled-table th, .styled-table td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                .styled-table th {{
                    background-color: #f2f2f2;
                }}
                .styled-table tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .styled-table tr:hover {{
                    background-color: #ddd;
                }}
            </style>
            {html_content}
        </div>
    """

    # Write the HTML content to the output file
    with open(output_file, 'w') as f:
        f.write(styled_html_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a CSV file to HTML.")
    
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Filepath of the CSV file",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=";",
        help="Delimiter of the CSV file",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        help="Filepath of the output HTML file",
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )
    
    args = parser.parse_args()

    main(
        filepath=args.filepath,
        delimiter=args.delimiter,
        output_file=args.output+"/output.html",
    )
