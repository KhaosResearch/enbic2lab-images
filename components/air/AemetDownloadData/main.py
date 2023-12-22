from enum import Enum
from urllib.parse import urljoin
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import argparse
import requests

# This class provides an enumeration for future uses in Aemet class
class Period(Enum):
    WEEKLY = "WEEKLY"
    HOURLY = "HOURLY"

class Aemet:
    BASE_URL = "https://opendata.aemet.es/opendata/api/"
    EMA_API_URL_STATIONS = urljoin(BASE_URL, "valores/climatologicos/inventarioestaciones/todasestaciones")
    DAILY_WEATHER_VALUE = urljoin(
        BASE_URL, "valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}/?api_key={}"
    )

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_daily_weather(self, start_date: datetime, end_date: datetime, station: str):
        start_date_parse = start_date.strftime("%Y-%m-%dT%H:%M:%SUTC")
        end_date_parse = end_date.strftime("%Y-%m-%dT%H:%M:%SUTC")
        url = self.DAILY_WEATHER_VALUE.format(start_date_parse, end_date_parse, station, self.api_key)
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            redirect_url = response.json()["datos"]
            
            r = requests.get(redirect_url, headers=self._get_headers())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

        all_data = r.json()
        return all_data

    def _get_headers(self):
        return {"api_key": self.api_key}

def main(
    output:str,
    start_date: str,
    end_date: str,
    aemet_api_key:str,
    station: str = "6155A",
    delimiter: str = ";"    
):
    """
    This Python component calculates evapotranspiration using an input CSV file containing necessary data for the calculation.

    Args:
        --start-date (str) -> First date of the date range, format (yyyy-mm-dd).
        --end-date (str) -> Last date of the date range, format (yyyy-mm-dd).
        --station (str) -> Code of the station from AEMET
        --aemet-api-key (str) -> Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).
        --delimiter (str) -> Delimiter of the output CSV File.
        --output (str) -> Putput path
    """
    # Parse Date
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Download Aemet Data
    aemet_client = Aemet(api_key=aemet_api_key)
    daily_weather_values = []
    start = start_date
    try:
        while start <= end_date:
            daily_weather_values.extend(aemet_client.get_daily_weather(start, start + relativedelta(years=3), station))
            start = start + relativedelta(day=1, years=3)
    except Exception as e:
        print(e)

    # Create Dataframe with Aemet Data
    dataframe = pd.json_normalize(daily_weather_values)

    dataframe[["tmed", "prec", "tmin", "tmax", "dir", "velmedia", "racha", "sol", "presMax", "presMin"]] = dataframe[
        ["tmed", "prec", "tmin", "tmax", "dir", "velmedia", "racha", "sol", "presMax", "presMin"]
    ].apply(lambda x: x.str.replace(",", "."))
    dataframe["fecha"] = pd.to_datetime(dataframe["fecha"], format="%Y-%m-%d").dt.date
    dataframe = dataframe.drop(dataframe[dataframe["fecha"] > end_date].index)
    dataframe["prec"].loc[dataframe["prec"] == "Ip"] = 0 

    dataframe.to_csv(output, sep=delimiter, index=None)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Statistics component")

    # Define command-line arguments
    parser.add_argument(
        "--start-date", 
        type=str, 
        required=True, 
        help="Start date", 
        default="1991-05-11"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default="2021-09-30",
        required=True,
        help="End date",
    )
    parser.add_argument(
        "--station",
        type=str,
        default="6155A",
        required=True,
        help="Code of the station from AEMET",
    )
    parser.add_argument(
        "--aemet-api-key",
        type=str,
        required=True,
        help="Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=False,
        help="Delimiter",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output file path",
    )

    args = parser.parse_args()
    
    # Call the main function with provided arguments and specify the output file path
    main(
        args.output,
        args.start_date,
        args.end_date,
        args.aemet_api_key,
        args.station,
        args.delimiter
    )