"""
This project was made by Megumi Conde (https://github.com/gvmii) for the Valorant ESP Discord server.
For any questions, contact https://github.com/gvmii or GUMI#1337
"""
import csv
import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()

intents.message_content = True
intents.members = True
AUTHORIZED_USERS = 483056864355942405
GUILD_TO_USE = [839361178127695922, 1084367607982993428]

bot = commands.Bot(
    command_prefix="lain!",
    status=nextcord.Status.do_not_disturb,
    activity=nextcord.Game(name="Moderation bot by GUMI#1337 and Lain#1312"),
    intents=intents,
)


async def read_csv_file(filename):
    rows = []
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                for i in row:
                    rows.append(i)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return
    return rows


async def write_csv_file(filename, msg):
    try:
        wordlist = await read_csv_file("wordlist.csv")
        wordlist.append(msg)
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(wordlist)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return


async def del_csv_file(filename, msg):
    try:
        wordlist = await read_csv_file("wordlist.csv")
        wordlist.remove(msg)
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(wordlist)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return


@bot.slash_command(guild_ids=GUILD_TO_USE)
async def read_wordlist(ctx):
    if ctx.user.id != 483056864355942405:
        await ctx.response.send_message(
            "https://cdn.discordapp.com/attachments/944802613378035733/1068192404965961738/him.gif",
            ephemeral=True,
        )
    else:
        wordlist = await read_csv_file("wordlist.csv")
        await ctx.response.send_message(wordlist)


@bot.slash_command(guild_ids=GUILD_TO_USE)
async def write_to_wordlist(ctx, msg):
    if ctx.user.id != 483056864355942405:
        await ctx.response.send_message(
            "https://cdn.discordapp.com/attachments/944802613378035733/1068192404965961738/him.gif",
            ephemeral=True,
        )
    else:
        await write_csv_file("wordlist.csv", msg)
        wordlist = await read_csv_file("wordlist.csv")
        await ctx.response.send_message(wordlist)


@bot.slash_command(guild_ids=GUILD_TO_USE)
async def delete_from_wordlist(ctx, msg):
    if ctx.user.id != 483056864355942405:
        await ctx.response.send_message(
            "https://cdn.discordapp.com/attachments/944802613378035733/1068192404965961738/him.gif",
            ephemeral=True,
        )
    else:
        await del_csv_file("wordlist.csv", msg)
        wordlist = await read_csv_file("wordlist.csv")
        await ctx.response.send_message(wordlist)


@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    words_to_check = await read_csv_file("wordlist.csv")
    channel_to_check = 1099216827923562568  # ID OF CHANNEL

    # Check if the message was sent in the specified channel
    if ctx.channel.id == channel_to_check:
        if ctx.content.lower().startswith(tuple(words_to_check)):
            if ctx.user.id != 483056864355942405:

                user = ctx.author
                await ctx.delete()
                dm_channel = await user.create_dm()
                await dm_channel.send(
                    "**NO PIDAS JUGADORES O BUSQUES PARTIDA EN EL CHAT "
                    "GENERAL.** \n"
                    "Utiliza los canales de buscar jugadores para eso. \n"
                    "Los puedes encontrar en explorar canales, encima de todos "
                    "los canales.\n "
                    "**INSTRUCCIONES:** https://canary.discord.com/channels/1084367607982993428/1099067987291541514/1100082703774257252"
                )
    await bot.process_commands(ctx)


print("Working. Made by GUMI#1337")
bot.run("UR TOKEN HERE IF YOU MAKE THIS PUBLIC UR RETARDED")
