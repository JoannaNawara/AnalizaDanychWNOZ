import pandas as pd
import numpy as np
from src.data_ingestion import create_path_to_data


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
    data['Data'] = data.apply(create_datetime, axis=1)
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
    filled_data =  pd.concat([data, missing_data], axis=0, keys=list(data.columns))
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

def eda(region):
    print("\nExploratory Data Analysis:\n")
    data_path = create_path_to_data()
    data = pd.read_csv(f'{data_path}/{region}_data.csv.gz', compression='gzip')
    check_null_values(data)
    data = remove_duplicates(data)
    data = change_types(data)

    data = add_missing_rows(data)
    data = fill_null_values(data)

    
    # Do używania po usunięciu złych stacji
    #data = interpolate_values(data)