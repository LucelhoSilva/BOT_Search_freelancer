import hikari
from hikari import intents
import asyncio
import keyring
import csv
from engines.freelas99 import get_freelas99
from engines.freelancer import get_freelancer
from engines.workana import get_workana

token = keyring.get_password('discord_freelancer', 'token')
channel_id = keyring.get_password('discord_freelancer', 'channel')

try:
    with open('job_vacancies.csv', 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        sent_freelancer = set(row[3] for row in csv_reader)
except FileNotFoundError:
    sent_freelancer = set()

bot = hikari.GatewayBot(token, intents=intents.Intents.ALL)

@bot.listen()
async def on_started(event: hikari.StartedEvent) -> None:
    '''
    Assynchronous function that searches for new jobs every 63 seconds and sends them to the Discord channel.
    The function searches for vacancies in the following websites:
    * 99freelas
    * Freelancer
    * Workana
    '''
  
    # 99freelas
    results = await get_freelas99()
    with open ('job_vacancies.csv', 'a+', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        for result in results:
            if result[3] not in sent_freelancer:
                sent_freelancer.add(result[3])
                csv_writer.writerow(result)
                freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nSTACK:{result[2]}\nLINK: {result[3]}'
                await bot.rest.create_message(channel_id, freelancer_info)
                await asyncio.sleep(60)
        await asyncio.sleep(30)

    # Freelancer
    results = await get_freelancer()
    with open ('job_vacancies.csv', 'a+', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        for result in results:
            if result[3] not in sent_freelancer:
                sent_freelancer.add(result[3])
                csv_writer.writerow(result)
                freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nLINK: {result[3]}'
                await bot.rest.create_message(channel_id, freelancer_info)
                await asyncio.sleep(60)
        await asyncio.sleep(30)

    # Workana
    results = await get_workana()
    with open ('job_vacancies.csv', 'a+', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        for result in results:
            if result[3] not in sent_freelancer:
                sent_freelancer.add(result[3])
                csv_writer.writerow(result)
                freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nSTACKS: {result[2]}\nLINK: {result[3]}'
                await bot.rest.create_message(channel_id, freelancer_info)
                await asyncio.sleep(60)
        await asyncio.sleep(30)

bot.run()