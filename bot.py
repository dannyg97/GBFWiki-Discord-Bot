import discord
import requests
import re
from discord.ext import commands
from bs4 import BeautifulSoup

description = "A GBF Wiki web-scraping bot"
bot = commands.Bot(command_prefix='$', description=description)


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)


@bot.command()
async def art(ctx, *, char: str):
    embed = find_art(char, 1)
    await ctx.send(embed=embed)


@bot.command()
async def art2(ctx, *, char: str):
    embed = find_art(char, 2)
    await ctx.send(embed=embed)


@bot.command()
async def art3(ctx, *, char: str):
    embed = find_art(char, 3)
    await ctx.send(embed=embed)


@bot.command()
async def storyart(ctx, *, char: str):
    embed = find_art(char, 4)
    await ctx.send(embed=embed)


@bot.command()
async def bonusart(ctx, *, char: str):
    embed = find_art(char, 5)
    await ctx.send(embed=embed)


# find_art("Medusa", 1); find_art("Esser", 3); find_art("Katalina", 4)
def find_art(char: str, stage: int):
    session = requests.Session()
    api = "https://gbf.wiki/api.php"

    parameters = {
        'action': "parse",
        'page': char,
        'format': "json"
    }

    result = session.get(url=api, params=parameters)
    soup = BeautifulSoup(result.content, 'lxml')

    regex = ""
    if stage == 1:
        regex = "01\.png"
    elif stage == 2:
        regex = "02\.png"
    elif stage == 3:
        regex = "03\.png"
    elif stage == 4:            # Story Art
        regex = "81\.png"
    elif stage == 5:            # EX/Bonus Art
        regex = "91\.png"

    image = soup.find_all(attrs={'srcset': True})
    linkToImage = ""
    for i in image:
        if bool(re.search(regex, i['srcset'])):
            linkToImage = i['srcset']
            linkToImage = linkToImage[2:]
            linkToImage = "https://gbf.wiki/" + linkToImage
            break
    if linkToImage == "":
        return

    embed = discord.Embed(title=char,
                          colour=discord.Colour(0xFFFFFF),
                          url="https://gbf.wiki/" + char)
    embed.set_image(url=linkToImage)
    return embed


bot.run('-')
