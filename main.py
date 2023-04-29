"""
This project was made by Megumi Conde (https://github.com/gvmii) for the Valorant ESP Discord server.
For any questions, contact https://github.com/gvmii or GUMI#1337
"""
import csv
import nextcord
from nextcord.ext import commands
from colorama import just_fix_windows_console
from colorama import Fore, Back, Style
import time

just_fix_windows_console()

# Intents. Do not touch.
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

# Add users following the exact same format as below.
AUTHORIZED_USERS = [
    709932049808752663,  # Lain
    988469766954057738,  # Arisu
    786612352656080907,  # MURPHY
    718168143155036261,  # Mayins
    855212339866632203,  # Katy
    483056864355942405,  # GUMI
]
GUILD_TO_USE = [
    839361178127695922, # My test server
    1084367607982993428 # Valo ESP
]

# Add channel IDs, separated by commas.
CHANNELS_TO_CHECK = [
    1099216827923562568,  # General chat
    839361179892580394  # My test server
]

bot = commands.Bot(
    command_prefix="lain!",
    status=nextcord.Status.do_not_disturb,
    activity=nextcord.Game(name="Bot de moderación por GUMI#1337 and "
                                "Lain#1312"),
    intents=intents,
)


async def get_time():
    seconds = time.time()
    local_time = time.ctime(seconds)
    return local_time


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
    local_time = await get_time()
    if ctx.user.id not in AUTHORIZED_USERS:
        await ctx.response.send_message(
            "https://cdn.discordapp.com/attachments/944802613378035733/1068192404965961738/him.gif",
            ephemeral=True,
        )
        print(f'{Fore.RESET} {local_time} > {Fore.CYAN} {ctx.user} ({ctx.user.id}) {Fore.RESET} -> Read_wordlist. {Fore.RED} NO '
              f'PERMISSIONS.')
    else:
        wordlist = await read_csv_file("wordlist.csv")
        await ctx.response.send_message(wordlist)
        print(f'{Fore.RESET} {local_time} > {Fore.CYAN} {ctx.user} ({ctx.user.id}) {Fore.RESET} -> Read_wordlist.')


@bot.slash_command(guild_ids=GUILD_TO_USE)
async def write_to_wordlist(ctx, msg):
    local_time = await get_time()
    if ctx.user.id not in AUTHORIZED_USERS:
        await ctx.response.send_message(
            "https://cdn.discordapp.com/attachments/944802613378035733/1068192404965961738/him.gif",
            ephemeral=True,
        )
        print(f'{Fore.RESET} {local_time} > {Fore.CYAN} {ctx.user} ({ctx.user.id}) {Fore.RESET} -> Write_to_wordlist. {Fore.RED} '
              f'NO PERMISSIONS.')
    else:
        await write_csv_file("wordlist.csv", msg)
        wordlist = await read_csv_file("wordlist.csv")
        await ctx.response.send_message(wordlist)
        print(f'{Fore.RESET} {local_time} > {Fore.CYAN} {ctx.user} ({ctx.user.id}) {Fore.RESET} -> Write_to_wordlist. | Added '
              f'words: '
              f'{Fore.GREEN} {msg}')


@bot.slash_command(guild_ids=GUILD_TO_USE)
async def delete_from_wordlist(ctx, msg):
    local_time = await get_time()
    if ctx.user.id not in AUTHORIZED_USERS:
        await ctx.response.send_message(
            "https://cdn.discordapp.com/attachments/944802613378035733/1068192404965961738/him.gif",
            ephemeral=True,
        )
        print(f' {Fore.RESET} {local_time} > {Fore.CYAN} {ctx.user} ({ctx.user.id}) {Fore.RESET} -> Delete_from_wordlist.'
              f' {Fore.RED} NO '
              f'PERMISSIONS.')
    else:
        await del_csv_file("wordlist.csv", msg)
        wordlist = await read_csv_file("wordlist.csv")
        await ctx.response.send_message(wordlist)
        print(f' {Fore.RESET} {local_time} > {Fore.CYAN} {ctx.user} ({ctx.user.id}) {Fore.RESET} -> Delete_from_wordlist. | '
              f'Deleted words: '
              f'{Fore.GREEN} {msg}')


@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    words_to_check = await read_csv_file("wordlist.csv")

    # Check if the message was sent in the specified channel
    if ctx.channel.id in CHANNELS_TO_CHECK:
        if ctx.content.lower().startswith(tuple(words_to_check)):
            if ctx.author.id not in AUTHORIZED_USERS:
                local_time = await get_time()
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
                print(
                    f' {Fore.RESET} {local_time} > {Fore.CYAN} {ctx.author} ({ctx.author.id}) {Fore.RESET} -> SENT A '
                    f'BLOCKED WORD. | '
                    f'Deleted '
                    f'content: '
                    f'{Fore.GREEN} {ctx.content}')
    await bot.process_commands(ctx)


print(Fore.RED + "Working. Made by GUMI#1337")
print(Fore.YELLOW + "Working. Made by GUMI#1337")
print(Fore.GREEN + "Working. Made by GUMI#1337")
print(Fore.LIGHTBLUE_EX + "Working. Made by GUMI#1337")
print(Fore.BLUE + "Working. Made by GUMI#1337")
print(Fore.LIGHTMAGENTA_EX + "Working. Made by GUMI#1337")
print(Fore.MAGENTA + "Working. Made by GUMI#1337")
print(Fore.RESET)




bot.run("TOKEN, DO NOT SHARE WITH ANYONE")
