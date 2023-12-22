import pdfkit
from argparse import ArgumentParser


def html2pdf(filepath: str, output: str) -> None:
    """Convert HTML file to PDF.

    This function takes an HTML file as input and converts it to a PDF file using
    the pdfkit library.

    Args:
        filepath (str): The path to the HTML file to be converted.
        output (str): The path to save the converted PDF file.
    """
    with open(filepath) as file:
        pdfkit.from_file(input=file, output_path=output)


if __name__ == "__main__":
    parser = ArgumentParser(description="Convert HTML to PDF")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Name of the HTML file",
        required=True,
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path of the output PDF file",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    html2pdf(filepath=args.filepath, output=args.output+"/output.pdf")
