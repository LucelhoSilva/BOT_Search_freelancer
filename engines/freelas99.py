import httpx
from bs4 import BeautifulSoup

async def get_freelas99() -> list:

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
        stack = cell.find("p", class_="item-text habilidades")
        if stack:
          stack = ' - '.join(a.get_text(strip=True) for a in stack.find_all("a"))
        else:
          stack = "Não informado"

        frelas.append([url,title,stack,link])

  return frelas

