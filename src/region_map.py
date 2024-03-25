#comment to run just this file
from src.plot_map import draw_map
from src.region_data import choose_region
#from plot_map import draw_map
#from region_data import choose_region
import matplotlib.pyplot as plt 

def region_stations_map(region):
    region_map, region_points = choose_region(region)
    draw_map(region_map, region_points, region)

def region_stations_analysis_map(region, data, empty):
    mapa, points = choose_region(region)
    fig, ax = plt.subplots(1, 1, figsize=(10, 30))
    mapa.plot(ax=ax, color="green")
    data.plot(ax=ax, markersize=2, color="yellow")
    empty.plot(ax=ax, markersize=2, color="red")
    ax.set_title(f"Metrological station locations for {region}")
    plt.show()

if __name__ == "__main__":
    region_stations_map("dolnośląskie")