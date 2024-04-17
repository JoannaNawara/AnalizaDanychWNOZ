from src.data_ingestion import prepare_data
from src.plot_map import all_stations_map
from src.download_data import download_data
from src.eda import eda
from src.first_analysis import analysis_1
from src.second_analysis import analysis_2
from src.SPI import get_SPI

def main():
    #Downloading data
    download_data("https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/")
    #Data ingestion
    prepare_data()
    #Map of all station locations
    all_stations_map()
    #First analysis of data for chosen region
    analysis_1("dolnośląskie")
    #Second analysis of data for chosen region
    analysis_2("dolnośląskie")

    eda("dolnośląskie")
    #Counting SPI values for n defined in the list
    get_SPI("dolnośląskie", [1,3,12])

if __name__ == "__main__":
    main()