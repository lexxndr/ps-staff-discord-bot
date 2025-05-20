# fucking polaroid bot

## what the fuck is this?
This is a fucking Polaroid Studios Discord bot that does some cool shit with levels and responses.

## installation
**Python 3.10 or higher is required.**

1. install the fucking requirements
```sh
# linux/macOS
python3 -m pip install -U -r requirements.txt

# wndows
py -3 -m pip install -U -r requirements.txt
```

2. get your fucking `.env` ready
```
TOKEN=your discord token
GUTHIB=your [github raw url](#getting-github-raw-url)
TEST_GUILDS=[your test guilds ids]
TICKET_CATEGORY=your ticket category id
QOTD_CHANNEL=your qotd channel id
```

### getting github raw url

to get the fucking github raw url, follow these damn steps:

1. head into your fucking GitHub repository and open any file in the `/json` directory
2. add `?raw=true` at the end of the url and go to the resulting link. it should look something like this:  
   `https://raw.githubusercontent.com/lexxndr/ps-staff-discord-bot/refs/heads/main/json/badges.json`
3. now, remove everything after the last `/` in that fucking url, now it should look like this: `GUTHIB=https://raw.githubusercontent.com/lexxndr/ps-staff-discord-bot/refs/heads/main/json/`. if you try to go to this url in your browser, you will get `400: Invalid request` error, but don't worry, the code will be fine
4. copy the link and paste it into your `.env` file.


## usage
run the bot with:
```sh
python main.py
```
make sure your `.env` file is in the right place and filled with the correct shit.

## support
if this shit breaks, i dont care if you are not a polaroid staff. check your setup, your python version, and your environment variables.

## credits
most of this code was written by 303 and me

