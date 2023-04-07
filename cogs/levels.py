import discord
import random
import json
from discord.ext import commands

class LevelsCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    async def update_data(self, users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 0
            users[f'{user.id}']['num_messages'] = 0
    
    async def add_experience(self, users, user, exp):
        users[f'{user.id}']['num_messages'] += 1
        users[f'{user.id}']['experience'] += exp

    async def level_up(self, users, user, message):
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1 / 7))
        if lvl_start < lvl_end:
            await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
            users[f'{user.id}']['level'] = lvl_end

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != 1051631077455839242:
            if message.author.bot == False:
                with open('users.json', 'r') as f:
                    users = json.load(f)

                await self.update_data(users, message.author)
                if message.content.__len__() > 100 and message.attachments.__len__() > 1:
                    await self.add_experience(users, message.author, random.randrange(10, 15))
                elif message.content.__len__() > 100:
                    await self.add_experience(users, message.author, random.randrange(5, 10)) 
                elif message.attachments.__len__() > 1:
                    await self.add_experience(users, message.author, random.randrange(5, 10))
                else: 
                    await self.add_experience(users, message.author, random.randrange(1, 5))
                await self.level_up(users, message.author, message)

                with open('users.json', 'w') as f:
                    json.dump(users, f, sort_keys=True, indent=4)

    @commands.slash_command()
    async def level(self, ctx: discord.ApplicationContext):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not str(ctx.author.id) in users:
            users[f'{ctx.author.id}'] = {}
            users[f'{ctx.author.id}']['experience'] = 0
            users[f'{ctx.author.id}']['level'] = 0
            users[f'{ctx.author.id}']['num_messages'] = 0

            with open('users.json', 'r'):
                json.dump(users, f, sort_keys=True, indent=4)

            await ctx.respond(f"{ctx.author.mention} you have not sent anything yet!")
        else:
          await ctx.respond(f"{ctx.author.mention} you are currently level {users[f'{ctx.author.id}']['level']}. You have sent **{users[f'{ctx.author.id}']['num_messages']}** messages!")

def setup(bot: discord.Bot):
    bot.add_cog(LevelsCog(bot))