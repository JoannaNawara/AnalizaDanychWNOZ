import pandas as pd
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

def choose_good_stations(data, time_span):
    data_30 = data[data["Nazwa"].isin(list(time_span[time_span["len"]>30]["Nazwa"]))]
    print(f"\na) Timeline of stations with more than 30 years of data in new window")
    timeline(data_30, "stations with more than 30 years of data")
    data_new = data_30[data_30["Nazwa"].isin([row["Nazwa"] for i, row in time_span.iterrows() if sorted(row["Rok"])[-1] == 2022])]
    print(f"\nb) Timeline of stations with data from the last years in new window")
    timeline(data_new, "stations with data from the last year")
    diff = [min([sorted(row["Rok"])[j]-sorted(row["Rok"])[j+1] for j in range(len(row["Rok"])-1)], default=-1) for i, row in time_span.iterrows()]
    data_const = data_new[data_new["Nazwa"].isin([row["Nazwa"] for i, row in time_span.iterrows() if diff[i] >= -1])]
    print(f"\nc) Timeline of stations with continuous data")
    timeline(data_const, "stations with continuous data")
    return data_const

def analysis_2(region):
    print("\nSecond analysis:\n")
    data = get_region_meteo_data(region)
    print(f"\n1. Checking how mamy stations don't have any data for {region}:")
    data, empty = check_empty_stations(data)
    time_span = data_time_span(data)
    print(f"\n2. Map with station locations and number of years of data in new window")
    region_stations_analysis_map(region, time_span, empty)
    print(f"\n3. Timeline of station data in new window")
    timeline(data, "all stations")
    print(f"\n4. As there is a lot of data missing, we will choose the stations with the best timelines:")
    good_data = choose_good_stations(data, time_span)
    print(f"\nSaving the data from {len(good_data['Nazwa'].unique())} chosen stations to a new file")
    data_path = create_path_to_data()
    good_data.to_csv(f'{data_path}/chosen_stations_data.csv.gz', compression='gzip', index=False)

if __name__ == "__main__":
    analysis_2("dolnośląskie")