import disnake, json
from disnake.ext import commands
"""
from libs import dropdown

with open("json/serverFAQ.json", "r", encoding="utf-8") as f:
            faq_data = json.load(f)

options = []
for key in faq_data:
    entry = faq_data[key]
    options.append(disnake.SelectOption(label=entry.get("label", "No label"), description=entry.get("description", "")))
"""

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Show the Polaroid Studios FAQ.")
    async def faq(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        faq_json = self.bot.jsones["faq.json"]

        view = disnake.ui.View()
        dropdown = disnake.ui.StringSelect(options=[disnake.SelectOption(label=value["label"], description=value["description"], value=key) for key, value in faq_json.items()])
        view.add_item(dropdown)

        async def page(inter: disnake.MessageInteraction, page_name: str):
            embed = disnake.Embed(
                title=faq_json[page_name]["label"], # faq_json[page_name]["label"]
                description=faq_json[page_name]["description"], # faq_json[page_name]["description"]
                color=disnake.Color.blue()
            )

            [embed.add_field(name=question["name"], value=question["value"], inline=False) for question in faq_json[page_name]["embed"]]
            embed.set_footer(text="Polaroid Studios • Community Support", icon_url=inter.author.display_avatar.url)

            return await inter.edit_original_message(content="", embed=embed, view=view)

        async def callback(interaction: disnake.MessageInteraction):
            await interaction.response.send_message(content="** **", ephemeral=True, delete_after=0)
            await page(inter, interaction.values[0])


        dropdown.callback = callback
        return await page(inter, "serverQuestions")
        """
        async def dropdown_callback(interaction, selected_value):

            await interaction.response.edit_message(content=f"You selected: {selected_value}", embed=embed, view=view)
        """

        #view = dropdown.DropDownView(options, "select", callback_func=dropdown_callback)
        
        await inter.response.send_message(embed=embed)#, view=view, ephemeral=False)  # Change to False to make it public
        

def setup(bot):
    bot.add_cog(FAQ(bot))
