import discord
import json

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot == True:
        return

    if msg.interaction:
        return 
    
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if not f'{msg.author.id}' in users:
        users[f'{msg.author.id}'] = 0
    
    users[f'{msg.author.id}'] += 1

    with open('users.json', 'w') as i:
        json.dump(users, i, indent=4)

bot.load_extension('cogs.weather')
bot.load_extension('cogs.other')


bot.run("MTAzNzU3MTA5MzMzNjE2MjM2NQ.G97OZT.lpfxWs9eMG9s4EiMRmdV3wcD3Ez8F3MsXK7DFA")