#from src.data_ingestion import read_data, transform_localization, create_path_to_data, prepare_data
from src.data_ingestion import prepare_data

'''
def prepare_data():
    data_path = create_path_to_data()
    data = read_data(data_path)
    data.to_csv(f'{data_path}/full_data.csv.gz', compression='gzip')
    localization = transform_localization(data_path)
    localization.to_csv(f'{data_path}/localization_data.csv.gz', compression='gzip')
'''

def main():
    prepare_data()

if __name__ == "__main__":
    main()