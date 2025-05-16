import disnake, aiofiles, aiohttp, asyncio, dotenv, json
from disnake.ext import commands, tasks

env = dotenv.dotenv_values('.env')

testGuilds = json.loads(env.get('testGuilds'))

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(intents=intents,test_guilds=testGuilds)

async def update_ts(bot: commands.InteractionBot):
    async with aiohttp.ClientSession() as session:
        url_base = env.get("guthib")

        async def updater(session: aiohttp.ClientSession, filename):
            request = await session.get(url_base+filename)

            if request.status == 200:
                response = await request.text()
                content = json.loads(response)

                async with aiofiles.open(f"./json/{filename}", "w", encoding="utf8") as file:
                    dumped = json.dumps(content)
                    await file.write(dumped)
                    print("sawed off")

            else:
                print(f"foiled to get {filename} from guthib, using local file")
                async with aiofiles.open(f"./json/{filename}", "r", encoding="utf8") as file:
                    content = json.loads(await file.read())

            
            return filename, content
    
        tasks = [updater(session, filename) for filename in ["faq.json", "newlevel.json", "systemprompt.json"]]
        responses = await asyncio.gather(*tasks)
        bot.jsones = {response[0]: response[1] for response in responses}

@tasks.loop(minutes=10)
async def json_updater():
    return await update_ts(bot)

@bot.event
async def on_ready():
    print(f'gurt : {bot.user.id}')
    return await update_ts(bot)

bot.load_extensions('cogs')
bot.run(env.get('token'))