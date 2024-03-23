from src.data_ingestion import prepare_data
from src.plot_map import all_stations_map

def main():
    prepare_data()
    all_stations_map()

if __name__ == "__main__":
    main()