import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 

def read_data_points():
    data = pd.read_csv('dane/localization_data.csv.gz', compression='gzip')
    points = gpd.GeoDataFrame({"geometry":gpd.points_from_xy(x=data["Długość geograficzna"], y=data["Szerokość geograficzna"])})
    points = points.set_crs(epsg=9702)
    points = points.drop(points[points["geometry"].x == points["geometry"].y].index)
    return points

def read_data_map():
    mapa = gpd.read_file("dane/Wojewodztwa.zip")
    mapa = gpd.GeoDataFrame(mapa, geometry="geometry")
    return mapa

def draw_map(mapa, points):
    fig, ax = plt.subplots(1, 1, figsize=(10, 30))
    mapa.plot(ax=ax, color="green")
    points.plot(ax = ax, markersize=2, color="yellow")
    plt.show()

def main():
    points = read_data_points()
    mapa = read_data_map()
    draw_map(mapa, points)

if __name__ == "__main__":
    main()