import discord
import asyncio
import keyring
from discord.ext import commands

from engines.freelancer99 import get_freelancer99
from engines.freelancer import get_freelancer

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
channel_id = 1144974807432183811

sent_freelancer = []

async def search_freelancer():
    '''
    Assynchronous function that searches for new jobs every 60 seconds and sends them to the Discord channel.
    The function searches for vacancies in the following websites:
    * udemy
    '''
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    while not bot.is_closed():
        
        # 99freelas
        results = await get_freelancer99()
        for result in results:
            if result[0] not in sent_freelancer:
                sent_freelancer.append(result[0])
                freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nLINK: {result[3]}'
                await channel.send(freelancer_info)
                await asyncio.sleep(15)
        await asyncio.sleep(30)

        #freelancer
        results = await get_freelancer()
        for result in results:
            if result[0] not in sent_freelancer:
                sent_freelancer.append(result[0])
                freelancer_info = f'{"-"*50}\n\nTRABALHO: {result[1]}\nLINK: {result[3]}'
                await channel.send(freelancer_info)
                await asyncio.sleep(15)
        await asyncio.sleep(30)

        
@bot.event
async def on_ready():
    bot.loop.create_task(search_freelancer())

bot.run(keyring.get_password('bot_freelancer', 'token'))
