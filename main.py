
import os

import discord
from dotenv import load_dotenv
from discord.utils import get
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MINVOTES = int(os.getenv("MIN_VOTES"))
PINMINVOTES = int(os.getenv("PIN_MIN_VOTES"))

client = discord.Client()

me = 0


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    global me
    me = guild.me
    print(f'{client.user.name} is connected to {guild.name} that has {guild.member_count} members')


@client.event
async def on_message(message):
    print(message)
    if not message.author.bot:
        await message.add_reaction('⬆️')
        await message.add_reaction('⬇️')


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        if reaction.emoji == "⬆️":
            print("new upvote reaction")
        elif reaction.emoji == "⬇️":
            print("new downvote reaction")
        hide, votes = check_if_hide(reaction)
        if hide:
            print("deleting message")
            await reaction.message.delete()

        if check_if_pin(votes):
            print("pining")
            await reaction.message.pin()
            await reaction.message.add_reaction('🏆')
        else:
            await reaction.message.unpin()
            await reaction.message.remove_reaction('🏆', me)


@client.event
async def on_reaction_remove(reaction, user):
    if not user.bot:
        if reaction.emoji == "⬆️":
            print("new upvote reaction")
        elif reaction.emoji == "⬇️":
            print("new downvote reaction")

        hide, votes = check_if_hide(reaction)
        if hide:
            print("deleting message")
            await reaction.message.delete()

        if check_if_pin(votes):
            print("pining")
            await reaction.message.pin()
            await reaction.message.add_reaction('🏆')
        else:
            await reaction.message.unpin()
            await reaction.message.remove_reaction('🏆')


def check_if_pin(votes):
    if votes >= PINMINVOTES:
        return True
    return False


def check_if_hide(reaction):
    reacted_message = reaction.message
    votes = 0
    for r in reacted_message.reactions:
        if r.emoji == "⬆️":
            v = get(reacted_message.reactions, emoji='⬆️')
            votes = votes + v.count
        elif r.emoji == "⬇️":
            v = get(reacted_message.reactions, emoji='⬇️')
            votes = votes - v.count
        print(r.emoji)
    print("v:", votes)
    if votes <= MINVOTES:
        return True, votes
    return False, votes


client.run(TOKEN)
