import discord
import requests
import re
from discord.ext import commands
from bs4 import BeautifulSoup

description = "A Granblue Fantasy Wiki web-scraping bot"
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


@bot.command()
async def info(ctx, *, char: str):
    embed = find_info(char)
    await ctx.send(embed=embed)


def find_info(char: str):
    search_query = init(char)
    soup, url = search_query[0], search_query[1]
    print(f"Page URL: {url}")
    print(f"Gameplay notes: {url}#Gameplay_Notes")

    for span in soup.findAll("span", class_="tooltiptext"):
        span.decompose()

    result = soup.findAll("table", class_='wikitable')

    char_name = result[0].find("div", {"class": "char-name"})
    print(char_name.text)

    # Finds traits
    traits = ""
    for cell in result[1].find_all('a', href=True):
        category_res = re.search('(?<=:).*(?=_)', cell['href'])
        if category_res:
            res = category_res.group(0)
            if len(res) < 10:
                if traits == "":
                    traits += res
                else:
                    traits += ", " + res

    print(f"Traits: {traits}")
    embed = discord.Embed(title=char_name.text, colour=discord.Colour(0xc9937f),
                          url=url, description=("**Traits: **" + traits + "\n" + "[Gameplay notes](" + url + "#Gameplay_Notes)"))

    image = soup.find_all(attrs={'srcset': True})
    linkToImage = ""
    for i in image:
        if bool(re.search("01\.png", i['srcset'])):
            link = re.search('.*?(?=\s)', i['srcset'])
            linkToImage = link.group(0)
            linkToImage = "https://gbf.wiki" + linkToImage
            break
    if linkToImage == "":
        raise ValueError("This type of art for the character does not exist, or the character itself does not exist.\n"
                         "Try checking your spelling.")
    embed.set_image(url=linkToImage)

    # Finds description
    for cell in result[5].find_all('td'):
        print(f"Description: {cell.text}")

    # Finds, formats charge attack
    ca_counter = 0
    ca = ""
    for cell in result[6].find_all('td'):
        if ca_counter not in [0, 3]:    # if they're not the skill icon, then...
            if ca_counter % 3 == 1:     # if it's the charge attack name, then...
                to_string = str(cell.text)
                to_string = re.sub("After 5★:", " ", to_string)
                to_string = re.sub("After 5★", " ", to_string)
                to_string = re.sub("  ", " ", to_string)
                print(f"Charge attack: {to_string}")
                ca = to_string
            else:                       # elif it's the skill description, then...
                to_string = str(cell.text)
                to_string = re.sub("After 5★:", " ", to_string)
                to_string = re.sub(r"\[[0-9]\]", "", to_string)
                to_string = re.sub(r"\.", r"\. ", to_string)
                print(f"Charge attack: {to_string}")
                print(f"{to_string}")
                ca_description = to_string
                if ca != "":
                    if ca_counter > 3:
                        ca_description = "**5★ upgrade:** " + ca_description
                    embed.add_field(name="**Ougi**:" + ca, value=ca_description)

        ca_counter += 1

    # Finds, formats skill details
    skill_counter = 0
    skill = ""
    skill_description = ""
    for cell in result[7].find_all('td'):
        to_print = str(cell.text)
        to_print = re.sub(r"\[[0-9]\]", "", to_print)
        if "enhanced at level" in str(cell.text):
            to_print = re.sub(r"This skill is enhanced at level \d\d.", " ", to_print)
            to_print = re.sub(r"This skill is enhanced again at level \d\d.", " ", to_print)
            to_print = re.sub(r"Complete a Fate Episode to unlock.", " ", to_print)
            print(f"{to_print}")
        elif str(cell.text) == "  ":
            continue
        elif skill_counter % 5 == 0:
            print(f"Skill: {to_print}")
            skill_number = int((skill_counter/5) + 1)
            skill = "**Skill** " + str(skill_number) + ": " + to_print
        elif skill_counter % 5 == 1:
            skill_description = skill_description + "**Cooldown:** " + to_print + "\n"
        elif skill_counter % 5 == 2:
            skill_description = skill_description + "**Duration:** " + to_print + "\n"
        elif skill_counter % 5 == 3:
            skill_description = skill_description + "**Obtained:** " + to_print + "\n"
        elif skill_counter % 5 == 4:
            skill_description = skill_description + to_print
            skill_description = re.sub(r'(?<=[.,:])(?=[^\s])', r' ', skill_description)
            embed.add_field(name=skill, value=skill_description, inline=False)
            skill = ""
            skill_description = ""

        skill_counter += 1

    return embed


def init(search: str):
    """
    Creates the BS4 soup object and the character page URL
    Usage: init("Katalina"); init("Medusa")
    Returns: BS4 soup object, URL (str)
    """
    request_url = "https://gbf.wiki/index.php?search=" + search + "&title=Special%3ASearch&go=Go"
    page = requests.get(request_url)
    return [BeautifulSoup(page.text, "html.parser"), page.url]


# find_art("Medusa", 1); find_art("Esser", 3); find_art("Katalina", 4)
def find_art(unit: str, stage: int):
    #TODO: Create a function that formats the unit name, so people don't have
    # to focus on getting the name right, e.g. katalina summer ==> Katalina_(Summer)
    query = init(unit)
    soup, url = query[0], query[1]
    print(url)

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
            link = re.search('.*?(?=\s)', i['srcset'])
            linkToImage = link.group(0)
            linkToImage = "https://gbf.wiki" + linkToImage
            break
    if linkToImage == "":
        return discord.Embed(description="No such image available - did you do a typo?")

    result = soup.findAll("table", class_='wikitable')
    char_name = result[0].find("div", {"class": "char-name"})
    print(char_name.text)

    embed = discord.Embed(title=char_name.text,
                          colour=discord.Colour(0xFFFFFF),
                          url=url)
    print(linkToImage)
    embed.set_image(url=linkToImage)
    return embed

bot.run('---')
