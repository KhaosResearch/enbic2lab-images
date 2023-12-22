import argparse
import json
from datetime import datetime
from enum import Enum
from re import findall
from typing import List
from urllib.parse import urljoin
import time

import requests
from dateutil.relativedelta import relativedelta

# ================ Classes ================
# Period
class Period(Enum):
    WEEKLY = "WEEKLEY"
    HOURLY = "HOURLY"


# Aemet
class Aemet:
    BASE_URL = "https://opendata.aemet.es/opendata/api/"
    EMA_API_URL_STATIONS = urljoin(BASE_URL, "valores/climatologicos/inventarioestaciones/todasestaciones")
    DAILY_WEATHER_VALUE = urljoin(
        BASE_URL, "valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}/?api_key={}"
    )

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_daily_weather(self, start_date, end_date, station):
            start_date_parse = start_date.strftime("%Y-%m-%dT%H:%M:%SUTC")
            end_date_parse = end_date.strftime("%Y-%m-%dT%H:%M:%SUTC")
            url = self.DAILY_WEATHER_VALUE.format(start_date=start_date_parse, end_date=end_date_parse, station=station, api_key=self.api_key)
            time_sleep = 0

            try:
                response = requests.get(url, headers=self._get_headers())
                response.raise_for_status()
                
                redirect_url = response.json()["datos"]
                r = requests.get(redirect_url, headers=self._get_headers())
                r.raise_for_status()

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                return None

            while r.status_code == 429:
                time.sleep(time_sleep)
                r = requests.get(redirect_url, headers=self._get_headers())
                time_sleep += 5

            if r.status_code == 200:
                all_data = r.json()
                return all_data
            else:
                print(f"Unexpected status code: {r.status_code}")
                return None

    def _get_headers(self):
        return {"api_key": self.api_key}
    
def main(
    aemet_api_key: str,
    start_date:str,
    end_date:str,
    analysis_stations: List[str],
    output:str
):
    """
    Download meteorological data from AEMET for multiple Stations.

    Args:
        output (str) -> Output filepath
        start_date (str) -> First date of the date range, format (yyyy-mm-dd).
        end_date (str) -> Last date of the date range, format (yyyy-mm-dd).
        analysis_stations (List[str]) -> Station list for AEMET data search.
        aemet_api_key (str) -> Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).
    """
# Parsing date
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Download AEMET Data
    aemet_client = Aemet(api_key=aemet_api_key)
    stations_weather_values = []
    try:
        for station in analysis_stations:
            daily_weather_values = []
            start = start_date
            while start <= end_date:
                try:
                    daily_weather_values.extend(
                        aemet_client.get_daily_weather(start, start + relativedelta(years=3), station)
                    )
                except Exception as e:
                    print(f"Warning in station {station} at start date {start}: {e}")
                    pass
                start = start + relativedelta(day=1, years=3)

            stations_weather_values.extend(daily_weather_values)

    except Exception as e:
        print(f"Warning in station {station} at start date {start}: {e}")
    with open(output, 'w', encoding='utf-8') as json_file:
        json.dump(stations_weather_values, json_file, ensure_ascii=False, indent=2)


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Statistics component")

    # Define command-line arguments
    parser.add_argument(
        "--output", 
        type=str, 
        required=True, 
        help="Output file name", 
        default="/mnt/shared/output.json"
    )
    parser.add_argument(
        "--aemet-api-key", 
        type=str, 
        required=True, 
        help="Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?)."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="1991-05-11",
        required=True,
        help="Start date",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default="2021-09-30",
        required=True,
        help="End date",
    )
    parser.add_argument(
        "--analysis-stations",
        type=str,
        default="6155A,6172O,6156X",
        required=True,
        help="Analysis stations separated with comma",
    )

    args = parser.parse_args()
    args.analysis_stations = findall(r'\s*([^,]+)\s*', args.analysis_stations) if args.analysis_stations != None else None

    # Call the main function with provided arguments and specify the output file path
    main(
        args.aemet_api_key,
        args.start_date,
        args.end_date,
        args.analysis_stations,
        args.output
    )
