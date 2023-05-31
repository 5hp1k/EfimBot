import discord
from discord.ext import commands
import aiohttp
import random


class EfimBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot} is online and ready')

    @commands.command(aliases=['capybara', 'capy', 'capybarka', 'carbonara',
                               'carburator', 'kartoshka', 'funny_animal',
                               'cabbage', 'coconut_doggy', 'ok_i_pull_up',
                               'caterpillar'])
    async def send_capybara_image(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.capy.lol/v1/capybara?json=true") as response:
                data = await response.json()
                url = data['data']['url']
                image = discord.Embed(title=random.choice(['балдеж-то какой', 'ok he pull up', 'какой же он крутой',
                                                           'ему точно можно доверить огнестрельное оружие :)']),
                                      color=discord.Color.random())
                image.set_image(url=url)
                await ctx.send(embed=image)

    '''@commands.command(aliases=['anecdote', 'anec', 'anekdot', 'anek']):
        async def send_anecdote(self, ctx):
            async with aiohttp.ClientSession() as self:
                async with session.get'''