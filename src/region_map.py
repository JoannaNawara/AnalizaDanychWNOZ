import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.lines import Line2D
from .plot_map import draw_map
from .region_data import choose_region
#from plot_map import draw_map
#from region_data import choose_region

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
    points.plot(ax=ax, markersize=points["len"], column="len", legend=True, cmap="spring", legend_kwds={"label":"Number of years"})
    empty.plot(ax=ax, markersize=15, color="red", marker='x')
    handles = Line2D([0], [0], marker='x', color='red', label='Stations without data', markersize=8, linestyle='None'),
    plt.legend(handles=handles)
    ax.set_title(f"Numbers of years of data for metrological station locations in {region} ")
    plt.show()

def timeline(data, title_scope):
    fig, ax = plt.subplots(1, 1, figsize=(10, 30))
    sns.scatterplot(data=data, x="Rok", y="Nazwa", marker="_")
    plt.tick_params(axis='y', labelsize=5)
    ax.set_title(f"Timeline of station data for {title_scope}")
    plt.show()

if __name__ == "__main__":
    region_stations_map("dolnośląskie")