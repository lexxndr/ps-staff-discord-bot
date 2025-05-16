import disnake
from disnake.ext import commands

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Show the Polaroid Studios FAQ.")
    async def faq(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="📘 Polaroid Studios Frequently Asked Questions",
            description="Here are answers to some of the most commonly asked questions in the server.",
            color=disnake.Color.blue()
        )

        embed.add_field(
            name="❓ Is the game still being worked on?",
            value="Yes, the game is actively being worked on.",
            inline=False
        )
        embed.add_field(
            name="⏳ When is the next update?",
            value="Nobody knows when the next update will be. Check out <#1021912153592176732> to see progress.",
            inline=False
        )
        embed.add_field(
            name="🔧 Why does the server update but not the game?",
            value="The development and moderation teams are separate. We manage different things.",
            inline=False
        )
        embed.add_field(
            name="🎮 What should I do while I wait for the update?",
            value="Try speedrunning! Check out <#1105613325875810435> to learn more.",
            inline=False
        )
        embed.add_field(
            name="🙊 What happened to the old owner?",
            value="Drama. They're not to be brought up here. Please respect that.",
            inline=False
        )
        embed.add_field(
            name="🖼️ How do I get image permissions?",
            value="Read <#1023773325006217256> to see which roles have image permissions.",
            inline=False
        )
        embed.add_field(
            name="📝 How do I post in <#1021973016269312032>?",
            value="You need to be **level 10 or higher** to post in suggestions.",
            inline=False
        )
        embed.add_field(
            name="⚡ How do I gain levels faster?",
            value="Be active in text channels and use the 'Fighting with Watcher' VC.",
            inline=False
        )
        embed.add_field(
            name="🆘 Can someone help me with the game?",
            value="Ask in <#1119009164312727663> or ping the **Game Guides** role.",
            inline=False
        )
        embed.add_field(
            name="👥 Does anyone want to play?",
            value="Visit <#1021909104949743658> to find others to play with.",
            inline=False
        )

        embed.set_footer(text="Polaroid Studios • Community Support", icon_url=inter.author.display_avatar.url)

        await inter.response.send_message(embed=embed, ephemeral=True)  # Change to False to make it public

def setup(bot):
    bot.add_cog(FAQ(bot))
