import pandas as pd
import re
import os

def read_data(folder_path):
    # List of months
    years =  list(range(1950, 2023))
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    # List of column names
    column_names = ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Suma dobowa opadów [mm]', 'Status pomiaru SMDB', 
                    'Rodzaj opadu       [S/W/ ]', 'Wysokość pokrywy śnieżnej [cm]', 'Status pomiaru PKSN', 'Wysokość świeżospadłego śniegu [cm]',
                   'Status pomiaru HSS', 'Gatunek śniegu  [kod]', 'Status pomiaru GATS', 'Rodzaj pokrywy śnieżnej [kod]', 'Status pomiaru RPSN' ]


    # Create an empty DataFrame to store the results
    df_all = pd.DataFrame()

    # Loop over the years
    for year in years:
        if year >= 2001:
            # Loop over the months
            for month in months:
                # Read the data for the current month
                path = f'{folder_path}/o_d_{month}_{year}.csv'
                df = pd.read_csv(path, na_values=['NA', ''], encoding='cp1250')

                # Set column names
                df.columns = column_names

                # Append the data for the current month to the main DataFrame
                df_all = pd.concat([df, df_all])
        else:
            # Read the data for the current month
            path = f'{folder_path}/o_d_{year}.csv'
            df = pd.read_csv(path, na_values=['NA', ''], encoding='cp1250')

            # Set column names
            df.columns = column_names

            # Append the data for the current month to the main DataFrame
            df_all = pd.concat([df, df_all])


    # Display the first few rows of the combined DataFrame
    return df_all

def transform_localization(folder_path):
    localization = pd.read_csv(f'{folder_path}\kody_stacji.csv', encoding = 'cp1250', delimiter=';')
    localization['Szerokość geograficzna'] = [ int(element[0]) + int(element[1])/60 + int(element[2])/3600 for element in localization['Szerokość geograficzna'].str.split()]
    localization = localization.dropna(subset=['Długość geograficzna'], axis=0)
    localization = localization[localization['Długość geograficzna'].str.match('[0-9][0-9] [0-9][0-9] [0-9][0-9]')]
    localization['Długość geograficzna'] = [ int(element[0]) + int(element[1])/60 + int(element[2])/3600 for element in localization['Długość geograficzna'].str.split()]
    return localization


def create_path_to_data():
    current_path = os.getcwd()
    current_path = current_path + '\data'
    return current_path

def prepare_data():
    data_path = create_path_to_data()
    print("Reading data")
    data = read_data(data_path)
    data.to_csv(f'{data_path}/full_data.csv.gz', compression='gzip')
    print("Full data saved")
    print("Reading localization data")
    localization = transform_localization(data_path)
    localization.to_csv(f'{data_path}/localization_data.csv.gz', compression='gzip')
    print("Localization data saved")

if __name__ == "__main__":
    prepare_data()
    