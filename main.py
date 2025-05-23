import disnake, aiofiles, aiohttp, asyncio, dotenv, json
from disnake.ext import commands, tasks
from rich import print

env = dotenv.dotenv_values('.env')

test_guilds = json.loads(env.get('TEST_GUILDS'))

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(intents=intents,test_guilds=test_guilds)

async def update_ts(bot: commands.InteractionBot):
    async with aiohttp.ClientSession() as session:
        url_base = env.get("GUTHIB")

        async def updater(session: aiohttp.ClientSession, filename):
            request = await session.get(url_base+filename)

            if request.status == 200:
                response = await request.text()
                content = json.loads(response)

                async with aiofiles.open(f"./json/{filename}", "w", encoding="utf8") as file:
                    await file.write(response)
                    print(f":information_source:   [white]{filename}[/white] loaded.")

            else:
                print(f"foiled to get {filename} from guthib, using local file")
                async with aiofiles.open(f"./json/{filename}", "r", encoding="utf8") as file:
                    content = json.loads(await file.read())

            
            return filename, content
    
        tasks = [updater(session, filename) for filename in ["faq.json", "new_level.json", "system_prompt.json", "badges.json", "qotds.json", "entities.json"]]
        responses = await asyncio.gather(*tasks)
        bot.jsones = {response[0]: response[1] for response in responses}

@tasks.loop(minutes=10)
async def json_updater():
    return await update_ts(bot)

@bot.event
async def on_ready():
    print(f'[bold white on black]bot is ready![/bold white on black]')
    print(f':fish:  gurt : {bot.user.id}')
    return await update_ts(bot)

bot.load_extensions('cogs')
bot.run(env.get('TOKEN'))