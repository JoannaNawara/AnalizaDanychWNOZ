from .region_data import choose_region
from .region_map import region_stations_map
#from region_data import choose_region
#from region_map import region_stations_map

def check_stations_unique(region):
    mapa, data = choose_region(region)
    counted = data.groupby("geometry").count().sort_values("ID")
    number = len(counted)
    number_unique = sum(counted["ID"] == 1)
    if number_unique - number == 0:
        print("All stations are unique in this region")
    else:
        print("There are duplicate stations in this region")

def analysis_1(region):
    print("\nFirst analysis:\n")
    print(f"1. Stations list for region {region}:")
    mapa, stations = choose_region(region)
    print(stations.to_string())
    print("\n2. Checking if stations are unique in this region")
    check_stations_unique(region)
    print(f"\n3. Map with {len(stations)} station locations saved in file 'Station_locations_{region}.png'")
    region_stations_map(region)

if __name__ == "__main__":
    analysis_1("dolnośląskie")