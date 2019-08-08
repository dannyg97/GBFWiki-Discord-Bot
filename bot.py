import discord
import requests
import re
from discord.ext import commands
from bs4 import BeautifulSoup

description = "A GBF Wiki web-scraping tool"
bot = commands.Bot(command_prefix='$', description=description)


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)


@bot.command()
async def art(ctx, *, char: str):
    session = requests.Session()
    api = "https://gbf.wiki/api.php"
    request = char

    parameters = {
        'action': "parse",
        'page': request,
        'format': "json"
    }

    result = session.get(url=api, params=parameters)
    soup = BeautifulSoup(result.content, 'lxml')

    image = soup.find_all(attrs={'srcset': True})
    regex = re.compile(r".png'")
    linkToImage = ""
    for i in image:
        if bool(re.search('01\.png', i['srcset'])):
            linkToImage = i['srcset']
            linkToImage = linkToImage[2:]
            linkToImage = "https://gbf.wiki/" + linkToImage
            break

    embed = discord.Embed(title=request,
                          colour=discord.Colour(0xFFFFFF),
                          url="https://gbf.wiki/" + request)
    embed.set_image(url=linkToImage)

    await ctx.send(embed=embed)


@bot.command()
async def art2(ctx, *, char: str):
    session = requests.Session()
    api = "https://gbf.wiki/api.php"
    request = char

    parameters = {
        'action': "parse",
        'page': request,
        'format': "json"
    }

    result = session.get(url=api, params=parameters)
    soup = BeautifulSoup(result.content, 'lxml')

    image = soup.find_all(attrs={'srcset': True})
    regex = re.compile(r".png'")
    linkToImage = ""
    for i in image:
        if bool(re.search('02\.png', i['srcset'])):
            linkToImage = i['srcset']
            linkToImage = linkToImage[2:]
            linkToImage = "https://gbf.wiki/" + linkToImage
            break

    embed = discord.Embed(title=request,
                          colour=discord.Colour(0xFFFFFF),
                          url="https://gbf.wiki/" + request)
    embed.set_image(url=linkToImage)

    await ctx.send(embed=embed)


@bot.command()
async def art3(ctx, *, char: str):
    session = requests.Session()
    api = "https://gbf.wiki/api.php"
    request = char

    parameters = {
        'action': "parse",
        'page': request,
        'format': "json"
    }

    result = session.get(url=api, params=parameters)
    soup = BeautifulSoup(result.content, 'lxml')

    image = soup.find_all(attrs={'srcset': True})
    regex = re.compile(r".png'")
    linkToImage = ""
    for i in image:
        if bool(re.search('03\.png', i['srcset'])):
            linkToImage = i['srcset']
            linkToImage = linkToImage[2:]
            linkToImage = "https://gbf.wiki/" + linkToImage
            break
    if linkToImage == "":
        await ctx.send('Couldn\'t find 5* FLB art for that character.')
    else:
        embed = discord.Embed(title=request,
                              colour=discord.Colour(0xFFFFFF),
                              url="https://gbf.wiki/" + request)
        embed.set_image(url=linkToImage)
        await ctx.send(embed=embed)

# Change ...
bot.run('-')
