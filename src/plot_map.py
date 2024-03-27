import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 
from .data_ingestion import create_path_to_data

def read_data_points(folder_path):
    data = pd.read_csv(f'{folder_path}/localization_data.csv.gz', compression='gzip')
    points = gpd.GeoDataFrame({"geometry":gpd.points_from_xy(x=data["Długość geograficzna"], y=data["Szerokość geograficzna"])})
    points = points.set_crs(epsg=9702)
    points = points.drop(points[points["geometry"].x == points["geometry"].y].index)
    return points

def read_data_map(folder_path):
    mapa = gpd.read_file(f"{folder_path}/Wojewodztwa.zip")
    mapa = gpd.GeoDataFrame(mapa, geometry="geometry")
    return mapa

def draw_map(mapa, points):
    fig, ax = plt.subplots(1, 1, figsize=(10, 30))
    mapa.plot(ax=ax, color="green")
    points.plot(ax=ax, markersize=2, color="yellow")
    ax.set_title("Metrological stations' locations")
    plt.show()

def all_stations_map():
    data_path = create_path_to_data()
    points = read_data_points(data_path)
    mapa = read_data_map(data_path)
    draw_map(mapa, points)

if __name__ == "__main__":
    all_stations_map()