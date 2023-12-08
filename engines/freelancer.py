import httpx
import re
from bs4 import BeautifulSoup

async def get_freelancer() -> list:

  frelas = []

  stacks = ['java', 'python', 'html','cplusplus-programming', 'c-sharp-programming', 'c-programming']

  for stack in stacks:
    for page in range(1, 10):
      async with httpx.AsyncClient() as client:
        response = await client.get(f'https://www.br.freelancer.com/jobs/{stack}/{page}/?languages=pt,en&results=100')    
        soup = BeautifulSoup(response.text, 'html.parser')

        cells = soup.find_all("div", class_="JobSearchCard-item")
        for cell in cells:
          title = cell.find("a", class_="JobSearchCard-primary-heading-link").get_text(strip=True)
          url = cell.find("a")["href"]
          link = 'https://www.br.freelancer.com' + url
          description = cell.find("p", class_="JobSearchCard-primary-description").get_text().strip()[:500]
          description = re.sub(r'[^\w\s]', '', description)
          description = description.replace(' ', ' ')

          frelas.append([url, title, description, link])

  return frelas
