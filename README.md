# My Discord Bot

A beginner-friendly Discord bot built with Python and discord.py.

## Features
- Fun commands: jokes, dice rolling, coin flip, random chooser
- Utility: weather, polls, server info, ping
- Auto-welcome new members

## Commands
| Command | Description |
|--------|-------------|
| `!hello` | Bot says hello |
| `!roll [sides]` | Roll a dice (default: 6 sides) |
| `!flip` | Flip a coin |
| `!joke` | Get a programming joke |
| `!choose option1 option2 ...` | Bot picks an option |
| `!ping` | Check bot latency |
| `!poll "question" opt1 opt2 ...` | Create a poll |
| `!weather [city]` | Get weather for a city |
| `!serverinfo` | Show server details |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create your bot
1. Go to [discord.com/developers](https://discord.com/developers/applications)
2. Click **New Application** → give it a name
3. Go to **Bot** tab → click **Add Bot**
4. Copy your **Token**
5. Replace `"YOUR_BOT_TOKEN"` in `bot.py` with your token

### 3. Get a free Weather API key (optional)
1. Sign up at [openweathermap.org](https://openweathermap.org/api)
2. Copy your API key
3. Replace `"YOUR_OPENWEATHER_API_KEY"` in `bot.py`

### 4. Invite bot to your server
1. In Discord Developer Portal → **OAuth2** → **URL Generator**
2. Check `bot` scope
3. Check permissions: `Send Messages`, `Read Messages`, `Add Reactions`, `Embed Links`
4. Copy the URL and open it to invite the bot

### 5. Run the bot
```bash
python bot.py
```

## Ideas for future updates
- [ ] Add music playback
- [ ] Add XP/leveling system
- [ ] Add moderation commands (kick, ban, mute)
- [ ] Connect to Claude AI for smart responses
- [ ] Add mini-games (trivia, hangman)
- [ ] Add reminder command
