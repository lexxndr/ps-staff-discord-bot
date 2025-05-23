# Polaroid Bot

## What is this?
This is a Polaroid Studios Discord bot that provides features such as displaying in-game levels, entities, badges, frequently asked questions and automated responses.

## Installation
**Python 3.10 or higher is required.**

1. Install the requirements:
```sh
# Linux/macOS
python3 -m pip install -U -r requirements.txt

# Windows
py -3 -m pip install -U -r requirements.txt
```

2. Prepare your `.env` file with the following variables:
```
TOKEN=your discord token
GUTHIB=your [GitHub raw URL](#getting-github-raw-url)
TEST_GUILDS=[your test guild IDs]
TICKET_CATEGORY=your ticket category ID
QOTD_CHANNEL=your QOTD channel ID
QOTD_ALLOWED_ROLE_IDS=[allowed role IDs for QOTD]
QOTD_ALLOWED_USER_IDS=[allowed user IDs for QOTD]
```

### Getting GitHub raw URL

To get the GitHub raw URL, follow these steps:

1. Go to your GitHub repository and open any file in the `/json` directory.
2. Add `?raw=true` at the end of the URL and navigate to the resulting link. It should look something like this:  
   `https://raw.githubusercontent.com/lexxndr/ps-staff-discord-bot/refs/heads/main/json/badges.json`
3. Remove everything after the last `/` in that URL, so it looks like this:  
   `GUTHIB=https://raw.githubusercontent.com/lexxndr/ps-staff-discord-bot/refs/heads/main/json/`  
   If you try to open this URL in your browser, you will get a `400: Invalid request` error, but this is expected and will not affect the bot.
4. Copy the link and paste it into your `.env` file.

## Usage
Run the bot with:
```sh
python main.py
```
Make sure your `.env` file is in the correct location and filled with the appropriate values.

## Support
If you encounter issues, please check your setup, Python version, and environment variables.

## Credits
Most of this code was written by 303 and me.
havaka - python police, helped a lot with coding
jaymetrics - filled in most of .json files with Apeirophobia information
ted - helped with the code and testing
