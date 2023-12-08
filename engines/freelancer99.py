import httpx
from bs4 import BeautifulSoup

async def get_freelancer99() -> list:

  frelas = []

  for page in range(1, 70):
    async with httpx.AsyncClient() as client:
      response = await client.get(f'https://www.99freelas.com.br/projects?categoria=web-mobile-e-software&page={page}')
      soup = BeautifulSoup(response.text, "html.parser")
      cells = soup.find_all("li", class_="result-item")
      for cell in cells:
        title = cell.find("h1", class_="title").get_text(strip=True)
        url = cell.find("a")["href"]
        link = "https://www.99freelas.com.br" + url
        description = cell.find("div", class_="item-text description formatted-text").get_text(strip=True)[:1000]

        frelas.append([url,title, description, link])

  return frelas

