import aiohttp, json, aiofiles, asyncio, dotenv
from disnake.ext import commands
from rich import print

env = dotenv.dotenv_values('.env')

async def update_jsones(bot: commands.InteractionBot):
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