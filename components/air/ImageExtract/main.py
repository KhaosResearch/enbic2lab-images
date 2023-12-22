import numpy as np
import os, zipfile, re
import bioformats as bf
import javabridge
from argparse import ArgumentParser


def startJava():
    # Start CellProfiler's JVM via Javabridge

    javabridge.start_vm(class_path=bf.JARS, max_heap_size="6G")  # Sobremesa "ps3aj"
    javabridge.attach()

    """
    # This is so that Javabridge doesn't spill out a lot of DEBUG messages during runtime. From CellProfiler/python-bioformats.
    rootLoggerName = javabridge.get_static_field("org/slf4j/Logger", "ROOT_LOGGER_NAME", "Ljava/lang/String;")
    rootLogger = javabridge.static_call("org/slf4j/LoggerFactory", "getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
    logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level", "WARN", "Lch/qos/logback/classic/Level;")
    javabridge.call(rootLogger, "setLevel", "(Lch/qos/logback/classic/Level;)V", logLevel)
    """


def stopJava():
    javabridge.detach()
    javabridge.kill_vm()


def unzipFile(file: str, directory: str):
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(directory)


def listFiles(directory: str, extension: str):
    for _, _, filenames in os.walk(directory):
        files = []
        for filename in filenames:
            if filename.endswith("." + extension):
                files.append(filename)
        return files


def getImageInfo(input_image: str):
    javabridge.attach()

    file_full_path = input_image  # Ruta del fichero
    md = bf.get_omexml_metadata(file_full_path)
    # Lectura de sus metadatos para obtener el ID de las series sin comprimir

    ome = bf.OMEXML(md)
    niceImages = []
    for serie in range(ome.get_image_count()):
        # Por cada serie que contenga nuestra imagen
        currentImage = ome.image(serie)

        acquisitionDate = None
        acquisitionDate = currentImage.get_AcquisitionDate()

        if acquisitionDate != None:
            # Nos quedamos unicamente con las que tengan fecha de captura, es decir, las que son sin comprimir
            total_pixel = (
                currentImage.Pixels.get_SizeX() * currentImage.Pixels.get_SizeY()
            )
            niceImages.append((serie, currentImage.get_Name(), total_pixel))
            # Y almacenamos ese numero de serie en una lista que despues utilizaremos para la conversión

    javabridge.detach()
    return niceImages


def parseImages(
    imageList: list,
    image_directory: str,
    output_directory: str,
    regex_filter: str,
    tam_filter: int,
):
    try:
        max_pixel_amount = int(tam_filter)
    except:
        max_pixel_amount = max([image[2] for image in imageList])

    for image in imageList:
        if (regex_filter == "" or re.match(regex_filter, image[1])) and image[
            2
        ] >= max_pixel_amount:
            print(image)
            stringScript = "./bioformats/bfconvert "
            stringScript += "-overwrite "
            stringScript += "-series " + str(image[0]) + " "
            stringScript += '"' + image_directory + '" '
            stringScript += '"' + output_directory + '/%n.ome.tiff"'
            os.system(stringScript)
            print(stringScript)


def compressImages(zippath: str):
    zf = zipfile.ZipFile(file=zippath + ".zip", mode="w")
    for dirname, subdirs, files in os.walk("images"):
        for filename in files:
            print("images/" + filename)
            zf.write("images/" + filename, filename)
    
    if(len(zf.namelist()) == 0):
        print("WARNING: No images returned")
        
    zf.close()


def imageExtract(
    filepath: str,
    output_path: str,
    file_extension: str = "vsi",
    image_name_regex: str = None,
    min_image_size: int = 10000,
) -> None:
    """Extract images from a zip file

    This function extracts images of the extension given in `file_extension`
    from a zip file and saves them in a directory given by the user.

    Args:
        - filepath (str): Path to the zip file
        - output_path (str): Output directory
        - file_extension (str): Extension of the file
        - image_name_regex (str): Regex to filter the image names
        - min_image_size (str): Minimum image size

    Returns:
        - None
    """

    directory = "vsi"

    unzipFile(filepath, directory)

    vsiFiles = listFiles(directory, file_extension)

    vsiFile = vsiFiles[0]

    startJava()

    selectedImages = [x for x in getImageInfo(directory + "/" + vsiFile)]

    if not image_name_regex:
        image_name_regex = ""

    if min_image_size == None or min_image_size == "":
        min_image_size = 0

    parseImages(
        selectedImages,
        directory + "/" + vsiFile,
        "images",
        image_name_regex,
        min_image_size,
    )

    stopJava()

    compressImages(f"{output_path}imagesZipped")


if __name__ == "__main__":
    parser = ArgumentParser(description="Extract images from a zip file")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path to the zip file",
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--file-extension",
        type=str,
        required=False,
        default="vsi",
        help="Extension of the file",
        dest="file_extension",
        metavar="STRING",
    )
    parser.add_argument(
        "--image-name-regex",
        type=str,
        required=False,
        default=None,
        help="Regex to filter the image names",
        dest="image_name_regex",
        metavar="STRING",
    )
    parser.add_argument(
        "--min-image-size",
        type=int,
        required=False,
        default=10000,
        help="Minimum image size",
        dest="min_image_size",
        metavar="INT",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared/",
        help="Output directory",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    imageExtract(
        filepath=args.filepath,
        file_extension=args.file_extension,
        image_name_regex=args.image_name_regex,
        min_image_size=args.min_image_size,
        output_path=args.output,
    )
