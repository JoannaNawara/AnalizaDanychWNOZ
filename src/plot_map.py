from .reading_data import read_map_data, read_localization_data 
#from reading_data import read_map_data, read_localization_data
import matplotlib.pyplot as plt 
import os

def create_path_to_visualizations():
    current_path = os.getcwd()
    vis_path = current_path + '\\visualizations'
    if not os.path.exists(vis_path):
        os.makedirs(vis_path)
    return vis_path

def draw_map(mapa, points, region):
    path = create_path_to_visualizations()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    mapa.plot(ax=ax, color="green")
    points.plot(ax=ax, markersize=2, color="yellow")
    ax.set_title(f"Metrological station locations for {region}")
    plt.savefig(f"{path}/Station_locations_{region}.png")

def all_stations_map():
    points = read_localization_data()
    mapa = read_map_data()
    draw_map(mapa, points, "Poland")
    print(f"\nMap with station locations saved in file 'Station_locations_Poland.png'")

if __name__ == "__main__":
    all_stations_map()