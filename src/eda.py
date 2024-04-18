import pandas as pd
import numpy as np
from .data_ingestion import create_path_to_data
from .plot_map import create_path_to_visualizations
import matplotlib.pyplot as plt
import seaborn as sns
import os

def check_null_values(data):
    print('Amount of null values in each column:')
    print(data.isnull().sum())

def remove_duplicates(data):
    old = data.shape[0]
    data.drop_duplicates(subset=['ID', 'Rok', 'Miesiąc', 'Dzień'], keep='last', inplace=True)
    new = data.shape[0]
    print(f'\nRemoving duplicates: found {old-new} duplicates')
    return data

def change_types(data):
    print('\nChanging column types:')
    data['ID'] = data['ID'] .map(str)
    data['Kod stacji'] = data['Kod stacji'] .map(str)
    data['Rok'] = data['Rok'] .map(int)
    data['Miesiąc'] = data['Miesiąc'] .map(int)
    data['Dzień'] = data['Dzień'] .map(int)
    data['Gatunek śniegu  [kod]'] = data['Gatunek śniegu  [kod]'] .map(str)
    print(data.dtypes)
    return data

def remove_missing_measures(data):
    return data[data['Status pomiaru SMDB']!=8]

def create_date_range(data):
    data_start = data[['Rok', 'Miesiąc', 'Dzień']].min()
    data_end = data[['Rok', 'Miesiąc', 'Dzień']].max()
    data_start = pd.to_datetime(f"{data_start['Rok']}-{data_start['Miesiąc']}-{data_start['Dzień']}", format='%Y-%m-%d')
    data_end = pd.to_datetime(f"{data_end['Rok']}-{data_end['Miesiąc']}-{data_end['Dzień']}", format='%Y-%m-%d')
    date_range = pd.date_range(start=data_start, end=data_end, freq='D')
    return pd.DataFrame(date_range, columns=['Data'])

def choose_locations_data(data):
    return data[['geometry', 'ID', 'Nazwa', 'Rzeka', 'Wysokość n.p.m.', 'Kod stacji', 'Nazwa stacji']].drop_duplicates()

def create_datetime(row):
    return f"{row['Rok']}-{row['Miesiąc']}-{row['Dzień']}"

def create_full_data_pattern(data_locations, date_range):
    full_data = data_locations.join(date_range, how='cross')
    full_data['Suma dobowa opadów [mm]'] = np.nan
    full_data['Status pomiaru SMDB'] = 8
    full_data['Rodzaj opadu       [S/W/ ]'] = 'nieznany'
    full_data['Wysokość pokrywy śnieżnej [cm]'] = 0
    full_data['Status pomiaru PKSN'] = 8
    full_data['Wysokość świeżospadłego śniegu [cm]'] = 0
    full_data['Status pomiaru HSS'] = 8
    full_data['Gatunek śniegu  [kod]'] = 'brak śniegu'
    full_data['Status pomiaru GATS'] = 8
    full_data['Rodzaj pokrywy śnieżnej [kod]'] = 'brak śniegu'
    full_data['Status pomiaru RPSN'] = 8
    return full_data

def create_year(row):
    return row['Data'].year

def create_month(row):
    return row['Data'].month

def create_day(row):
    return row['Data'].day

def add_date_column(data):
    data = data.assign(Data=data.apply(create_datetime, axis=1).values)
    data['Data'] = pd.to_datetime(data['Data'], format='%Y-%m-%d')
    return data

def get_missing_data(full_data_pattern, data):
    df_merged = full_data_pattern.merge(data[['ID', 'Data']], how='left', on=['ID', 'Data'], indicator=True)
    missing_data = df_merged[df_merged['_merge'] == 'left_only'].drop('_merge', axis=1)
    missing_data['Rok'] = missing_data.apply(create_year, axis=1)
    missing_data['Miesiąc'] = missing_data.apply(create_month, axis=1)
    missing_data['Dzień'] = missing_data.apply(create_day, axis=1)
    return missing_data

def add_missing_rows(data):
    data = remove_missing_measures(data)
    date_range = create_date_range(data)
    data_locations = choose_locations_data(data)
    full_data_pattern = create_full_data_pattern(data_locations, date_range)
    data = add_date_column(data)
    missing_data = get_missing_data(full_data_pattern, data)
    filled_data =  pd.concat([data, missing_data], axis=0)
    return filled_data

def fill_null_values(data):
    data['Rodzaj opadu       [S/W/ ]'] = data['Rodzaj opadu       [S/W/ ]'].fillna('nieznany')
    data['Gatunek śniegu  [kod]'] = data['Gatunek śniegu  [kod]'].fillna('brak śniegu')
    data['Rodzaj pokrywy śnieżnej [kod]'] = data['Rodzaj pokrywy śnieżnej [kod]'].fillna('brak śniegu')
    data['Wysokość pokrywy śnieżnej [cm]'] = data['Wysokość pokrywy śnieżnej [cm]'].fillna(0)
    data['Wysokość świeżospadłego śniegu [cm]'] = data['Wysokość świeżospadłego śniegu [cm]'].fillna(0)
    return data

def interpolate_values(data):
    columns = data.columns
    locations = data['ID'].unique()
    list_df = []
    for location in locations:
        location_data = data[data['ID']==location]
        location_data = location_data.set_index('Data')
        location_data['Suma dobowa opadów [mm]'] = location_data['Suma dobowa opadów [mm]'].interpolate('index')
        list_df.append(location_data)

    return pd.concat(list_df)

