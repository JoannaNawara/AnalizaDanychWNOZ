from src.region_data import get_region_meteo_data
from src.region_map import region_stations_analysis_map
#from region_data import get_region_meteo_data
#from region_map import region_stations_analysis_map

def check_empty_stations(data):
    number = data["Kod stacji"].isnull().sum()
    print(f"{number} of stations don't have any data\n\nThose stations are:")
    print(data[data["Kod stacji"].isnull()]["Nazwa"])
    empty = data[data["Kod stacji"].isnull()]
    data.drop(data[data["Kod stacji"].isnull()].index, inplace=True)
    number = len(data["Kod stacji"].unique())
    print(f"\nAfter deleting them we are left with {number} stations")
    return data, empty

def data_time_span(data):
    #[len(row) for row in data.groupby("ID")["Rok"].unique()]
    #print(data["Time"])
    return data

def analysis_2(region):
    print("\nSecond analysis:\n")
    data = get_region_meteo_data(region)
    print(f"\n1. Checking how mamy stations don't have any data for {region}:")
    data, empty = check_empty_stations(data)
    region_stations_analysis_map(region, data, empty)

if __name__ == "__main__":
    analysis_2("dolnośląskie")