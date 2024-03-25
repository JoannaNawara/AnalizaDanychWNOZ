import pandas as pd
import geopandas as gpd
#comment to run just this file
#from src.data_ingestion import create_path_to_data
from data_ingestion import create_path_to_data

def read_localization_data():
    data_path = create_path_to_data()
    data = pd.read_csv(f'{data_path}/localization_data.csv.gz', compression='gzip')
    points = gpd.GeoDataFrame({"geometry":gpd.points_from_xy(x=data["Długość geograficzna"], y=data["Szerokość geograficzna"]),
                               "ID": data["ID"], "Nazwa": data["Nazwa"], "Rzeka": data["Rzeka"], "Wysokość n.p.m.": data["Wysokość n.p.m."]})
    points = points.set_crs(epsg=9702)
    points = points.drop(points[points["geometry"].x == points["geometry"].y].index)
    return points

def read_map_data():
    data_path = create_path_to_data()
    mapa = gpd.read_file(f"{data_path}/Wojewodztwa.zip")
    mapa = gpd.GeoDataFrame(mapa, geometry="geometry")
    return mapa

def read_meteo_data():
    data_path = create_path_to_data()
    data = pd.read_csv(f'{data_path}/full_data.csv.gz', compression='gzip', low_memory=False)
    return data