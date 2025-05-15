import disnake, aiohttp, aiofiles, dotenv, json, os, disnake.ui as ui
from disnake.ext import commands
from typing import Sequence

env = dotenv.dotenv_values('.env') or os.environ

class levelInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelList = {}
        self.emojiList = {"Badges": "<:Overview:1372561106219827341>", "Description": "<:Description:1372561094014537830>", "Tutorial": "<:Objective:1372561114524553226>", "Entities": "<:Skull:1372670255284883476>", "Fun Facts": "<:Tips:1372670198125035571>", "Level Type": "<:Note:1372670234841845973>"}
            # available emojis
            # <:Origin:1372670213702811728>; <:Question:1372670182937460766>; <:Exit:1372670158610632905>; <:Gallery:1372670132249296946>; <:Wrench:1372670271957368893>
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
        image1 = content['image1']
        image2 = content['image2']

        components: Sequence[ui.UIComponent] = [ # init components v2
            ui.Container(
                ui.TextDisplay(f'# {level}'),
                *[ # i have no idea how this works but its perfect and i dont want to touch this EVER
                    item
                    for key, value in sections.items()
                    for item in (
                        ui.TextDisplay(f"## {self.emojiList.get(key, '')}  {key}\n**    {value}**"),
                        ui.Separator(spacing=disnake.SeparatorSpacingSize.small),
                    )
                ],
                ui.MediaGallery( # add more mediagalleryitem objects if need more images but it may break everything
                    disnake.MediaGalleryItem(
                        {
                            "media": {"url": image1},
                        },
                    ),
                    disnake.MediaGalleryItem(
                        {
                            "media": {"url": image2},
                        },
                    )
                ), # for now only 2 screenshots are being used so dont change this
                accent_colour=disnake.Colour(0xf0b000),
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