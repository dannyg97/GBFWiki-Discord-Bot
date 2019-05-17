#!/usr/bin/python3

import discord
import requests

client = discord.Client()

@client.event
async def on_ready():
	print('Logged on as {0.user}!'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$gbf'):
		await message.channel.send('Working!')

client.run('NDg0OTU3ODcwNDc1OTY4NTE5.XN7fKw.4dqhQaQti3CzLL9UAFfS_eZkpRU')
