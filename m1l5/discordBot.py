import random as r
import discord
from discord.ext import commands
import ast
from settings import settings
import os
import requests
import time

intents = discord.Intents.default()
intents.message_content = True
botPrefix = '!'
bot = commands.Bot(command_prefix=botPrefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Hello! I am {bot.user}')
@bot.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
        await guild.system_channel.send(to_send)

@bot.command()
async def random(ctx, min_val = commands.parameter(default=0,description="Minimal value"), max_val = commands.parameter(default=None,description="Maximal value")):
    '''
    Outputs a random number in a given range.
    Examples:
    --------------------------------------------
    -input- !random 100
    -output- Random number between 0 and 100: 5
    --------------------------------------------
    -input- !random 10 100
    -output- Random number between 10 and 100: 15
    --------------------------------------------
    '''
    if max_val is None:
        max_val = min_val
        min_val = 0

    try:
        min_val = int(min_val)
        max_val = int(max_val)
        random_number = r.randint(min_val, max_val)
        await ctx.send(f"Random number between {min_val} and {max_val}: {random_number}")
    except ValueError:
        await ctx.send("Invalid range. Please enter valid numbers.")
@bot.command()
async def dice(ctx):
    '''
    Tosses the dice.
    Example: 
    --------------------------------------------
    -input- !dice
    -output- Dice fell out: :two: and :three:
    --------------------------------------------
    '''
    numbersDice = [':one:', ':two:', ':two:', ':four:', ':five:', ':six:']
    dice1 = r.choice(numbersDice)
    dice2 = r.choice(numbersDice)
    await ctx.send(f"Dice fell out: {dice1} and {dice2}")
@bot.command()
async def headtail(ctx):
    '''
    Flipping a coin. 
    Example:
    --------------------------------------------
    -input- !headtail
    -output- You flipped a coin... Tail!
    --------------------------------------------
    '''
    resultHT = r.choice(['Head', 'Tail'])
    await ctx.send(f"You flipped a coin... {resultHT}!")
@bot.command()
async def choice(ctx, seq = commands.parameter(description="List (with format like in example)") ):
    '''
    Chooses random element in a given list. 
    Example: 
    --------------------------------------------
    -input- !choice banana,mango,apple (***list without spaces***)
    -output- I think banana is the best option!
    --------------------------------------------
    '''
    userListNew = "'" + seq.replace(',', "','") + "'"
    try:
        newlist = ast.literal_eval(userListNew)
        resultChoice = r.choice(newlist)
        await ctx.send(f"I think {resultChoice} is the best option!")
    except Exception:
        await ctx.send("Invalid format. Please enter valid list.")
@bot.command()
async def pswgen(ctx, amount = commands.parameter(default=8,description="Amount of symbols in password")):
    '''
    Generate powerful password. 
    Example: 
    --------------------------------------------
    -input- !pswgen 8
    -output- Your generated password: Y3_#83
    --------------------------------------------
    '''
    upper_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 's', 'y', 'x', 'z']
    lower_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'S', 'Y', 'X', 'Z']
    symbols = ['!','@','#','$','(',')','_']
    numbers = [1,2,3,4,5,6,7,8,9,0]
    password = ''
    for i in range(int(amount)):
        letter = r.randint(1, 5)
        if letter == 1:
            password = password + r.choice(upper_case)
        elif letter == 2:
            password = password + r.choice(lower_case)
        elif letter == 3:
            password = password + r.choice(symbols)
        elif letter == 4:
            password = password + str(r.choice(numbers))
    await ctx.send(f"Your generated password: || {password} ||")
@bot.command()
async def meme(ctx):
    '''
    Send random meme. 
    Example: 
    --------------------------------------------
    -input- !meme
    -output- **send image**
    --------------------------------------------
    '''
    img_name = r.choice(os.listdir('m1l5\images'))
    with open(f'm1l5\images\{img_name}', 'rb') as f:
            picture = discord.File(f)
    await ctx.send(file=picture)
@bot.command()
async def fox(ctx):
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    await ctx.send(data['image'])
@bot.command()
async def what_time(ctx):
    seconds = time.time()
    local_time = time.ctime(seconds)
    await ctx.send(f"Local time is: {local_time}")

bot.run(settings["TOKEN"])