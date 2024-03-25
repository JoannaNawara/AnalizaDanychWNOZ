#comment to run just this file
#from src.plot_map import draw_map
#from src.region_points import choose_region
from plot_map import draw_map
from region_data import choose_region

def region_stations_map(region):
    region_map, region_points = choose_region(region)
    draw_map(region_map, region_points, region)

if __name__ == "__main__":
    region_stations_map("dolnośląskie")