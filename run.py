from src.data_ingestion import prepare_data
from src.plot_map import all_stations_map
from src.download_data import download_data
from src.eda import eda

def main():
    #download_data("https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/")
    #prepare_data()
    #all_stations_map()
    eda("dolnośląskie")

if __name__ == "__main__":
    main()