import pandas as pd
#from .region_data import get_region_meteo_data
#from .region_map import region_stations_analysis_map
from region_data import get_region_meteo_data
from region_map import region_stations_analysis_map
import matplotlib.pyplot as plt 
import seaborn as sns

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

def timelines(data):
    #times = list(range(min(data["Rok"]), max(data["Rok"])))
    sns.scatterplot(data=data, x="Rok", y="Nazwa", marker="_")
    plt.tick_params(axis='y', labelsize=5)
    plt.show()

def choose_good_stations(data, time_span):
    data_30 = data[data["Nazwa"].isin(list(time_span[time_span["len"]>30]["Nazwa"]))]
    #print([sorted(row)[-1] for row in time_span["Rok"]])
    #print([sorted(row["Rok"])[-1] for i, row in time_span.iterrows() if sorted(row["Rok"])[-1] == 2022])
    data_new = data_30[data_30["Nazwa"].isin([row["Nazwa"] for i, row in time_span.iterrows() if sorted(row["Rok"])[-1] == 2022])]
    timelines(data_new)

def analysis_2(region):
    print("\nSecond analysis:\n")
    data = get_region_meteo_data(region)
    print(f"\n1. Checking how mamy stations don't have any data for {region}:")
    data, empty = check_empty_stations(data)
    time_span = data_time_span(data)
    print(data.groupby("Nazwa").count().sort_values("geometry")["geometry"])
    timelines(data)
    choose_good_stations(data, time_span)
    #region_stations_analysis_map(region, time_span, empty)

if __name__ == "__main__":
    analysis_2("dolnośląskie")