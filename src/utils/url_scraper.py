from bs4 import BeautifulSoup

import requests

url = "https://news.google.pt/"

r  = requests.get(url)

data = r.text

soup = BeautifulSoup(data)

str0 = ""
for link in soup.find_all('a'):
    url = (link.get('href'))
    if url == None:
        continue
    str0 += url + "\n"
    
with open("scrape.txt", "w+") as f:
    f.write(str0)