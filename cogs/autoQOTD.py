import disnake
import dotenv
import json
import ast
from math import ceil
from disnake.ui import View, Button
from disnake import Interaction, ButtonStyle
from disnake.ext import commands, tasks
from datetime import datetime

env = dotenv.dotenv_values('.env')

QOTD_FILE = "json/qotds.json"
ALLOWED_ROLE_IDS = ast.literal_eval(env["QOTD_ALLOWED_ROLE_IDS"])
ALLOWED_USER_IDS = ast.literal_eval(env["QOTD_ALLOWED_USER_IDS"])


class AutoQOTD(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.qotd_channel_id = int(env["QOTD_CHANNEL"])
        self.qotd_post_time = (12, 0)  # Time in UTC (hour, minute)
        self.post_qotd.start()

# Test loop control: -----------------------------------------------------------------------------------------------------------------------------------------------------
        self.test_post_qotd_loop = None
    
    @commands.slash_command(description="Start posting QOTDs every 10 seconds for testing.")
    async def starttestqotd(self, inter: disnake.ApplicationCommandInteraction):
        if not self.is_allowed(inter):
            return await inter.response.send_message("You are not allowed to start the test.", ephemeral=True)

        if self.test_post_qotd_loop and self.test_post_qotd_loop.is_running():
            return await inter.response.send_message("Test QOTD posting is already running.", ephemeral=True)

        await inter.response.send_message("Starting test QOTD posting every 10 seconds...", ephemeral=True)

        # Create and start the test loop
        self.test_post_qotd_loop = tasks.Loop(self.send_qotd, seconds=10)
        self.test_post_qotd_loop.start()

    @commands.slash_command(description="Stop the test QOTD posting.")
    async def stoptestqotd(self, inter: disnake.ApplicationCommandInteraction):
        if not self.is_allowed(inter):
            return await inter.response.send_message("You are not allowed to stop the test.", ephemeral=True)

        if self.test_post_qotd_loop and self.test_post_qotd_loop.is_running():
            self.test_post_qotd_loop.cancel()
            return await inter.response.send_message("Stopped test QOTD posting.", ephemeral=True)

        await inter.response.send_message("Test QOTD posting is not running.", ephemeral=True)

# Delete above when ready to start the bot, this is for TESTING PURPOSES ONLY ------------------------------------------------------------------------------------------

    def get_qotds(self):
        try:
            with open(QOTD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_qotds(self, qotds):
        with open(QOTD_FILE, "w", encoding="utf-8") as f:
            json.dump(qotds, f, indent=2)

    def is_allowed(self, inter: disnake.ApplicationCommandInteraction):
        return (
            inter.author.id in ALLOWED_USER_IDS or
            any(role.id in ALLOWED_ROLE_IDS for role in inter.author.roles)
        )

    @commands.slash_command(description="Add a QOTD to the list.")
    async def addqotd(self, inter: disnake.ApplicationCommandInteraction, question: str):
        if not self.is_allowed(inter):
            return await inter.response.send_message("You are not allowed to add QOTDs.", ephemeral=True)

        await inter.response.defer(ephemeral=True)
        qotds = self.get_qotds()
        qotds.append(question)
        self.save_qotds(qotds)
        index = len(qotds)
        await inter.edit_original_message(content=f"✅ Added QOTD: `{question}`\nIndex: {index}")

    @commands.slash_command(description="Edit an upcoming QOTD.")
    async def editqotd(self, inter: disnake.ApplicationCommandInteraction, index: int, new_text: str):
        if not self.is_allowed(inter):
            return await inter.response.send_message("You are not allowed to edit QOTDs.", ephemeral=True)

        await inter.response.defer(ephemeral=True)
        qotds = self.get_qotds()

        if index < 1 or index > len(qotds):
            return await inter.edit_original_message(content="❌ Invalid QOTD index.")

        old = qotds[index - 1]
        qotds[index - 1] = new_text
        self.save_qotds(qotds)
        await inter.edit_original_message(content=f"✅ Updated QOTD #{index}:\nOld: `{old}`\nNew: `{new_text}`")

    @commands.slash_command(description="Show the list of QOTDs with their indexes.")
    async def qotdindex(self, inter: disnake.ApplicationCommandInteraction):
        if not self.is_allowed(inter):
            return await inter.response.send_message("You are not allowed to view QOTDs.", ephemeral=True)

        qotds = self.get_qotds()
        if not qotds:
            return await inter.response.send_message("No QOTDs found.", ephemeral=True)

        items_per_page = 15
        total_pages = ceil(len(qotds) / items_per_page)
        current_page = 1

        def build_embed(page: int):
            start = (page - 1) * items_per_page
            end = start + items_per_page
            page_qotds = qotds[start:end]
            description = "\n".join(f"**{i+1}.** {q}" for i, q in enumerate(page_qotds, start=start))
            return disnake.Embed(
                title=f"QOTD Index (Page {page}/{total_pages})",
                description=description or "No QOTDs found.",
                color=disnake.Color.blurple()
            )

        class QOTDIndexButtons(View):
            def __init__(self):
                super().__init__(timeout=120)

            @disnake.ui.button(label="Previous", style=ButtonStyle.blurple, disabled=True)
            async def prev_button(self, button: Button, interaction: Interaction):
                nonlocal current_page
                current_page -= 1
                embed = build_embed(current_page)
                self.update_buttons()
                await interaction.response.edit_message(embed=embed, view=self)

            @disnake.ui.button(label="Next", style=ButtonStyle.blurple, disabled=(total_pages == 1))
            async def next_button(self, button: Button, interaction: Interaction):
                nonlocal current_page
                current_page += 1
                embed = build_embed(current_page)
                self.update_buttons()
                await interaction.response.edit_message(embed=embed, view=self)

            def update_buttons(self):
                self.children[0].disabled = current_page <= 1
                self.children[1].disabled = current_page >= total_pages

            async def on_timeout(self):
                for child in self.children:
                    child.disabled = True
                await message.edit(view=self)

        view = QOTDIndexButtons()
        embed = build_embed(current_page)
        message = await inter.response.send_message(embed=embed, view=view, ephemeral=True)

    @tasks.loop(minutes=1)
    async def post_qotd(self):
        now = datetime.utcnow()
        if (now.hour, now.minute) == self.qotd_post_time:
            await self.send_qotd()

    async def send_qotd(self):
        qotds = self.get_qotds()
        if not qotds:
            print("[QOTD] No QOTDs left to post.")
            return

        question = qotds.pop(0)
        self.save_qotds(qotds)

        channel = self.bot.get_channel(self.qotd_channel_id)
        if not channel:
            print("[QOTD] QOTD channel not found.")
            return

        try:
            message = await channel.send(f"📢 **Question of the Day:**\n> {question}")
            await message.create_thread(name=f"QOTD - {datetime.utcnow().strftime('%b %d')}")
            print(f"[QOTD] Posted: {question}")
        except Exception as e:
            print(f"[QOTD] Failed to post: {e}")

    @post_qotd.before_loop
    async def before_qotd_loop(self):
        await self.bot.wait_until_ready()
        print("[QOTD] Background loop started.")

def setup(bot):
    bot.add_cog(AutoQOTD(bot))