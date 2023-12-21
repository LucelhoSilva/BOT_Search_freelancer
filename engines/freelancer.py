import httpx
import re
from bs4 import BeautifulSoup

async def get_freelancer() -> list:

  frelas = []

  stacks = ['python', 'javascript', 'java', 'c++', 'c#', 'c', 'php', 'ruby', 'sql', 'mysql', 'postgresql', 'oracle', 'linux', 'unix', 'aws', 'azure', 'docker', 'ansible', 'nginx', 'apache', 'sysadmin', 'cloud', 'front-end', 'back-end', 'full-stack', 'cybersegurança', 'devops','pentest']

  for stack in stacks:
    for page in range(0, 10):
      async with httpx.AsyncClient() as client:
        response = await client.get(f'https://www.br.freelancer.com/jobs/{stack}/{page}/?languages=pt,en&results=100')    
        soup = BeautifulSoup(response.text, 'html.parser')

        cells = soup.find_all("div", class_="JobSearchCard-item")
        for cell in cells:
          title = cell.find("a", class_="JobSearchCard-primary-heading-link").get_text(strip=True)
          url = cell.find("a")["href"]
          link = 'https://www.br.freelancer.com' + url
          stack = cell.find("div", class_="JobSearchCard-primary-tags")
          if stack:
            stack = ' - '.join(a.get_text(strip=True) for a in stack.find_all("a"))
          else:
            stack = "Não informado"
          frelas.append([url, title, stack, link])

  return frelas
