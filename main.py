import disnake, dotenv, json
from disnake.ext import commands

env = dotenv.dotenv_values('.env')

testGuilds = json.loads(env.get('testGuilds'))

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(intents=intents,test_guilds=testGuilds)

@bot.event
async def on_ready():
    print(f'gurt : {bot.user.id}')

bot.load_extensions('cogs')
bot.run(env.get('token'))