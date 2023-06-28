import json
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

    @commands.slash_command()
    async def messages(self, ctx: discord.ApplicationContext, user: discord.Option(discord.User, required=False)):
        if not user:
            with open('users.json', 'r') as f:
                users = json.load(f)
            
            await ctx.respond(f"You have sent, {users[f'{ctx.user.id}']} messages!")
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)

                await ctx.respond(f"{user.name} has sent, {users[f'{ctx.user.id}']} messages!")

    ###########
    #  Tasks  #
    ###########

def setup(bot: discord.Bot):
    bot.add_cog(other(bot))

