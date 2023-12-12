import httpx
from bs4 import BeautifulSoup
import json
import hashlib

async def get_workana():
    '''
    DOCSTRING
    '''

    jobs = []

    for page in range(1):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://www.workana.com/jobs?category=it-programming&language=pt&page={page}')

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                cells = soup.find_all('div', class_='project-item')
                for cell in cells:
                    title = cell.find('h2').get_text(strip=True)
                    date = cell.find('h5')['title']
                    code = f'{title} - {date}'
                    code = hashlib.sha256(code.encode()).hexdigest()

                    skills = cell.find('div', class_='skills')
                    to_expand = skills.find('label-expander').get(':to-expand')
                    skills = json.loads(to_expand)
                    stacks = [skill['anchorText'] for skill in skills]

                    link = cell.find('a')['href']
                    link = f'https://www.workana.com{link}'

                    job = [code, title, stacks, link]
                    jobs.append(job)

    return jobs