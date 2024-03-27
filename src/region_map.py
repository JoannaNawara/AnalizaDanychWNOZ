#comment to run just this file
#from .plot_map import draw_map
#from .region_data import choose_region
from plot_map import draw_map
from region_data import choose_region
import matplotlib.pyplot as plt 

def region_stations_map(region):
    region_map, region_points = choose_region(region)
    draw_map(region_map, region_points, region)

def region_stations_analysis_map(region, time_span, empty):
    mapa, points = choose_region(region)
    fig, ax = plt.subplots(1, 1, figsize=(10, 30))
    not_empty = [i for i, row in points.iterrows() if row["geometry"] not in empty["geometry"]]
    points = points[points.index.isin(not_empty)]
    points = points.merge(time_span, how="inner", on="Nazwa")
    mapa.plot(ax=ax, color="green")
    points.plot(ax=ax, markersize=points["len"], column="len", legend=True, cmap="spring")
    empty.plot(ax=ax, markersize=15, color="red", marker='x')
    ax.set_title(f"Years of data for metrological station locations in {region} ")
    plt.show()

if __name__ == "__main__":
    region_stations_map("dolnośląskie")