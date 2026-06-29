import discord


class GameEmbed:

    @staticmethod
    def create(game, title="🎮 Random Game Recommendation"):

        description = game["description"] or "No description available."

        # Discord embed descriptions are limited to 4096 characters
        if len(description) > 1000:
            description = description[:1000] + "..."

        embed = discord.Embed(
            title=title,
            description=f"## {game['name']}\n\n{description}",
            color=discord.Color.green()
        )

        embed.add_field(
            name="⭐ Rating",
            value=game["rating"] or "N/A",
            inline=True
        )

        embed.add_field(
            name="🏆 Metacritic",
            value=game["metacritic"] or "N/A",
            inline=True
        )

        embed.add_field(
            name="📅 Released",
            value=game["released"] or "Unknown",
            inline=True
        )

        embed.add_field(
            name="🎯 Genres",
            value=game["genres"] or "Unknown",
            inline=False
        )

        embed.add_field(
            name="🖥 Platforms",
            value=game["platforms"] or "Unknown",
            inline=False
        )

        embed.add_field(
            name="🏢 Developers",
            value=game["developers"] or "Unknown",
            inline=False
        )

        if game["website"]:
            embed.add_field(
                name="🌐 Website",
                value=game["website"],
                inline=False
            )

        if game["image"]:
            embed.set_image(url=game["image"])

        embed.set_footer(text="AfterHoursBot")

        return embed