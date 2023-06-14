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

    async def log_message(self, ctx, bot_response):
        """Логгирование сообщений бота и его собеседника"""
        author_id = ctx.author.id
        author_name = f"{ctx.author.name}#{ctx.author.discriminator}"
        bot_name = f"{ctx.me.name}#{ctx.me.discriminator}"
        message_content = ctx.message.content
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not os.path.exists("logs"):
            os.makedirs("logs")

        log_file_path = f"logs/{author_id}.log"

        with open(log_file_path, "a") as file:
            file.write(f"[{timestamp}] {author_name}: {message_content}\n"
                       f"[{timestamp}] {bot_name}: {bot_response}\n")

    async def get_anecdotes(self):
        """Данная функция получает анекдоты путем веб-скраппинга 25 страниц с лучшими анекдотами
           сайта anekdotov.net"""
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
        """Данная функция активируется при запуске бота и перед началом работы запрашивает список анекдотов"""
        await self.get_anecdotes()
        print(f'{self.bot.user.name} (ID: {self.bot.user.id}) is online and ready')

    @commands.command()
    async def commands_info(self, ctx):
        """Вывод текстовоо сообщения с информацией о всех командах"""
        bot_response = f"Команды EfimBot\n" \
                       f"1. //help - информация обо всех доступных командах\n" \
                       f"2. //commands_info - аналог /help\n" \
                       f"3. //send_capybara_image (также можно использовать одну из следующиъ команд:\n" \
                       f"'capybara', 'capy', 'capybarka', 'carbonara', 'carburator', 'kartoshka', 'funny_animal',\n" \
                       f"'cabbage', 'coconut_doggy', 'ok_i_pull_up', 'caterpillar') " \
                       f"- отправляет картинку с капибарой, причем если указать параметр False," \
                       f"то будет выведен один из следующих заголовков изображения:" \
                       f"['балдеж-то какой', 'ok he pull up', 'какой же он крутой'," \
                       f"ему точно можно доверить огнестрельное оружие :)']\n" \
                       f"4. //send_anecdote (также можно использовать одну из следующих команд:\n" \
                       f"'anecdote', 'anec', 'anekdot', 'anek') - случайный анекдот с anekdotov.net\n" \
                       f"5. //clear_messages (int) - удаляет указанное количество сообщений " \
                       f"(если не указать количество, то удалит 1 сообщение)\n" \
                       f"6. //server_stats - выводит общую статистику сервера."
        await ctx.send(bot_response)
        await self.log_message(ctx, bot_response)

    @commands.command(aliases=['capybara', 'capy', 'capybarka', 'carbonara',
                               'carburator', 'kartoshka', 'funny_animal',
                               'cabbage', 'coconut_doggy', 'ok_i_pull_up',
                               'caterpillar'])
    async def send_capybara_image(self, ctx, api_title=True):
        """Получение ботом изображения с капибарой посредством обращения к сервису с изображениями через api,
        причем обращение асинхронно и происходит при помощи aiohttp. Также имеется возможность выбирать,
        какой заголовок будет у изображения: один из рандомных локальных или полученный по API"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.capy.lol/v1/capybara?json=true") as response:
                data = await response.json()
                url = data['data']['url']

                if api_title:
                    title = data['data']['alt']
                else:
                    title = random.choice(['балдеж-то какой', 'ok he pull up', 'какой же он крутой',
                                           'ему точно можно доверить огнестрельное оружие :)'])

                image = discord.Embed(title=title, color=discord.Color.random())
                image.set_image(url=url)
                await ctx.send(embed=image)
                await self.log_message(ctx, str(image.to_dict()))

    @commands.command(aliases=['anecdote', 'anec', 'anekdot', 'anek'])
    async def send_anecdote(self, ctx):
        """Отправляет один анекдот с одной из 25 страниц лучших анекдотов с сайта anekdotov.net"""
        bot_response = str(random.choice(self.anecdotes))
        await ctx.send(bot_response)
        await self.log_message(ctx, bot_response)

    @commands.command()
    async def clear_messages(self, ctx, amount: int = 1):
        """Удаление заданного количества сообщений. По стандарту оно равно 1"""
        bot_response = f"Удалено сообщений: {amount}."
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(bot_response, delete_after=60)
        await self.log_message(ctx, bot_response)

    @commands.command()
    async def server_stats(self, ctx):
        """Вывод информации о количестве участников сервера (в том числе и онлайн),
        количестве тексовых и голосовых каналов"""
        guild = ctx.guild
        members_count = guild.member_count
        online_count = sum(member.status != discord.Status.offline for member in guild.members)

        embed = discord.Embed(title="Статистика сервера", color=discord.Color.blue())
        embed.add_field(name="Участники", value=f"Всего: {members_count}\nОнлайн: {online_count}")
        embed.add_field(name="Каналы", value=f"Текстовые: {len(guild.text_channels)}\n"
                                             f"Голосовые: {len(guild.voice_channels)}")
        embed.set_footer(text=f"Сервер: {guild.name}")

        await ctx.send(embed=embed)
        await self.log_message(ctx, str(embed.to_dict()))
