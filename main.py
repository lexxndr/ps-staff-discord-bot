import disnake, dotenv
from disnake.ext import commands

env = dotenv.dotenv_values('.env')

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(intents=intents,test_guilds=[1226166880960774225,1372528511985782877])

@bot.event
async def on_ready():
    print(f'gurt : {bot.user.id}')

bot.load_extensions('cogs')
bot.run(env.get('token'))