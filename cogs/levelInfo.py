import disnake, aiohttp, aiofiles, dotenv, json, os, disnake.ui as ui
from disnake.ext import commands
from typing import Sequence

env = dotenv.dotenv_values('.env') or os.environ

#levelList = json.loads(open('./json/newlevel.json', 'r').read())

class levelInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelList = {}
        self.emojiList = {"Overview": "<:Overview:1372561106219827341>", "Description": "<:Description:1372561094014537830>", "Objective": "<:Objective:1372561114524553226>"}
    
    @commands.Cog.listener()
    async def on_ready(self):
        async with aiohttp.ClientSession() as session:
            request = await session.get(env.get("guthib"))

            if request.status == 200:
                response = await request.text()
                jsoned = json.loads(response)
                self.levelList = jsoned

                async with aiofiles.open("./json/newlevel.json", "w") as file:
                    dumped = json.dumps(jsoned)
                    await file.write(dumped)
                    print("sawed off")

                return

            print("foiled to get list from guthib, using local file")
            async with aiofiles.open("./json/newlevel.json", "r") as file:
                content = await file.read()
                self.levelList = json.loads(content)

    @commands.slash_command(name='level', description='Shows information about a specified level.') # init the slash command
    async def levelinfo(self, interaction: disnake.CommandInteraction, level: str): # I understand it now.
        content = self.levelList[level]
        sections = content['sections']
        image = content['image']

        components: Sequence[ui.UIComponent] = [ # init components v2
            ui.Container(
                *[
                    item
                    for key, value in sections.items()
                    for item in (
                        ui.TextDisplay(f"## {self.emojiList.get(key, '')} {key}\n{value}"),
                        ui.Separator(spacing=disnake.SeparatorSpacingSize.large),
                    )
                ],
                ui.MediaGallery(
                    disnake.MediaGalleryItem(
                        {
                            "media": {"url": image},
                            "description": "The image of the specified level.",
                        },
                    )
                ),
                accent_colour=disnake.Colour(0xEE99CC),
                spoiler=False,
            ),
        ]

        await interaction.response.send_message(components=components, flags=disnake.MessageFlags(is_components_v2=True))
    
    @levelinfo.autocomplete("level")
    async def level_autocomplete(self, inter: disnake.ApplicationCommandInteraction, string: str):
        if not self.levelList:
            return []

        suggestions = [
            level_name for level_name in self.levelList.keys()
            if string.lower() in level_name.lower()
        ][:25]  # Discord limit for autocomplete options

        return suggestions

def setup(bot): # setup the cog
    bot.add_cog(levelInfo(bot))