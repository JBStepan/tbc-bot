import os

class Type:
    cog = 1

FILE = input("What doyou want to call your file? ")
TYPE = int(input("Type? 1=Cog"))
path: str

if(TYPE == Type.cog):
    path = f"{os.curdir}/cogs/{FILE}"
else:
    pass

open(f"{path}.py", "x")

file = open(f"{path}.py", "w")
file.write(f"""
import discord
from discord.ext import commands

class {FILE}(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @commands.slash_command()
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond("Hello World!")

def setup(bot: discord.Bot):
    bot.add_cog({FILE}(bot))

""")

file.close()