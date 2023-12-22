from datetime import date
import numpy as np
import os, zipfile
import cv2
import pandas as pd
from argparse import ArgumentParser

def unzipFile(file: str, directory: str) -> None:
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(directory)


def listFiles(directory: str, extension: str) -> list:
    for (_, _, filenames) in os.walk(directory):
        files = []
        for filename in filenames:
            if filename.endswith("." + extension):
                print(filename)
                files.append(filename)
        return files


def analyseImage(image_name: str, image_directory: str, percentage: float = 0.7) -> list:

    print("Image analyzed: " + image_name)

    # im = cv2.imread(image_directory+'\\'+image_name) # Windows
    try:
        im = cv2.imread(image_directory + "/" + image_name)
    

        # Splitting image in two different images for each day
        dims = im.shape

        cropped_images = []
        cropped_images.append(im[0 : int(dims[0] * percentage), 0 : dims[1]])
        cropped_images.append(im[int(dims[0] * percentage) : dims[0], 0 : dims[1]])

    except Exception as e:
        print(e)
        return [0, 0]

    # Colors to Filter
    lower_pink = np.array([135, 19, 89])
    higher_pink = np.array([179, 255, 255])

    res = []
    for cp_image in cropped_images:

        # Color filtering
        hsv = cv2.cvtColor(cp_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_pink, higher_pink)
        cv2.bitwise_and(cp_image, cp_image, mask=mask)

        # Noise reduction
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=2)

        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        res.append(len(cnts))

    return res


def resultToPandas(result: list, name: str, measureDate: str | date) -> pd.DataFrame:
    server_date = f"{date.today().day}/{date.today().month}/{date.today().year}"

    test_df = pd.DataFrame(
        data={
            "SampleName": name,
            "SampleDate": measureDate,
            "AnalysisDate": server_date,
            "DayResult": result[0],
            "NextDayResult": result[1],
        },
        index=[0]
    )

    return test_df


def pollenCount(
    filepath: str,
    sample_name: str,
    output_path: str,
    sample_date: str = None,
    delimiter: str = ","
) -> None:
    """Count pollen points

    This function counts pollen points from a tiff image. Then returns the results as a CSV and JSON.

    Args:
        - filepath (str): The path to the zip file with the images
        - sample_name (str): Name of the experiment
        - outuput_path (str): Path for the output files
        - sample_date (str): Date of the experiment
        - delimiter (str): Delimiter to be used in the output CSV

    Returns:
        - None
    """
    
    unzipFile(filepath, "images")

    totalBlobsDetected = [0, 0]
    for image in listFiles("images", "ome.tiff"):
        res = analyseImage(image, "images", 0.5833)
        totalBlobsDetected = np.add(totalBlobsDetected, res)

    print(totalBlobsDetected)

    if sample_date is None:
        sample_date = ""

    pandas_df = resultToPandas(totalBlobsDetected, sample_name, sample_date)
    pandas_df.to_csv(f"{output_path}output.csv", index=False, sep=delimiter)
    pandas_df.to_json(f"{output_path}output.json", orient="records", indent=4)


if __name__ == "__main__":
    parser = ArgumentParser(description="Count pollen in images")
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path to the images ZIP",
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--sample-name",
        type=str,
        required=True,
        help="Analysed sample name",
        dest="sample_name",
        metavar="STRING",
    )
    parser.add_argument(
        "--sample-date",
        type=str,
        required=False,
        default=None,
        help="Sample date of collection",
        dest="sample_date",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=",",
        help="Delimiter of csv file",
        dest="delimiter",
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared/",
        help="Output path",
        dest="output",
        metavar="STRING",
    )
    
    args = parser.parse_args()

    pollenCount(
        filepath=args.filepath,
        sample_name=args.sample_name,
        sample_date=args.sample_date,
        delimiter=args.delimiter,
        output_path=args.output,
    )
