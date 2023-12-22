import argparse
import os
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from minio import Minio

MINIO_HOST = os.environ["MINIO_HOST"]
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
MINIO_USE_SSL = bool(os.environ["MINIO_USE_SSL"])


def get_filename(url: str) -> str:
    """Returns the filename from a URL."""
    return os.path.basename(urlparse(url).path)


def get_minio(bucket_name: str, object_name: str, file_path: str) -> str:
    """Downloads a file from a Minio bucket."""
    client = Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_USE_SSL,
    )
    client.fget_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path,
    )
    return filepath.as_posix()


def main(url: str, query_string: str | None, output: str) -> None:
    """Imports a file from an online resource."""
    try:
        if url.startswith("minio://"):
            parsed_url = urlparse(url)
            bucket_name = parsed_url.netloc
            object_name = parsed_url.path.lstrip("/")
            get_minio(bucket_name, object_name, output)
        else:
            if query_string:
                url = url + query_string
            urllib.request.urlretrieve(url, output)
    except Exception as e:
        raise Exception("File could not be downloaded") from e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Import a file from an online resource."
    )
    parser.add_argument("--url", type=str, required=True, help="URL of the file")
    parser.add_argument(
        "--query-string",
        type=str,
        required=False,
        help="Query string attached to the end of a url",
    )
    parser.add_argument(
        "--rename",
        type=str,
        required=False,
        help="New name of the file. If not specified, the original name is used.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output directory.",
    )
    args = parser.parse_args()

    filename = args.rename if args.rename else get_filename(args.url)
    filepath = Path(args.output, filename)

    main(url=args.url, query_string=args.query_string, output=filepath.as_posix())
