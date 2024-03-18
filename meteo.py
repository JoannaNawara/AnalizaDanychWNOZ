from urllib.request import urlretrieve
import requests 
import random
from bs4 import BeautifulSoup 
from urllib.parse import urljoin 
import re

# Get links from website
def get_links(url): 
    response = requests.get(url) 
    bs = BeautifulSoup(response.text, 'html.parser') 
    links = bs.find_all('a', href=True) 
    absolutes = [urljoin(url, link['href']) for link in links] 
    return absolutes 

# Write used links to txt file
def write_results(results, filename):
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
        if re.search("\.zip", link):
            zip_links.append(link)
    return zip_links
        

# load all chosen files
def load_files(zip_links):
    for link in zip_links:
        res = [i for i in range(len(link)) if link.startswith('/', i)]
        division = max(res)
        folder = link[0:division+1]
        file = link[division+1:]

        url = (
            folder
        )
        urlretrieve(url, file)


all_links = get_all_links("https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/")
zip_links = choose_zip(all_links)
write_results(zip_links, 'pobrane_pliki.txt')
load_files(zip_links)