def correct_interpolate(data, stations_start_end):
    data = data.reset_index()
    # Make sure the data is in datetime format
    data.loc[:,'Data'] = pd.to_datetime(data['Data'])
    
    # Filter data based on start and end dates
    for location, start_end in stations_start_end.iterrows():
        start_date = pd.to_datetime(start_end['Start_date'])
        end_date = pd.to_datetime(start_end['End_date'])
        
        condition = (data['ID'] == location) & ((data['Data'] < start_date) | (data['Data'] > end_date))
        # Replace values with NaN for rows that are out of range of the start and end dates
        # For dates where stations where not measuring yet or already stopped
        data.loc[condition, 'Suma dobowa opadów [mm]'] = np.nan

    return data

def get_stations_start_end(data_original):
    # Get start and end dates for each station
    data_original = add_date_column(data_original)
    stations_start_end = data_original.groupby('ID')['Data'].agg(['min', 'max'])
    stations_start_end.columns = ["Start_date", "End_date"]
    return stations_start_end

def filter_by_number_of_nulls_in_row(data, stations_start_end, threshold=30):
    nulls_in_row = pd.DataFrame(index=data['ID'].unique(), columns = {'max':[], 'mean':[], 'min':[], 'median':[]})

    # Iterate through each station
    for station in data['ID'].unique():
        chosen_id_data = data[data['ID'] == station]
        chosen_id_data.reset_index(inplace=True, drop=True)
        # Filter by start and end date of collecting data by station
        chosen_id_data = chosen_id_data[(pd.to_datetime(chosen_id_data['Data']) > pd.to_datetime(stations_start_end.loc[station]['Start_date'])) & (pd.to_datetime(chosen_id_data['Data']) < pd.to_datetime(stations_start_end.loc[station]['End_date']))]
        chosen_id_data = chosen_id_data.sort_values(by='Data', ascending=True)
        # Count number of nulls in a row
        chosen_id_data['group'] = (~chosen_id_data['is_null']).cumsum().values
        null_sequence_lengths = chosen_id_data.groupby('group').size() - 1

        # Find max, min, mean, median nulls in a row 
        nulls_in_row.loc[station,'max'] = null_sequence_lengths.max()
        nulls_in_row.loc[station,'min'] = null_sequence_lengths.min()
        nulls_in_row.loc[station,'mean'] = null_sequence_lengths.mean()
        nulls_in_row.loc[station,'median'] = null_sequence_lengths.median()

    # Choose stations with less than 30 nulls in a row - default
    chosen_stations = list(nulls_in_row[nulls_in_row['max'] <= threshold].index)
    data_filtered = data[data.ID.isin(chosen_stations)]

    return data_filtered

def plot_nulls_percent(data, stations_start_end, region):
    data['is_null'] = data['Suma dobowa opadów [mm]'].isnull()
    for station in data['ID'].unique():
        station_data = data[data['ID'] == station]
        station_data = data[(pd.to_datetime(data['Data']) > pd.to_datetime(stations_start_end.loc[station]['Start_date'])) & (pd.to_datetime(data['Data']) < pd.to_datetime(stations_start_end.loc[station]['End_date']))]
        stations_start_end.loc[station,'Null%'] = station_data['is_null'].sum()/len(station_data)

    path = create_path_to_visualizations()
    plt.figure(figsize=(10, 10))
    sns.scatterplot(x='ID', y='Null%', data=stations_start_end, color='seagreen')
    plt.xlabel('ID')
    plt.ylabel('Null Percentage')
    plt.title('Null Percentage for Each ID')
    plt.xticks(rotation=45)  
    plt.grid(True)
    plt.savefig(f"{path}/Null_percantage_station_{region}.png")
    print(f"\nPlot saved as Null_percantage_station_{region}.png in visualizations folder.\n")

def get_description(data):
    print(data[["Suma dobowa opadów [mm]", "Status pomiaru SMDB", "Wysokość pokrywy śnieżnej [cm]", 
    "Status pomiaru PKSN", "Wysokość świeżospadłego śniegu [cm]", "Status pomiaru HSS", "Status pomiaru GATS", "Status pomiaru RPSN"]].describe())

def eda(region):
    print("\nExploratory Data Analysis:\n")
    data_path = create_path_to_data()
    print("Reading data...")
    data_original = pd.read_csv(f'{data_path}/{region}_data.csv.gz', compression='gzip', low_memory=False)
    print("Data loaded\n")

    check_null_values(data_original)
    
    data = remove_duplicates(data_original)
    data = change_types(data)

    print("Cleaning data...\n")
    data = add_missing_rows(data)
    data = fill_null_values(data)
    
    stations_start_end = get_stations_start_end(data_original)
    print("\nPreparing plot for null values percentage...")
    plot_nulls_percent(data, stations_start_end, region)

    print("Filtering data...\n")
    data_filtered = filter_by_number_of_nulls_in_row(data, stations_start_end, threshold=30)
    print("Data filtered.\n")

    print("Interpolating values...\n")
    data_filtered = interpolate_values(data_filtered)
    data_filtered = correct_interpolate(data_filtered, stations_start_end)
    print("Data is transformed and cleaned")

    if not os.path.isfile(f'{data_path}/{region}_data_cleaned.csv.gz'):
        data_filtered.to_csv(f'{data_path}/{region}_data_cleaned.csv.gz', compression='gzip', index=False)
    print(f"\nData saved in '{region}_data.csv.gz' file")


