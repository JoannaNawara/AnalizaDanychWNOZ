import pandas as pd
import os
from .region_data import get_region_meteo_data
from .region_map import region_stations_analysis_map, timeline
from .data_ingestion import create_path_to_data
#from region_data import get_region_meteo_data
#from region_map import region_stations_analysis_map, timeline
#from data_ingestion import create_path_to_data

def check_empty_stations(data):
    number = data["Kod stacji"].isnull().sum()
    print(f"{number} of stations don't have any data\n\nThose stations are:")
    print(data[data["Kod stacji"].isnull()]["Nazwa"])
    empty = data[data["Kod stacji"].isnull()]
    data.drop(data[data["Kod stacji"].isnull()].index, inplace=True)
    number = len(data["Kod stacji"].unique())
    print(f"\nAfter deleting them we are left with {number} stations")
    return data, empty

def data_time_span(data):
    time_span = data.groupby("Nazwa")["Rok"].unique()
    time_span = pd.DataFrame(time_span)
    time_span["len"] = [len(row) for row in time_span["Rok"]]
    time_span.reset_index(inplace=True)
    return time_span

def choose_good_stations(data, time_span, region):
    data_30 = data[data["Nazwa"].isin(list(time_span[time_span["len"]>30]["Nazwa"]))]
    print(f"\na) Timeline of {len(data_30['Nazwa'].unique())} stations with more than 30 years of data saved in file 'Timeline_{region}_more_than_30_years_of_data.png'")
    timeline(data_30, "more than 30 years of data", region)
    data_new = data_30[data_30["Nazwa"].isin([row["Nazwa"] for i, row in time_span.iterrows() if sorted(row["Rok"])[-1] == 2022])]
    print(f"\nb) Timeline of {len(data_new['Nazwa'].unique())} stations with data from the last years saved in file 'Timeline_{region}_with_data_from_last_year.png'")
    timeline(data_new, "with data from last year", region)
    diff = [min([sorted(row["Rok"])[j]-sorted(row["Rok"])[j+1] for j in range(len(row["Rok"])-1)], default=-1) for i, row in time_span.iterrows()]
    data_const = data_new[data_new["Nazwa"].isin([row["Nazwa"] for i, row in time_span.iterrows() if diff[i] >= -1])]
    print(f"\nc) Timeline of {len(data_const['Nazwa'].unique())} stations with continuous data on yearly granularity saved in file 'Timeline_{region}_continuous_data.png'")
    timeline(data_const, "continuous data", region)
    return data_const

def analysis_2(region):
    print("\nSecond analysis:\n")
    data = get_region_meteo_data(region)
    print(f"\n1. Checking how mamy stations don't have any data for {region}:")
    data, empty = check_empty_stations(data)
    time_span = data_time_span(data)
    print(f"\n2. Map with station locations and number of years of data saved in file 'Station_locations_{region}_years_n.png'")
    region_stations_analysis_map(region, time_span, empty)
    print(f"\n3. Timeline of station data saved in file 'Timeline_{region}_all.png'")
    timeline(data, "all", region)
    print(f"\n4. As there is a lot of data missing, we will choose the stations with the best timelines:")
    good_data = choose_good_stations(data, time_span, region)
    print(f"\nSaving the data from {len(good_data['Nazwa'].unique())} chosen stations")
    data_path = create_path_to_data()
    if not os.path.isfile(f'{data_path}/{region}_data.csv.gz'):
        good_data.to_csv(f'{data_path}/{region}_data.csv.gz', compression='gzip', index=False)
    print(f"\nData saved in '{region}_data.csv.gz' file")

if __name__ == "__main__":
    analysis_2("dolnośląskie")