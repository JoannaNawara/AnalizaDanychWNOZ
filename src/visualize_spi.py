import pandas as pd
from .data_ingestion import create_path_to_data
from .plot_map import create_path_to_visualizations
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

def plot_SPI_hists(data, region, i):
    path = create_path_to_visualizations()
    n = 0
    fig, ax = plt.subplots(4, 5, figsize=(15, 10))
    for id_station in data["ID"].unique():
        points = data[data["ID"] == id_station]
        name = points["Nazwa"].unique()[0]
        ax[n//5,n%5].tick_params(axis='both', labelsize=5)
        ax[n//5,n%5].hist(points["SPI"])
        ax[n//5,n%5].set(xlim=[-5,5])
        ax[n//5,n%5].set_title(name, size=8)
        n+=1
    ax[3,2].set(xlabel="SPI")
    ax[1,0].set(ylabel="Count")
    plt.suptitle(f"Histograms of SPI{i} values")
    plt.tight_layout(w_pad=None, h_pad=1)
    plt.savefig(f"{path}/SPI_hists_{i}_{region}.png")
    print(f"\nHistograms of SPI{i} values SPI_hists_{i}_{region}.png saved in visualizations folder.\n")

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

def all_hist(data, region, i):
    path = create_path_to_visualizations()
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.hist(data["SPI"])
    ax.set_title(f"Histogram of all SPI{i} values")
    ax.set(xlabel="SPI", ylabel="Count")
    plt.savefig(f"{path}/all_SPI_{i}_hist_{region}.png")
    print(f"\nHistogram of all SPI{i} values all_SPI_{i}_hist_{region}.png saved in visualizations folder.\n")

def all_boxplot(data, region, i):
    path = create_path_to_visualizations()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.boxplot(data["SPI"])
    ax.set_title(f"Boxplot of all SPI{i} values")
    ax.set(ylabel="SPI")
    plt.savefig(f"{path}/all_SPI_{i}_box_{region}.png")
    print(f"\nBoxplot of all SPI{i} values all_SPI_{i}_box_{region}.png saved in visualizations folder.\n")

def all_line(data, region, i):
    path = create_path_to_visualizations()
    data_mean = data.groupby("Data")["SPI"].mean()
    data_min = data.groupby("Data")["SPI"].min()
    data_max = data.groupby("Data")["SPI"].max()
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.plot(data_min.index, data_min.values, color="cornflowerblue", label="Min")
    ax.plot(data_max.index, data_max.values, color="limegreen", label="Max")
    ax.plot(data_mean.index, data_mean.values, color="orange", label="Mean")
    ax.set_title(f"Lineplots of all SPI{i} values")
    ax.set(ylabel="SPI", xlabel="Data")
    plt.legend()
    plt.savefig(f"{path}/all_SPI_{i}_lines_{region}.png")
    print(f"\nLineplots of all SPI{i} values all_SPI_{i}_lines_{region}.png saved in visualizations folder.\n")

def describe_region_spi(region):
    for i in [1, 3, 12]:
        data = load_spi_data(region, i)
        print(f"Statystyczne podsumowanie wyników SPI-{i} dla {region}:")
        print(data['SPI'].describe())
        visualize_variability(data, region, i)
        visualize_statistics(data, region, i)
        plot_SPI_hists(data, region, i)
        all_hist(data, region, i)
        all_boxplot(data, region, i)
        all_line(data, region, i)

if __name__ == "__main__":
    describe_region_spi('dolnośląskie')