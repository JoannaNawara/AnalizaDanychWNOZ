import pandas as pd
import re

def read_data():
    # List of months
    years =  list(range(1950, 2023))
    #years = [2000,2023]
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
                path = f'dane/o_d_{month}_{year}.csv'
                df = pd.read_csv(path, na_values=['NA', ''], encoding='cp1250')

                # Set column names
                df.columns = column_names

                # Append the data for the current month to the main DataFrame
                df_all = pd.concat([df, df_all])
        else:
            # Read the data for the current month
            path = f'dane/o_d_{year}.csv'
            df = pd.read_csv(path, na_values=['NA', ''], encoding='cp1250')

            # Set column names
            df.columns = column_names

            # Append the data for the current month to the main DataFrame
            df_all = pd.concat([df, df_all])


    # Display the first few rows of the combined DataFrame
    return df_all

def transform_localization():
    localization = pd.read_csv('dane/kody_stacji.csv', encoding = 'cp1250', delimiter=';')
    localization['Szerokość geograficzna'] = [ int(element[0]) + int(element[1])/60 + int(element[2])/3600 for element in localization['Szerokość geograficzna'].str.split()]
    localization = localization.dropna(subset=['Długość geograficzna'], axis=0)
    regex = re.compile("[0-9][0-9] [0-9][0-9] [0-9][0-9]")
    localization = localization[localization['Długość geograficzna'].str.match('[0-9][0-9] [0-9][0-9] [0-9][0-9]')]
    localization['Długość geograficzna'] = [ int(element[0]) + int(element[1])/60 + int(element[2])/3600 for element in localization['Długość geograficzna'].str.split()]


def main():
    data = read_data()
    data.to_csv('dane/full_data.csv.gz', compression='gzip')
    localization = transform_localization()
    localization.to_csv('dane/localization_data.csv.gz', compression='gzip')
    