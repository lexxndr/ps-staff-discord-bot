import disnake
from disnake.ext import commands

class Breakthrough(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Show Breakthrough requirements.")
    async def breakthrough(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="🏆 Breakthrough (BT) Title Requirements",
            description="Detailed steps on how to obtain the **Breakthrough Title** in the speedrunning community.",
            color=disnake.Color.purple()
        )

        embed.add_field(
            name="Requirements:",
            value=(
                "1. Both PC and Mobile are allowed.\n"
                "2. WR must be on a full-game category **and** done solo.\n"
                "3. Run must be **submitted** for at least 3 days.\n"
                "4. At least **3** non-obsoleted runs must exist in the category (Mobile: at least 2).\n"
                "5. You must have the WR **at the time of submission**.\n"
                "6. DM a Speedrun Staff your WR run link to get the title.\n"
                "7. Once earned, the BT title is **yours forever**."
            ),
            inline=False
        )

        embed.add_field(
            name="🔎 Notes:",
            value=(
                "**submitted** → Time starts when you submit the run (verification date doesn't matter).\n"
                "**full-game** → Includes: Pre-Classic, Classic, Modern, Chapter 1, Chapter 2 Ending 1, Ending 2."
            ),
            inline=False
        )

        embed.set_footer(text="Polaroid Studios • Breakthrough Title", icon_url=inter.author.display_avatar.url)

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Breakthrough(bot))
