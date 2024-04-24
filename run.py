from src.data_ingestion import prepare_data
from src.plot_map import all_stations_map
from src.download_data import download_data, download_codes
from src.eda import eda
from src.first_analysis import analysis_1
from src.second_analysis import analysis_2
from src.SPI import get_SPI
from src.visualize_spi import describe_region_spi

def main():
    #Downloading data
    download_data("https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/")
    download_codes("https://danepubliczne.imgw.pl/pl/datastore/getfiledown/Arch/Telemetria/Meteo/kody_stacji.csv")
    #Data ingestion
    prepare_data()
    #Map of all station locations
    all_stations_map()
    #First analysis of data for chosen region
    analysis_1("dolnośląskie")
    #Second analysis of data for chosen region
    analysis_2("dolnośląskie")
    # Peparing data for analysis
    eda("dolnośląskie")
    #Counting SPI values for n defined in the list
    get_SPI("dolnośląskie", [1,3,12])
    #Visualizing SPI for the entire region
    describe_region_spi('dolnośląskie')

if __name__ == "__main__":
    main()
