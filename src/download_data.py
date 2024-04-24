from urllib.request import urlretrieve
import requests 
from bs4 import BeautifulSoup 
from urllib.parse import urljoin 
import re
import zipfile, io
import os
from .data_ingestion import create_path_to_data

repo_path = os.getcwd()

# Get links from website
def get_links(url): 
    response = requests.get(url) 
    bs = BeautifulSoup(response.text, 'html.parser') 
    links = bs.find_all('a', href=True) 
    absolutes = [urljoin(url, link['href']) for link in links] 
    return absolutes 

# Write used links to txt file
def write_results(results):
    filename = repo_path + '\data' + '\loaded_files.txt'
    with open(filename, 'w') as file:
        for i in results:
            file.write(i)
            file.write("\n")

# Get all links from the directory
def get_all_links(url):
    all_links = []
    links = get_links(url)
    for l in links:
        links2 = get_links(l)
        for l2 in links2:
            all_links.append(l2)
    return all_links

# Choose only links with zip
def choose_zip(all_links):
    zip_links = []
    for link in all_links:
        if re.search("\.zip", link) and not re.search("2023", link) and not re.search("2024", link):
            zip_links.append(link)
    return zip_links

# load all chosen files
def load_files(zip_links):
    destination = repo_path + '\data'
    data_path = create_path_to_data()
    for link in zip_links:
        year_l = int(link.split("/")[-1].split("_")[0])
        if year_l <= 2000:
            file = f"o_d_{year_l}.csv"
        else:
            month = link.split("/")[-1].split("_")[1]
            file = f"o_d_{month}_{year_l}.csv"
        if os.path.isfile(data_path+"/"+file):
            continue
        r = requests.get(link)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(destination)

def download_data(url):
    all_links = get_all_links(url)
    print('URLs found\n')
    zip_links = choose_zip(all_links)
    write_results(zip_links)
    print('URLs to zip files chosen and saved in loaded_files.txt\n')
    load_files(zip_links)
    print('csv files loaded to data folder')

def download_codes(link):
    r = requests.get(link).content
    path = create_path_to_data() + '\kody_stacji.csv'
    csv_file = open(path, 'wb')
    csv_file.write(r)
    csv_file.close()

if __name__ == "__main__":
    download_data("https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/")
