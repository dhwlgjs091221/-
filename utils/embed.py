import discord


def create_status_embed(game_name, status):

    embed = discord.Embed(
        title=game_name,
        colour=0xd11f2a
    )

    embed.add_field(
        name="📅 시즌",
        value=status.season,
        inline=False
    )

    embed.add_field(
        name="🎉 이벤트",
        value=status.event,
        inline=False
    )

    embed.add_field(
        name="🎲 픽업",
        value=status.pickup,
        inline=False
    )

    embed.add_field(
        name="🔧 점검",
        value=status.maintenance,
        inline=False
    )

    embed.add_field(
        name="📢 최신 공지",
        value=status.notice,
        inline=False
    )

    return embed