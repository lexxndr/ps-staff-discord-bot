import disnake, dotenv, json
from disnake.ext import commands, tasks
from rich import print
from utils import *

env = dotenv.dotenv_values('.env')

test_guilds = json.loads(env.get('TEST_GUILDS'))

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(intents=intents,test_guilds=test_guilds)

@tasks.loop(minutes=10)
async def json_updater():
    return await update_jsones(bot)

@bot.event
async def on_ready():
    print(f'[bold white on black]bot is ready![/bold white on black]')
    print(f':fish:  gurt : {bot.user.id}')

    tasks = [update_jsones(bot), get_app_emojis(bot)]
    
    return await asyncio.gather(*tasks)

bot.load_extensions('cogs')
bot.run(env.get('TOKEN'))