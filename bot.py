import discord
import requests
import time

client = discord.Client()


@client.event
async def on_ready():
    print('Logged on as {0.user}!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$gbf'):
        starttime = time.time()
        S = requests.Session()
        URL = "https://gbf.wiki/api.php"
        TITLE = "Medusa"

        PARAMS = {
            'action': "parse",
            'page': TITLE,
            'format': "json"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        embed = discord.Embed(title="Katalina (Grand)",
                              colour=discord.Colour(0xc9937f),
                              url="https://gbf.wiki/Katalina_(Grand)")

        embed.set_image(
            url="https://gbf.wiki/images/thumb/d/de/Npc_zoom_3040054000_01.png/480px-Npc_zoom_3040054000_01.png")
        embed.set_author(name="Djeeta Bot", url="https://github.com",
                         icon_url="https://gbf.wiki/images/thumb/d/de/Npc_zoom_3040054000_01.png/480px"
                                  "-Npc_zoom_3040054000_01.png")

        embed.add_field(name="Characteristics", value="")
        # Have to account for multiple ougis
        embed.add_field(name="Ougi: Blades of Diamond",
                        value="Massive water damage to a foe. All allies gain 30% Water ATK up and 30% DA up.")

        # Have to account for characters with two or four skills
        embed.add_field(name="Skill 1: Enchanted Lands",
                        value="300%-400% Water damage to a foe (Damage cap: ~620,000). Gain Guaranteed TA.\n**CD**: 7 "
                              "turns; 6 turns\n**Duration**: 1 turn")
        embed.add_field(name="Skill 2: Loengard",
                        value="All allies gain Veil and Refresh. Refresh heals up to 1000 HP the first turn, "
                              "then decreases to 500 → 250 → 150 each turn thereafter.\n**CD**: 9 turns; 8 "
                              "turns\n**Duration**: Refresh: 4 turns")
        embed.add_field(name="Skill 3: Light Wall Divider",
                        value="All allies gain 25% DMG Cut.\n**CD**: 3 turns\n**Duration**: 1 turn")

        # Have to account for characters with more than
        embed.add_field(name="*Path of Duty*",
                        value="Starts battle with Lethal Attack Dodged. 50% boost to ATK and 100% boost to "
                              "DEF when affected by all-elemental DMG cut effect.")
        embed.add_field(name="*Extended Mastery Support Skill*", value="Boost to all allies healing cap.")
        await message.channel.send("Check console log", embed=embed)

        currenttime = time.time()
        print(starttime - currenttime)

client.run('----')
