import hikari
from hikari import intents
import asyncio
import keyring

from engines.freelancer99 import get_freelancer99
from engines.freelancer import get_freelancer
from engines.workana import get_workana

bot = hikari.GatewayBot(keyring.get_password('bot_freelancer', 'token'), intents=intents.Intents.ALL)
channel_id = keyring.get_password('bot_freelancer', 'channel')

sent_freelancer = []

@bot.listen()
async def on_started(event: hikari.StartedEvent) -> None:
    '''
    Assynchronous function that searches for new jobs every 60 seconds and sends them to the Discord channel.
    The function searches for vacancies in the following websites:
    * 99freelas
    * Freelancer
    * Workana
    '''
  
    # 99freelas
    results = await get_freelancer99()
    for result in results:
        if result[0] not in sent_freelancer:
            sent_freelancer.append(result[0])
            freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nLINK: {result[3]}'
            await bot.rest.create_message(channel_id, freelancer_info)
            await asyncio.sleep(60)
    await asyncio.sleep(30)

    # Freelancer
    results = await get_freelancer()
    for result in results:
        if result[0] not in sent_freelancer:
            sent_freelancer.append(result[0])
            freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nLINK: {result[3]}'
            await bot.rest.create_message(channel_id, freelancer_info)
            await asyncio.sleep(60)
    await asyncio.sleep(30)

    # Workana
    results = await get_workana()
    for result in results:
        if result[0] not in sent_freelancer:
            sent_freelancer.append(result[0])
            freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nSTACKS: {result[2]}\nLINK: {result[3]}'
            await bot.rest.create_message(channel_id, freelancer_info)
            await asyncio.sleep(60)
    await asyncio.sleep(30)

bot.run()