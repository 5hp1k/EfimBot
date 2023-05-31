import asyncio
import discord
from discord.ext import commands
from discord_token import TOKEN
from EfimBot import EfimBot as Efim


async def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix='//', intents=intents)

    await bot.add_cog(Efim(bot))
    await bot.start(TOKEN, reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())
