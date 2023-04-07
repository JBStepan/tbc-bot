import discord

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Ready")

@bot.slash_command()
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")

#bot.load_extension('cogs.levels')
bot.load_extension('cogs.weather')


bot.run("")
