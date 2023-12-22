import argparse
import zipfile
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from pykrige.ok3d import OrdinaryKriging3D


def get_value_in_coordinate(lon, lat, rasterio_opened, band):
    """
    Get the value of a coordinate in a rasterio object
    """
    val = rasterio_opened.index(lon, lat)
    return band[abs(val[0]), abs(val[1])]


def kriging(
    shp_path: Path,
    dem_path: Path,
    column_name: str,
    use_shp_height: bool,
    grid_size: int,
    output: str,
):
    shp_unzip_path = Path("shapefile_unzip")
    shp_unzip_path.mkdir(exist_ok=True)

    with zipfile.ZipFile(shp_path, "r") as zip_ref:
        zip_ref.extractall(shp_unzip_path)

    gdf = gpd.read_file(Path(shp_unzip_path))

    gdf = gdf.to_crs(crs=4326)  # degrees

    gdf["LATITUDE"] = gdf["geometry"].y
    gdf["LONGITUDE"] = gdf["geometry"].x

    gdf[column_name] = gdf[column_name].replace(",", ".", regex=True).astype(float)

    if use_shp_height in ["true", "1", "yes", "t"]:
        with rasterio.open(Path(dem_path)) as merged_dem:
            band = merged_dem.read(1)
            band_mean = band.mean()
            band_std = band.std()
            band = (((band - band_mean) / band_std) + 1) / 2
            gdf["ALTITUDE"] = gdf.apply(
                lambda row: get_value_in_coordinate(
                    row["LONGITUDE"], row["LATITUDE"], merged_dem, band
                ),
                axis=1,
            )

    elif use_shp_height in ["false", "0", "no", "f"]:
        gdf["ALTITUDE"] = gdf["geometry"].z

        altitude = gdf["ALTITUDE"].isna().all()

        if altitude:
            print("This shapefile has no z axis. Try using --use-shp-height False")
            raise ValueError(
                "This shapefile has no z axis. Try using --use-shp-height False"
            )
        z_mean = gdf["ALTITUDE"].mean()
        z_std = gdf["ALTITUDE"].std()
        gdf["ALTITUDE"] = (((gdf["ALTITUDE"] - z_mean) / z_std) + 1) / 2

        with rasterio.open(dem_path) as merged_dem:
            band = merged_dem.read(1)

            band_mean = band.mean()
            band_std = band.std()
            band = (((band - band_mean) / band_std) + 1) / 2
    else:
        raise ValueError("Invalid value for --use-shp-height. Please use one of: true, false, 1, 0, yes, no, t, f")

    x_orig = gdf["LONGITUDE"]
    y_orig = gdf["LATITUDE"]
    z_orig = gdf["ALTITUDE"]

    x_grid = np.linspace(np.min(x_orig), np.max(x_orig), grid_size)
    y_grid = np.linspace(np.max(y_orig), np.min(y_orig), grid_size)

    xy_grid_points = np.stack(np.meshgrid(x_grid, y_grid), -1).reshape(-1, 2).tolist()

    xyz_grid_points = np.array(
        [
            [
                xy_point[0],
                xy_point[1],
                get_value_in_coordinate(xy_point[0], xy_point[1], merged_dem, band),
            ]
            for xy_point in xy_grid_points
        ]
    )

    kriging = OrdinaryKriging3D(x_orig, y_orig, z_orig, val=gdf[column_name])

    predictions, _ = kriging.execute(
        style="points",
        xpoints=xyz_grid_points[:, 0],
        ypoints=xyz_grid_points[:, 1],
        zpoints=xyz_grid_points[:, 2],
        n_closest_points=10,
        backend="loop",
    )

    plt.scatter(
        x=xyz_grid_points[:, 0],
        y=xyz_grid_points[:, 1],
        c=predictions.data,
        cmap=plt.cm.jet,
    )
    plt.scatter(
        x=x_orig, y=y_orig, c=gdf[column_name], cmap=plt.cm.jet, edgecolor="white"
    )
    plt.colorbar()

    plt.xlabel("Longitude (Degrees)")
    plt.ylabel("Latitude (Degrees)")

    output_file_path_3d = Path(output + "output.png")
    plt.savefig(output_file_path_3d)

    df_final = pd.DataFrame(
        {
            "LATITUDE": xyz_grid_points[:, 1],
            "LONGITUDE": xyz_grid_points[:, 0],
            "ALTITUDE": xyz_grid_points[:, 2],
            str(column_name): predictions,
        }
    )

    df_final["ALTITUDE"] = (df_final["ALTITUDE"] * 2 - 1) * band_std + band_mean

    df_final.to_csv(output + "output.csv")


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
        "--dem-path",
        type=Path,
        required=True,
        help="Digital Elevation Model (DEM) path in tiff format path.",
    )

    parser.add_argument(
        "--column-name",
        type=str,
        required=True,
        help="Name of the column to be interpolated.",
    )

    parser.add_argument(
        "--use-shp-height",
        type=str.lower,
        dest="use_shp_height",
        required=False,
        default="True",
        help="Use height from SHP file. If false, take the height values from the DEM instead.",
        choices=[
            "true",
            "false",
            "1",
            "0",
            "yes",
            "no",
            "t",
            "f"
        ],
    )

    parser.add_argument(
        "--grid-size",
        type=int,
        required=True,
        help="Size of the grid to use in pixels.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/outputs/",
        help="Output path.",
    )

    args = parser.parse_args()

    kriging(
        args.shp_path,
        args.dem_path,
        args.column_name,
        args.use_shp_height,
        args.grid_size,
        args.output
    )
