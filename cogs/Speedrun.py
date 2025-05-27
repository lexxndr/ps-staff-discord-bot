import disnake, aiohttp, asyncio, json, disnake.ui as ui
from disnake.ext import commands
from collections import deque
from datetime import datetime, timedelta
from rich import print

AUTOCOMPLETE_LIMIT = 25
BASE_URL = "https://www.speedrun.com/api/v1/"
GAME_ID = "m1mn0ekd"
RETRIES = 3
RATE_LIMIT_PER_MINUTE = 100
RATE_LIMIT_WINDOW_SECONDS = 60

class Request:
    def __init__(self):
        self.request_timestamps = deque()
        self.lock = asyncio.Lock()
        self.session: aiohttp.ClientSession = None

    async def __aenter__(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        print("[bold cyan]Request handler session opened.[/bold cyan]")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session and not self.session.closed:
            await self.session.close()
            print("[bold cyan]Request handler session closed.[/bold cyan]")

    async def _wait_for_rate_limit(self):
        async with self.lock:
            now = datetime.now()
            while self.request_timestamps and \
                  now - self.request_timestamps[0] > timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS):
                self.request_timestamps.popleft()

            if len(self.request_timestamps) >= RATE_LIMIT_PER_MINUTE:
                time_to_wait = (self.request_timestamps[0] + \
                                timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS)) - now
                
                sleep_duration = max(0.1, time_to_wait.total_seconds())
                print(f"[bold yellow]:hourglass: [Speedrun] Rate limit hit ({len(self.request_timestamps)}/{RATE_LIMIT_PER_MINUTE}). Waiting for {sleep_duration:.2f} seconds...[/bold yellow]")
                await asyncio.sleep(sleep_duration)
                
                now = datetime.now()
                while self.request_timestamps and \
                      now - self.request_timestamps[0] > timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS):
                    self.request_timestamps.popleft()

            self.request_timestamps.append(datetime.now())
            print(f"[green]Request queued. Current rate: {len(self.request_timestamps)}/{RATE_LIMIT_PER_MINUTE}[/green]")

    async def request(self, url: str):
        if self.session is None or self.session.closed:
            raise RuntimeError("aiohttp.ClientSession is not open. Use 'async with Request()' to manage session.")

        tries = RETRIES
        while tries > 0:
            await self._wait_for_rate_limit()
            try:
                print(f"[blue]Attempting to fetch: {url}[/blue]")
                async with self.session.get(BASE_URL+url) as response:
                    status = response.status
                    response_json = await response.json()

                    if status == 200:
                        return response_json
                    elif status == 420:
                        print(f":x: [bold red][API Throttled] <{status}> Rate limited by API.[/bold red]")
                    else:
                        print(f":x: [bold red][API Error] <{status}> Failed to get data from {url}, response > {response_json}[/bold red]")

            except aiohttp.ClientError as e:
                print(f":x: [bold red][Network Error] {e}[/bold red]")
            except json.JSONDecodeError:
                print(f":x: [bold red][JSON Error] Could not decode JSON from response at {url}[/bold red]")
            except Exception as e:
                print(f":x: [bold red][Unexpected Error] {e}[/bold red]")

            tries -= 1
            if tries > 0:
                print(f"[yellow]Retrying in 2 seconds... ({tries} attempts left)[/yellow]")
                await asyncio.sleep(2)
        print(f":x::warning: [bold red]Failed to get data after {RETRIES} retries for {url}.[/bold red]")
        return None
    
