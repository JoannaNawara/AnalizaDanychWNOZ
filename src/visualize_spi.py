import pandas as pd
from .data_ingestion import create_path_to_data
from .plot_map import create_path_to_visualizations
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def load_spi_data(region, i):
    data_path = create_path_to_data()
    data = pd.read_csv(f'{data_path}/{region}_SPI{i}_data_cleaned.csv.gz', compression='gzip')
    # find limitations
    stations_start_end = data.groupby('ID')['Data'].agg(['min', 'max'])
    stations_start_end.columns = ["Start_date", "End_date"]
    first_date = stations_start_end['Start_date'].max()
    last_date = stations_start_end['End_date'].min()
    # filter the data
    data = data[data['Data'] >= first_date]
    data = data[data['Data'] <= last_date]
    return data

def visualize_variability(data, region, i):
    path = create_path_to_visualizations()
    grouped_data = data.groupby('Nazwa')
    plt.figure(figsize=(8, 6))
    for station, station_data in grouped_data:
        plt.plot(station_data['Data'], station_data['SPI'], label=station)

    plt.xlabel('Data')
    plt.ylabel('SPI')
    plt.title(f'Precipitation variability of SPI-{i} for all stations')
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.savefig(f"{path}/Precipitation variability of SPI-{i} for all stations_{region}.png", bbox_inches='tight')
    print(f"\nPrecipitation variability of SPI-{i} for all stations_{region}.png in visualizations folder.\n")

def visualize_statistics(data, region, i):
    path = create_path_to_visualizations()
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, x="Nazwa", y="SPI")
    plt.title(f"Boxplots of SPI-{i} for each station")
    plt.xticks(rotation=90)
    plt.savefig(f"{path}/Boxplots of SPI-{i} for each station_{region}.png", bbox_inches='tight')
    print(f"\nBoxplots of SPI-{i} for each station_{region}.png in visualizations folder.\n")

def describe_region_spi(region):
    for i in [1, 3, 12]:
        data = load_spi_data(region, i)
        print(f"Statystyczne podsumowanie wyników SPI-{i} dla {region}:")
        print(data['SPI'].describe())
        visualize_variability(data, region, i)
        visualize_statistics(data, region, i)

if __name__ == "__main__":
    describe_region_spi('dolnośląskie')