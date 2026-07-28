import discord
from discord import app_commands
from discord.ext import commands

from crawlers.limbus import LimbusCrawler


class Limbus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.crawler = LimbusCrawler()

    def format_news_list(self, news_list, max_items=4):
        """공지 목록을 지정된 개수만큼 링크 + 게시일시 조합으로 출력합니다."""
        if not news_list:
            return "등록된 소식이 없습니다."

        text = ""
        for item in news_list[:max_items]:
            text += f"• [{item['title']}]({item['url']})\n  └ 🗓️ `{item['date']}`\n"

        return text

    @app_commands.command(name="림버스", description="림버스 컴퍼니 최신 정보 공지")
    async def limbus(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        try:
            status = await self.crawler.get_status()

            embed = discord.Embed(
                title="🎭 림버스 컴퍼니 최신 공지 목록",
                description="제목을 클릭하면 해당 스팀 공지로 이동합니다.",
                colour=0xB71C1C,
            )

            # 1. 픽업 및 추출 소식 (가장 최신 1개만 출력)
            embed.add_field(
                name="🎲 최신 픽업 공지",
                value=self.format_news_list(status["pickups"], max_items=1),
                inline=False,
            )

            # 2. 이벤트 소식 (최대 3개)
            embed.add_field(
                name="🎉 주요 이벤트 및 시즌 공지",
                value=self.format_news_list(status["events"], max_items=3),
                inline=False,
            )

            # 3. 업데이트 및 점검 (최대 3개)
            embed.add_field(
                name="🔧 점검 및 패치 공지",
                value=self.format_news_list(status["updates"], max_items=3),
                inline=False,
            )

            # 4. 기타 소식 (최대 3개)
            embed.add_field(
                name="📢 기타 공지",
                value=self.format_news_list(status["other"], max_items=3),
                inline=False,
            )

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"❌ 정보를 가져오는 중 오류가 발생했습니다: {e}"
            )


async def setup(bot):
    await bot.add_cog(Limbus(bot))