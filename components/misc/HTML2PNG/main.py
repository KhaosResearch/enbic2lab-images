import imgkit
from argparse import ArgumentParser

def html2png(
        filepath: str,
        output: str
    ) -> None:
    # Convert HTML to PNG
    with open(filepath) as file:
        imgkit.from_file(
            filename=file,
            output_path=output,
            options={
                "format": "png",
                "encoding": "UTF-8",
                "quiet": None
            }
        )


if __name__ == "__main__":
    parser = ArgumentParser(description="Convert HTML to PNG")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Name of the HTML file",
        required=True,
        dest="filepath",
        metavar="STRING"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path of the output PNG file",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING"
    )

    args = parser.parse_args()

    html2png(
        filepath=args.filepath,
        output=args.output+"/output.png"
    )