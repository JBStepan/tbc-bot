import discord

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Ready")

@bot.slash_command()
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")

bot.run("")
