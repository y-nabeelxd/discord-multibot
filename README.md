<div align="center">

# Discord MultiBot

**Modular Discord bot written in Python for music streaming, moderation, economy, and player verification.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![discord.py](https://img.shields.io/badge/discord.py-2.3%2B-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
[![License: MIT](https://img.shields.io/github/license/y-nabeelxd/discord-multibot?color=brightgreen)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/y-nabeelxd/discord-multibot?style=social)](https://github.com/y-nabeelxd/discord-multibot)
[![GitHub Forks](https://img.shields.io/github/forks/y-nabeelxd/discord-multibot?style=social)](https://github.com/y-nabeelxd/discord-multibot)
[![Code Style: Prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://prettier.io)

[Quick Start](#setup--installation) • [Features](#features) • [Commands](#commands) • [Verification](#multi-game-verification) • [License](#license)

---

</div>

## Overview

Discord MultiBot is a cog-based bot written with `discord.py` 2.3+. It consolidates audio streaming, moderation utilities, game verification checks, virtual economy minigames, and support ticket management into a single service.

- **Audio playback**: Streaming engine backed by `yt-dlp` and `FFmpeg` with automatic SoundCloud fallback and button controls.
- **Server moderation**: Punishment tools including bans, kicks, timeouts, warnings, channel locks, and message purging.
- **Player verification**: Account verification for Roblox (code in bio), FiveM (live server queries), and SA:MP (MySQL/RCON).
- **Hybrid commands**: All primary commands work both as slash commands (`/`) and message prefixes (`!`).
- **Economy and minigames**: Virtual balance, daily rewards, coinflip, slots, work, and chat-based XP progression.
- **Tickets and giveaways**: Interactive button panels for support threads and automated giveaway timers.

---

## Features

| Category     | Description                                                                | Slash Support |
| :----------- | :------------------------------------------------------------------------- | :-----------: |
| Music        | Search, queue, skip, pause, resume, lyrics, SoundCloud fallback            |      Yes      |
| Moderation   | Ban, kick, timeout (1s to 28d), warnings, message purge, channel lock      |      Yes      |
| Verification | Roblox (code-in-bio), FiveM (query), SA:MP (MySQL/RCON)                    |      Yes      |
| Leveling     | Passive chat XP, rank cards, server leaderboard                            |      Yes      |
| Tickets      | Button panel, private thread creation, transcript exports                  |      Yes      |
| Giveaways    | Timed entries with button join and automatic winner selection              |      Yes      |
| Economy      | Balance tracking, daily claims, coinflip, slots, transfers                 |      Yes      |
| Games        | Tic-Tac-Toe, Rock Paper Scissors, 8-Ball, Trivia, coin flip                |      Yes      |
| Utilities    | Safe AST calculator, weather reports, Google translation, polls, reminders |      Yes      |

---

## Project Structure

```
discord-multibot/
├── bot.py                     # Bot entrypoint and extension loader
├── config.py                  # Configuration loader backed by .env
├── utils.py                   # Reusable helpers and network clients
├── test_load.py               # Automated verification test suite
├── requirements.txt           # Python package dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Tracked file exclusions
├── .prettierrc.json           # Code style formatting rules
└── plugins/                   # Cog modules
    ├── music/                 # Audio streaming (yt-dlp + FFmpeg)
    ├── moderation/            # Member and channel administration
    ├── verification/          # Roblox, FiveM, and SA:MP verification
    ├── leveling/              # XP calculation and storage
    ├── ticket/                # Ticket panels and channel management
    ├── giveaway/              # Timed giveaway coordinator
    ├── economy/               # Virtual currency and games
    ├── fun/                   # Social commands and minigames
    ├── utility/               # Weather, calculator, translate, reminder
    └── slash/                 # Dedicated slash management and voice routing
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/y-nabeelxd/discord-multibot.git
cd discord-multibot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> [!NOTE]
> On Windows, `static-ffmpeg` configures FFmpeg automatically. On Linux servers, install FFmpeg via your package manager:
>
> ```bash
> sudo apt update && sudo apt install -y ffmpeg
> ```

### 3. Configure environment variables

Copy the template:

```bash
cp .env.example .env
```

Set your values in `.env`:

```env
# Bot configuration
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
GAME_PREFIX=owo
BOT_OWNER_ID=your_discord_user_id

# Optional services
WEATHER_API_KEY=your_openweathermap_key
YT_COOKIES=cookies.txt

# Verification settings
VERIFICATION_ROBLOX=true
ROBLOX_ROLE_ID=123456789012345678

VERIFICATION_FIVEM=true
FIVEM_SERVER=127.0.0.1:30120
FIVEM_ROLE_ID=123456789012345678

VERIFICATION_SAMP=true
SAMP_ROLE_ID=123456789012345678
```

> [!IMPORTANT]
> Enable all three **Privileged Gateway Intents** (Presence, Server Members, Message Content) in the [Discord Developer Portal](https://discord.com/developers/applications) under your bot application settings.

### 4. Run verification tests

```bash
python test_load.py
```

### 5. Start the bot

```bash
python bot.py
```

---

## Commands

All commands can be invoked with the configured prefix (`!`) or through native slash commands (`/`).

### Music

| Command   | Usage                  | Description                                    |
| :-------- | :--------------------- | :--------------------------------------------- |
| `!play`   | `!play <query or URL>` | Search or stream audio into your voice channel |
| `!lyrics` | `!lyrics [song name]`  | Retrieve song lyrics                           |
| `!queue`  | `!queue`               | Show active playlist queue                     |
| `!skip`   | `!skip`                | Skip current track                             |
| `!pause`  | `!pause`               | Pause active playback                          |
| `!resume` | `!resume`              | Resume paused playback                         |
| `!stop`   | `!stop`                | Stop playback and clear the queue              |
| `!vc247`  | `!vc247`               | Toggle 24/7 voice channel stay                 |

### Moderation

| Command     | Usage                         | Required Permission | Description                             |
| :---------- | :---------------------------- | :-----------------: | :-------------------------------------- |
| `!ban`      | `!ban @user [reason]`         |     Ban Members     | Ban a member                            |
| `!kick`     | `!kick @user [reason]`        |    Kick Members     | Kick a member                           |
| `!timeout`  | `!timeout @user 15m [reason]` |  Moderate Members   | Apply timeout (`1s` to `28d`)           |
| `!warn`     | `!warn @user [reason]`        |  Moderate Members   | Record a user warning                   |
| `!warnings` | `!warnings [@user]`           |  Moderate Members   | List recorded warnings                  |
| `!purge`    | `!purge <count>`              |   Manage Messages   | Delete recent messages (max 100)        |
| `!lock`     | `!lock [#channel]`            |   Manage Channels   | Prevent members from sending messages   |
| `!unlock`   | `!unlock [#channel]`          |   Manage Channels   | Re-enable message permissions           |
| `!nuke`     | `!nuke [#channel]`            |    Administrator    | Recreate channel and delete old history |

### Multi-Game Verification

| Platform         | Command                       |    Method    | Details                                          |
| :--------------- | :---------------------------- | :----------: | :----------------------------------------------- |
| **Roblox**       | `!verifyroblox <username>`    | Code in bio  | Generates verification code for user profile bio |
| **FiveM**        | `!verifyfivem <name/id>`      | Server query | Queries online players on target FiveM server    |
| **FiveM Live**   | `!fivemserverlive [#channel]` | Status embed | Auto-updating embed tracking server status       |
| **SA:MP**        | `!verifysamp [code/name]`     | MySQL / RCON | Validates account credentials against database   |
| **SA:MP Status** | `!sampstatus`                 | Query packet | Displays player count and server status          |

### Economy (Prefix: `owo`)

| Command        | Usage                                 | Description                              |
| :------------- | :------------------------------------ | :--------------------------------------- |
| `owo daily`    | `owo daily`                           | Claim daily coins (300 to 5,000)         |
| `owo balance`  | `owo balance [@user]`                 | View wallet balance                      |
| `owo coinflip` | `owo coinflip <amount> [heads/tails]` | Wager coins on a coin flip               |
| `owo slots`    | `owo slots <amount>`                  | Bet coins on the slot machine            |
| `owo work`     | `owo work`                            | Complete a job for currency              |
| `owo pay`      | `owo pay @user <amount>`              | Transfer coins to another user           |
| `owo rob`      | `owo rob @user`                       | Attempt to steal coins from another user |

### Tickets & Giveaways

| Command         | Usage                                  | Description                       |
| :-------------- | :------------------------------------- | :-------------------------------- |
| `!ticket setup` | `!ticket setup [#channel]`             | Post ticket creation button panel |
| `!ticket close` | `!ticket close`                        | Close active ticket thread        |
| `!gstart`       | `!gstart <duration> <winners> <prize>` | Start timed giveaway              |
| `!gend`         | `!gend <message_id>`                   | End giveaway immediately          |
| `!greroll`      | `!greroll <message_id>`                | Select a new winner               |

---

## Security

- **Safe math evaluation**: Calculator queries are parsed via Abstract Syntax Trees (`ast.parse`) instead of Python `eval()`. Disallows imports, attributes, and exponent computations exceeding threshold limits.
- **Bounded network calls**: All outbound HTTP requests enforce an explicit 10-second timeout to avoid event loop stalls.
- **Interaction safety**: Hybrid command handlers verify message existence before deletion to avoid `404 Unknown Interaction` errors.

---

## Contributing

1. Fork `https://github.com/y-nabeelxd/discord-multibot`
2. Create your branch: `git checkout -b feature/improvement`
3. Commit changes: `git commit -m 'feat: add improvement'`
4. Push to branch: `git push origin feature/improvement`
5. Open a pull request

---

## License

MIT License. See [LICENSE](LICENSE) for details.
