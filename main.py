#!/usr/bin/env python3

import random
import asyncio
import discord
import requests
from discord import Member, Embed

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()

intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def attachments_to_files(attached,spoiler=False):
	filelist = []
	for i in attached:
		file = await i.to_file()
		filelist.insert(len(filelist),file)
	return filelist

async def morelikeend(morelike, original, message):
    if morelike.lower() == original.lower():
        await message.channel.send(f"{original} is perfect, it cannot be changed")
    else:
        await message.channel.send(f"{original}? more like {morelike}")

@client.event
async def on_ready():
	print("hello world!")

prefix = "!"

@client.event
async def on_message(message):

    compliments = ["nice shirt", "did you get a haircut today because i think you look GREAT", "wow, so cool", f"lookin good, {message.author.name}"]

    args = message.content.lower
    args = message.content.replace(prefix,"")
    argslist = args.split(" ")

    if ("ping" in argslist):
        await message.channel.send("pong!")

    if message.content.startswith(prefix):
        if (argslist[0] == "compliment"):
            await message.channel.send(compliments[random.randrange(len(compliments))])
        elif (argslist[0] == "pfp"):
            if not (message.author.id == 436985877806317586):
                await message.channel.send(f"https://cdn.discordapp.com/avatars/{client.user.id}/{client.user.avatar}.png")
                return
            try:
                if (argslist[2] == "reset"):
                    await message.channel.send("reseting pfp...")
                    await client.user.edit(avatar=open('images/resetpfp.png', 'rb').read())
                    await message.channel.send("pfp has been reset back to normal")
            except IndexError:
                try:
                    try:
                        open('images/newpfp.png', 'wb').write(requests.get(message.attachments[0].url, allow_redirects=True).content)
                        await message.channel.send("changing pfp...")
                        await client.user.edit(avatar=open('images/newpfp.png', 'rb').read())
                        await message.channel.send("pfp has been changed")
                    except discord.errors.HTTPException:
                        await message.channel.send("You are changing your avatar too fast. Try again later.")
                except IndexError:
                    await message.channel.send(f"https://cdn.discordapp.com/avatars/{client.user.id}/{client.user.avatar}.png")

client.run(token)