from src.reading_data import read_map_data, read_localization_data 
#from reading_data import read_map_data, read_localization_data
import matplotlib.pyplot as plt 

def draw_map(mapa, points, region):
    fig, ax = plt.subplots(1, 1, figsize=(10, 30))
    mapa.plot(ax=ax, color="green")
    points.plot(ax=ax, markersize=2, color="yellow")
    ax.set_title(f"Metrological station locations for {region}")
    plt.show()

def all_stations_map():
    points = read_localization_data()
    mapa = read_map_data()
    draw_map(mapa, points, "Poland")

if __name__ == "__main__":
    all_stations_map()