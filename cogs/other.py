import discord
from discord.ext import commands


class other(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    ##############
    #  Commands  #
    ##############

    @commands.slash_command()
    async def cyrus_time(self, ctx: discord.ApplicationContext):
        await ctx.respond("Hello World!")

    ###########
    #  Tasks  #
    ###########

def setup(bot: discord.Bot):
    bot.add_cog(other(bot))