class Speedrun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_data = {}
        #self.emoji_list = {1: "<:1st:1376607630226624733>", 2: "<:2nd:1376607670491938856>", 3: "<:3rd:1376607686594002994>"} # {1: "<:1st:1376607630226624733>", 2: "<:2nd:1376607670491938856>", 3: "<:3rd:1376607686594002994>"} # implement app emojis someday // https://github.com/Snipy7374/disnake/tree/feat/app_emojis
        self.request = Request() 
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.request.__aenter__()
        data = await self.request.request(f"games/{GAME_ID}?embed=category,categories,levels")
        self.game_data = data
        print(":information_source:   [white]speedrun.com data[/white] loaded.")

    def cog_unload(self):
        asyncio.create_task(self.request.__aexit__(None, None, None))

    @commands.slash_command(name="speedrun")
    async def speedrun_group(self, inter: disnake.ApplicationCommandInteraction): pass

    @speedrun_group.sub_command(name="leaderboard", description="Apeirophobia's Speedrun leaderboard")
    async def leaderboard_command(self, inter: disnake.ApplicationCommandInteraction, category, variable):
        if not variable: variable = "02q73nyd" if category == "fullgame" else "q255mxg2"
        await inter.response.defer()

        response = await self.request.request(f"categories/{variable}/records?embed=category,players") # self.request.request(f"runs?category={variable}&max=1&embed=category,players")
        #print(response)
        response_data = response.get("data", {})[0]
        category_data = response_data.get("category", {}).get("data", {})
        runs_data = response_data.get("runs", [])
        players_data = response_data.get("players", {})
        users_data = {user.get("id"): user for user in players_data.get("data")}
        #print(users)

        nl = "\n"

        lines = []

        for run in runs_data:
            place = run.get("place")
            data = run.get("run", {})

            link = data.get("weblink")
            date = round(datetime.fromisoformat(data.get("submitted")).timestamp())
            time = data.get("times", {}).get("primary")
            players = [users_data.get(player.get("id")) for player in data.get("players", [])]
            #print(players)

            for k, v in [("PT", ""), ("S", ""), ("M", ":"), ("H", ":"), ("D", ":")]: time = time.replace(k, v)
            content = f"""
{self.bot.app_emojis[f"{place}_"] if place <= 3 else place} — {time} — {"; ".join([f'''{":flag_"+player.get("location", {}).get("country", {}).get("code").split("/")[0].lower()+":" if player.get("location") else "🌐"} {"~~" if player.get("role") == "banned" else ""}[{player.get("names", {}).get("international")}](<{player.get("weblink")}>){"~~" if player.get("role") == "banned" else ""}''' for player in players])}
[Link 🔗](<{link}>) • Achieved <t:{date}:R>
"""
            lines.append(content)

        container = ui.Container(
            ui.MediaGallery(
                disnake.MediaGalleryItem({"media": {"url": self.game_data.get("data", {}).get("assets", {}).get("logo", {}).get("uri")}}),
            ),
            ui.TextDisplay("\n".join([f"""# [{category_data.get("name")}](<{category_data.get("weblink")}>)""", "## Rules: ", f"""{nl}> {f"{nl}> ".join(category_data.get("rules", None).split(nl))}""", "## Records: "])),
            ui.Separator(spacing=disnake.SeparatorSpacingSize.large),
            *[
                item
                for line in lines
                for item in (
                    ui.TextDisplay(line),
                    ui.Separator(spacing=disnake.SeparatorSpacingSize.large), 
                )
            ],
            accent_colour=disnake.Colour(0xf0b000),
            spoiler=False
        )
        await inter.edit_original_response(components=container, flags=disnake.MessageFlags(is_components_v2=True))

    @leaderboard_command.autocomplete("category")
    async def category_autocomplete(self, inter: disnake.ApplicationCommandInteraction, user_input: str):
        user_inputed = user_input.lower()
        
        game_data = self.game_data

        mapped = [(level.get("name"), level.get("id")) for level in game_data.get("data", {}).get("levels", {}).get("data")]
        mapped.insert(0, ("Full-Game", "fullgame"))
        options = [disnake.OptionChoice(name = k, value = v) for k, v in mapped]

        return [option for option in options if user_inputed in option.name.lower()][:AUTOCOMPLETE_LIMIT]

    @leaderboard_command.autocomplete("variable")
    async def variable_autocomplete(self, inter: disnake.ApplicationCommandInteraction, user_input: str):
        user_inputed = user_input.lower()

        game_data = self.game_data
        variables = game_data.get("data", {}).get("categories", {}).get("data", [])

        filled = inter.filled_options.get("category")
        target = "per-level"
        if filled == "fullgame": target = "per-game"

        filtered = [(variable.get("name"), variable.get("id")) for variable in variables if target in variable.get("type")]
        options = [disnake.OptionChoice(name = k, value = v) for k, v in filtered]
        
        return [option for option in options if user_inputed in option.name.lower()][:AUTOCOMPLETE_LIMIT]
    
def setup(bot): # setup the cog
    bot.add_cog(Speedrun(bot))