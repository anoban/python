import os
import sys
import requests
from bs4 import BeautifulSoup

URL = "https://www.ers.usda.gov/data-products/fruit-and-vegetable-prices.aspx"

response = requests.get(URL)
response.status_code
response.text
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find_all("table", attrs = {"class" : "usa-table usa-table--striped usa-table--stacked-header usa-table--borderless"})[0]
links = [tag.find_all("a", attrs = {"target" : "_blank"}) for tag in table.find_all("td") if len(tag.find_all("a", attrs = {"target" : "_blank"})) != 0]

links[0]
len(links[0])
