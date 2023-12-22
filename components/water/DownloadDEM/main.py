import argparse
import glob
import math
import os
import tempfile
import zipfile
from pathlib import Path
from typing import List

import geopandas as gpd
import numpy as np
import rasterio
import requests
from rasterio import merge


def download(url: str, dest_folder: str):
    # https://stackoverflow.com/a/56951135/8761164
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split("/")[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)

    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


def parse_lat(lat: int):
    """
    Parse latitude into a string. Appending N or S depending on the sign of the latitude.

    :param lat: Latitude in decimal degrees
    :return: String representation of the latitude
    """
    lat_str = "N" if lat >= 0 else "S"
    if 10 > lat > -10:
        lat_str += "0"
    lat_str += str(abs(lat))
    return lat_str


def parse_long(long: int):
    """
    Parse longitude into a string. Appending E or W depending on the sign of the longitude.

    :param long: Longitude in decimal degrees
    :return: String representation of the longitude
    """
    long_str = "E" if long >= 0 else "W"
    if 100 > long > -100:
        long_str += "0"
    if 10 > long > -10:
        long_str += "0"
    long_str += str(abs(long))
    return long_str


def _get_kwargs_raster(raster_path):
    """
    Get a raster's metadata from a raster's path
    """
    with rasterio.open(raster_path) as raster_file:
        kwargs = raster_file.meta
        return kwargs


def _merge_dem(dem_paths: List[Path], dem_name: str) -> Path:
    """
    Given a list of DEM paths and the corresponding product's geometry, merges them into a single raster.

    Returns the path to the merged DEM.
    """
    out_dem_meta = _get_kwargs_raster(dem_paths[0])
    dem_paths, dem_transform = merge.merge(dem_paths)
    out_dem_meta["driver"] = "GTiff"
    out_dem_meta["dtype"] = np.float32
    out_dem_meta["height"] = dem_paths.shape[1]
    out_dem_meta["width"] = dem_paths.shape[2]
    out_dem_meta["transform"] = dem_transform
    out_dem_meta["nodata"] = np.nan

    outpath_dem = dem_name

    if not os.path.exists(os.path.dirname(outpath_dem)):
        os.makedirs(os.path.dirname(outpath_dem))

    with rasterio.open(outpath_dem, "w", **out_dem_meta) as dm:
        dm.write(dem_paths)

    return outpath_dem


def unzip_aster_files(file_paths, out_folder):
    for file_path in file_paths:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            for inner_file in zip_ref.namelist():
                if inner_file.endswith("_dem.tif"):
                    zip_ref.extract(inner_file, out_folder)


def calculate_coordinates(lat, long):
    """
    To obtain the right dem according to the shapefile limits it is necessary to adjust the coordinate values.
    When a latitude or longitude is positive, it will be rounded down, while when it is negative, it will be rounded up.
    38.78 would be rounded down to 38 while -4.1 would be rounded down to -5.

    Returns the latitude and longitude with the needed transformation.
    """
    if lat <= 0:
        lat = -math.ceil(abs(lat))

    if long <= 0:
        long = -math.ceil(abs(long))

    if lat >= 0:
        lat = math.floor(lat)

    if long >= 0:
        long = math.floor(long)

    return lat, long


def download_dem(shp_path: Path, output: str):
    with tempfile.TemporaryDirectory() as shp_unzip_path:
        with zipfile.ZipFile(shp_path, "r") as zip_ref:
            zip_ref.extractall(shp_unzip_path)

        gdf = gpd.read_file(shp_unzip_path)

    gdf = gdf.to_crs(crs=4326)
    gdf["LATITUDE"] = gdf["geometry"].y
    gdf["LONGITUDE"] = gdf["geometry"].x

    lat_max, lat_min = gdf["LATITUDE"].max(), gdf["LATITUDE"].min()
    lon_max, lon_min = gdf["LONGITUDE"].max(), gdf["LONGITUDE"].min()

    lat_max, lon_max = calculate_coordinates(lat_max, lon_max)
    lat_min, lon_min = calculate_coordinates(lat_min, lon_min)

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        for lat in range(lat_min, lat_max + 1):
            for long in range(lon_min, lon_max + 1):
                download(
                    f"https://gdemdl.aster.jspacesystems.or.jp/download/Download_{parse_lat(lat)}{parse_long(long)}.zip",
                    dest_folder=temp_dir,
                )

        dem_files = os.listdir(temp_dir)
        aster_temp_folder = f"{temp_dir}/aster-temp"
        unzip_temp_folder = f"{aster_temp_folder}/aster_dem_tmp"

        for file_name in dem_files:
            with zipfile.ZipFile(f"{temp_dir}/{file_name}", "r") as zip_ref:
                zip_ref.extractall(aster_temp_folder)

        tif_files = glob.glob(f"{aster_temp_folder}/ASTGTMV003_*.zip")
        unzip_aster_files(tif_files, unzip_temp_folder)
        aster_files = glob.glob(f"{unzip_temp_folder}/*")
        _merge_dem(aster_files, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Apply the kriging algorithm to interpolate data from a Shapefile."
    )

    parser.add_argument(
        "--shp-path",
        type=Path,
        required=True,
        help="Input zip file path that contains a Shapefile.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        help="Output path.",
    )

    args = parser.parse_args()

    download_dem(args.shp_path, args.output + "output.tif")
