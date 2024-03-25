#from src.data_ingestion import create_path_to_data
#from src.plot_map import read_data_points, read_data_map
from data_ingestion import create_path_to_data
from reading_data import read_map_data, read_localization_data, read_meteo_data

def choose_region(region):
    points = read_localization_data()
    mapa = read_map_data()
    region_map = mapa[mapa["JPT_NAZWA_"] == region]
    region_points = points[points.within(region_map["geometry"].iloc(0)[0])]
    return region_map, region_points

def get_region_meteo_data(region):
    print("Getting data for chosen region")
    region_map, region_points = choose_region(region)
    meteo = read_meteo_data()
    region_meteo = region_points.merge(meteo, how="left", left_on="ID", right_on="Kod stacji")
    return region_meteo