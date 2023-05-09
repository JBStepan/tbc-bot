import discord

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Ready")

bot.load_extension('cogs.weather')

bot.run("")