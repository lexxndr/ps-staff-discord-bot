import disnake
from disnake.ext import commands

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Shows Polaroid Studios info.")
    async def faq(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        faq_json = self.bot.jsones["faq.json"]

        view = disnake.ui.View()
        dropdown = disnake.ui.StringSelect(options=[disnake.SelectOption(label=value["label"], description=value["description"], value=key) for key, value in faq_json.items()])
        view.add_item(dropdown)

        async def page(inter: disnake.MessageInteraction, page_name: str):
            embed = disnake.Embed(
                title=faq_json[page_name]["label"],
                description=faq_json[page_name]["description"],
                color=disnake.Color.blue()
            )

            [embed.add_field(name=question["name"], value=question["value"], inline=False) for question in faq_json[page_name]["embed"]]
            embed.set_footer(text="Polaroid Studios • Community Support", icon_url=inter.author.display_avatar.url)

            return await inter.edit_original_message(content="", embed=embed, view=view)

        async def callback(interaction: disnake.MessageInteraction):
            await interaction.response.defer(ephemeral=True)
            await page(inter, interaction.values[0])


        dropdown.callback = callback
        return await page(inter, "serverQuestions")
        

def setup(bot):
    bot.add_cog(FAQ(bot))
