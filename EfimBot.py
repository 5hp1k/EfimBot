import discord
from discord.ext import commands
import aiohttp
import os
import datetime
from bs4 import BeautifulSoup
import random


class EfimBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anecdotes = []

    async def log_message(self, ctx):
        author_id = ctx.author.id
        author_name = ctx.author.name
        message_content = ctx.message.content
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not os.path.exists("logs"):
            os.makedirs("logs")

        log_file_path = f"logs/{author_id}.txt"

        with open(log_file_path, "a") as file:
            file.write(f"[{timestamp}] {author_name}: {message_content}\n")

    async def get_anecdotes(self):
        for i in range(25):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://anekdotov.net/anekdot/index-page-{i}.html") as response:
                    html_text = await response.text()
                    soup = BeautifulSoup(html_text, "html.parser")
                    page_content = soup.find_all('div', {'class': 'anekdot'})
                    for line in page_content:
                        anecdote = line.find('p').text
                        self.anecdotes.append(anecdote)

        print(f"Anecdote list is ready!")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.get_anecdotes()
        print(f'{self.bot} is online and ready')

    @commands.command(aliases=['capybara', 'capy', 'capybarka', 'carbonara',
                               'carburator', 'kartoshka', 'funny_animal',
                               'cabbage', 'coconut_doggy', 'ok_i_pull_up',
                               'caterpillar'])
    async def send_capybara_image(self, ctx):
        await self.log_message(ctx)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.capy.lol/v1/capybara?json=true") as response:
                data = await response.json()
                print(f"session.get(''https://api.capy.lol/v1/capybara?json=true'')"
                      f"\nResponse status: {response.status}")
                url = data['data']['url']
                image = discord.Embed(title=random.choice(['балдеж-то какой', 'ok he pull up', 'какой же он крутой',
                                                           'ему точно можно доверить огнестрельное оружие :)']),
                                      color=discord.Color.random())
                image.set_image(url=url)
                await ctx.send(embed=image)

    @commands.command(aliases=['anecdote', 'anec', 'anekdot', 'anek'])
    async def send_anecdote(self, ctx):
        await self.log_message(ctx)
        await ctx.send(random.choice(self.anecdotes))
