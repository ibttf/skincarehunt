import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.cvs.com", timeout=5)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)