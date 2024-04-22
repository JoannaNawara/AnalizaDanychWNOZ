from .data_ingestion import create_path_to_data
import pandas as pd
from scipy.stats import gamma, norm
import os

def SPIn(data, n):
    df_months = data.groupby(pd.to_datetime(data.index).to_period('M'))["Suma dobowa opadów [mm]"].sum()
    df_sum = df_months.rolling(n).sum()
    df_sum.dropna(inplace=True)
    ind = df_sum.index
    alpha, loc, beta = gamma.fit(df_sum, floc=0)
    gamma_cdf = gamma.cdf(df_sum, alpha, scale=beta, loc=loc)
    return norm.ppf(gamma_cdf), ind

def get_SPI(region, list_n):
    data_path = create_path_to_data()
    clean_data = pd.read_csv(f'{data_path}/{region}_data_cleaned.csv.gz', compression='gzip')
    stations = clean_data[["ID", "Nazwa", "geometry"]].drop_duplicates()
    for i in list_n:
        SPI_df = pd.DataFrame()
        for id_data, name_data, geo_data in stations.values:
            station_df = clean_data[clean_data["ID"] == id_data]
            station_df.set_index("Data", inplace=True)
            station_df = station_df.dropna(subset=["Suma dobowa opadów [mm]"])
            SPI, ind = SPIn(station_df, i)
            df = pd.DataFrame({"SPI":SPI, "Data":ind, "ID":[id_data]*len(SPI), "Nazwa":[name_data]*len(SPI), "geometry":[geo_data]*len(SPI)})
            SPI_df = pd.concat([SPI_df, df])
        if not os.path.isfile(f'{data_path}/{region}_SPI{i}_data_cleaned.csv.gz'):
            SPI_df.to_csv(f'{data_path}/{region}_SPI{i}_data_cleaned.csv.gz', compression='gzip', index=False)
        print(f"\nData saved in '{region}_SPI{i}_data_cleaned.csv.gz' file")

if __name__ == "__main__":
    get_SPI("dolnośląskie", [1,3,12])