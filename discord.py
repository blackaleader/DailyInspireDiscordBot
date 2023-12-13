import discord
import asyncio
import requests
from datetime import datetime, timedelta

TOKEN = ''

def get_quote():
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = response.json()
        return f'"{data["content"]}" - {data["author"]}'
    else:
        return 'Failed to fetch a quote.'

def get_random_unsplash_image():
    url = 'https://source.unsplash.com/random/1200x800'  
    response = requests.get(url)
    if response.status_code == 200:
        return response.url
    else:
        return 'Failed to fetch an image.'
    
client = discord.Client()

async def send_quote():
    channel_id = 1184483588104790086 
    channel = client.get_channel(channel_id)
    quote = get_quote()
    random_unsplash_image = get_random_unsplash_image()
    await channel.send(f"quoute of the day : \n " *{quote}*" ")
    await channel.send(random_unsplash_image)


async def quote_scheduler():
    while True:
        now = datetime.now()
        print
        target_time = now.replace(hour=12, minute=0, second=0, microsecond=0)
        
        if now > target_time:
            target_time += timedelta(days=1)  
        
        delta = target_time - now
        await asyncio.sleep(delta.total_seconds())
        await send_quote()



@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

    client.loop.create_task(quote_scheduler())

# Run the bot
client.run(TOKEN)
