from src.data_ingestion import prepare_data
from src.plot_map import all_stations_map
from src.download_data import download_data

def main():
    download_data("https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/")
    prepare_data()
    all_stations_map()

if __name__ == "__main__":
    main()