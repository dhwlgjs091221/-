import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")


class GameNewsBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # cogs/limbus.py 로드
        await self.load_extension("cogs.limbus")

        # 슬래시 명령어 동기화
        synced = await self.tree.sync()
        print(f"{len(synced)}개의 슬래시 명령어 동기화 완료")

    async def on_ready(self):
        print(f"{self.user} 로그인 완료!")


bot = GameNewsBot()

if TOKEN is None:
    raise ValueError(".env 파일에 TOKEN이 설정되지 않았습니다.")

bot.run(TOKEN)