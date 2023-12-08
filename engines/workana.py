import requests
from bs4 import BeautifulSoup

def get_workana():
  
  url= 'https://www.workana.com/jobs?category=it-programming'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  print(soup)

  cells = soup.find_all("div", id_="projects")
  print(cells)

get_workana()