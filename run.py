from src.data_ingestion import prepare_data
from src.plot_map import all_stations_map
from src.download_data import download_data
from first_analysis import analysis_1

def main():
    #Downloading data
    download_data("https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/")
    #Data ingestion
    prepare_data()
    #Map of all station locations
    all_stations_map()
    #First analysis of data for chosen region
    analysis_1("dolnośląskie")

if __name__ == "__main__":
    main()