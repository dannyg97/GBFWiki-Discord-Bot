import discord
import requests
import time
from bs4 import BeautifulSoup

client = discord.Client()


@client.event
async def on_ready():
    print('Logged on as {0.user}!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$gbf'):
        startTime = time.time()
        s = requests.Session()
        api = "https://gbf.wiki/api.php"
        request = "Medusa"                    # Change this to be arg {whatever} later

        # Have a function here that makes changes to the title
        # For now, we'll make it such that it only accepts (basic) characters

        parameters = {
            'action': "parse",
            'page': request,
            'format': "json"
        }

        result = s.get(url=api, params=parameters)
        data = result.json()
        embed = discord.Embed(title="Katalina (Grand)",
                              colour=discord.Colour(0xFFFFFF),
                              url="https://gbf.wiki/Katalina_(Grand)")
        await message.channel.send(embed=embed)

        # Calculate the duration of the request
        currentTime = time.time()
        print(currentTime - startTime)


# Change ...
client.run('NDg0OTU3ODcwNDc1OTY4NTE5.XN7fKw.4dqhQaQti3CzLL9UAFfS_eZkpRU')
